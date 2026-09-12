#!/usr/bin/env python3
"""Export canonical sections as standalone LaTeX and verify every Math node.

Run from any directory: python3 tools/export_sections.py --jobs 6
Compile an exported file from verified/sections so its image paths stay relative.
This checks export fidelity, not the mathematical correctness of the textbook.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "verified/sections"
HEADER = ROOT / "tools/latex-header.tex"
LAYOUT = ROOT / "tools/latex-layout.lua"
REPORT = ROOT / "quality/sections-latex.json"
COMPILE_REPORT = ROOT / "quality/sections-compile.json"
READER = "markdown-implicit_figures+tex_math_dollars"
EXPECTED_SECTIONS = 275


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def natural_key(path: Path) -> tuple:
    return tuple((0, int(s)) if s.isdigit() else (1, s)
                 for s in re.split(r"(\d+)", path.stem) if s)


def ast_nodes(value, node_type: str):
    """Visit JSON values in document order, including table cells and metadata."""
    if isinstance(value, dict):
        if value.get("t") == node_type:
            yield value
        for child in value.values():
            yield from ast_nodes(child, node_type)
    elif isinstance(value, list):
        for child in value:
            yield from ast_nodes(child, node_type)


def collect_ast_math(ast: dict) -> list[tuple[str, str]]:
    return [(node["c"][0]["t"], node["c"][1])
            for node in ast_nodes(ast, "Math")]


def collect_tex_math(tex: str) -> list[tuple[str, str]]:
    r"""Read unescaped \(...\) and \[...\] in order, without counting code.

    Escaped backslashes, comments, and verbatim environments cannot introduce
    delimiters. Braced groups may contain nested text/math without closing the
    enclosing outer Math node.
    """
    result = []
    i = 0
    while i < len(tex):
        if tex[i] == "%":
            end = tex.find("\n", i)
            i = len(tex) if end < 0 else end + 1
            continue
        if tex[i] != "\\":
            i += 1
            continue
        verbatim = re.match(
            r"\\begin\{(verbatim\*?|Verbatim|lstlisting|Highlighting)\}", tex[i:]
        )
        if verbatim:
            closing = r"\end{" + verbatim[1] + "}"
            end = tex.find(closing, i + verbatim.end())
            if end < 0:
                raise ValueError("Unclosed verbatim environment in exported TeX")
            i = end + len(closing)
            continue
        inline_verb = re.match(r"\\verb\*?([^A-Za-z\s])", tex[i:])
        if inline_verb:
            end = tex.find(inline_verb[1], i + inline_verb.end())
            if end < 0:
                raise ValueError("Unclosed verb command in exported TeX")
            i = end + 1
            continue
        delimiter = tex[i + 1:i + 2]
        if delimiter not in ("(", "["):
            # Skipping a control symbol also skips \\, \%, \{ and \}.
            i += 2
            continue
        kind = "InlineMath" if delimiter == "(" else "DisplayMath"
        closing = ")" if delimiter == "(" else "]"
        start = i + 2
        j, depth = start, 0
        while j < len(tex):
            if tex[j] == "%":
                end = tex.find("\n", j)
                j = len(tex) if end < 0 else end + 1
                continue
            if tex[j] == "\\":
                if tex[j + 1:j + 2] == closing and depth == 0:
                    result.append((kind, tex[start:j]))
                    i = j + 2
                    break
                j += 2
                continue
            if tex[j] == "{":
                depth += 1
            elif tex[j] == "}":
                depth -= 1
            j += 1
        else:
            raise ValueError(f"Unclosed {kind} delimiter at TeX character {i}")
    return result


def normalized_math(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    # The layout filter may add only this discretionary break inside Math.
    return [(kind, re.sub(r"\s+", "", re.sub(r"\\allowbreak(?![A-Za-z])", "", text)))
            for kind, text in items]


def sequence_digest(items: list[tuple[str, str]]) -> str:
    return digest(json.dumps(items, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8"))


def compare_math(source, exported) -> dict:
    left, right = normalized_math(source), normalized_math(exported)
    mismatches = []
    for index in range(max(len(left), len(right))):
        a = left[index] if index < len(left) else None
        b = right[index] if index < len(right) else None
        if a != b:
            mismatches.append({"math_index_1_based": index + 1,
                               "source": a, "exported": b})
            if len(mismatches) == 5:
                break
    return {
        "status": "pass" if left == right else "fail",
        "source_math_nodes": len(source),
        "exported_math_fragments": len(exported),
        "source_sequence_sha256": sequence_digest(left),
        "exported_sequence_sha256": sequence_digest(right),
        "first_mismatches": mismatches,
    }


def graphics_paths(tex: str) -> list[str]:
    """Extract includegraphics paths, including options with nested braces."""
    paths = []
    for match in re.finditer(r"\\includegraphics\*?(?![A-Za-z])", tex):
        i = match.end()
        while i < len(tex) and tex[i].isspace():
            i += 1
        if i < len(tex) and tex[i] == "[":
            depth, braces = 1, 0
            i += 1
            while i < len(tex) and depth:
                char = tex[i]
                if char == "\\":
                    i += 2
                    continue
                if char == "{":
                    braces += 1
                elif char == "}":
                    braces -= 1
                elif not braces:
                    if char == "[":
                        depth += 1
                    elif char == "]":
                        depth -= 1
                i += 1
        while i < len(tex) and tex[i].isspace():
            i += 1
        if tex[i:i + 1] != "{":
            raise ValueError("includegraphics has no braced file path")
        end = tex.find("}", i + 1)
        if end < 0:
            raise ValueError("includegraphics has an unclosed file path")
        paths.append(tex[i + 1:end])
    return paths


def check_images(ast: dict, tex: str) -> dict:
    source = [node["c"][2][0] for node in ast_nodes(ast, "Image")]
    exported = graphics_paths(tex)
    errors = []
    if source != exported:
        errors.append({"type": "image_sequence_changed",
                       "source": source, "exported": exported})
    for target in exported:
        parts = urlsplit(target)
        if parts.scheme or Path(target).is_absolute():
            errors.append({"type": "image_path_is_not_local_relative", "path": target})
        elif not (SECTIONS / unquote(parts.path)).is_file():
            errors.append({"type": "relative_image_missing", "path": target})
    return {"status": "pass" if not errors else "fail",
            "source_images": len(source), "exported_images": len(exported),
            "paths": exported, "errors": errors}


def run_pandoc(command: list[str], *, input_text: str | None = None) -> str:
    proc = subprocess.run(command, cwd=SECTIONS, input=input_text, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(f"Pandoc failed ({proc.returncode}): {proc.stderr.strip()}")
    if proc.stderr.strip():
        raise RuntimeError(f"Pandoc warning requires inspection: {proc.stderr.strip()}")
    return proc.stdout


def atomic_text(path: Path, text: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                     prefix=path.name + ".", suffix=".tmp",
                                     delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(text)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def export_section(source: Path, pandoc: str) -> dict:
    record = {"section_id": source.stem, "markdown": relative(source),
              "latex": relative(source.with_suffix(".tex"))}
    try:
        raw = source.read_bytes()
        record["markdown_sha256"] = digest(raw)
        ast_json = run_pandoc([pandoc, f"--from={READER}", "--to=json"],
                              input_text=raw.decode("utf-8"))
        ast = json.loads(ast_json)
        tex = run_pandoc([
            pandoc, "--from=json", "--to=latex", "--standalone", "--wrap=none",
            "-V", "documentclass=ctexart", "-V", "classoption=fontset=fandol",
            "-V", "fontsize=10pt", "-V", "colorlinks=true",
            "-V", "geometry:margin=16mm", "--include-in-header", str(HEADER),
            "--lua-filter", str(LAYOUT),
        ], input_text=ast_json)
        record["math_check"] = compare_math(collect_ast_math(ast), collect_tex_math(tex))
        record["image_check"] = check_images(ast, tex)
        record["latex_sha256"] = digest(tex.encode("utf-8"))
        record["status"] = "pass" if all(
            record[key]["status"] == "pass" for key in ("math_check", "image_check")
        ) else "fail"
        if source.read_bytes() != raw:
            raise RuntimeError("Canonical Markdown changed during export")
        if record["status"] == "pass":
            atomic_text(source.with_suffix(".tex"), tex)
    except Exception as exc:
        record.update(status="fail", error=str(exc))
    return record


def compile_all_sections(records: list[dict], jobs: int) -> int:
    """Compile each standalone file once, with all generated files in /tmp."""
    import fitz

    xelatex = shutil.which("xelatex")
    if not xelatex:
        raise RuntimeError("xelatex is not installed")
    work = Path(tempfile.mkdtemp(prefix="sections-compile-", dir="/tmp"))
    report = {
        "status": "in_progress",
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "All 275 canonical standalone section TeX files",
        "latex_export_report": "quality/sections-latex.json",
        "latex_export_report_sha256": digest(REPORT.read_bytes()),
        "engine": subprocess.check_output([xelatex, "--version"], text=True).splitlines()[0],
        "compile_passes_per_section": 1,
        "compile_cwd": "verified/sections",
        "concurrency": jobs,
        "temporary_output_root": str(work),
        "expected_sections": len(records),
        "completed_sections": 0,
        "passed_sections": 0,
        "failed_sections": [],
        "visual_scope": "Compilation is not a visual review of all 275 files. Representative visual receipts remain in sections-latex.json.",
        "checks": [],
    }

    def compile_one(record: dict) -> dict:
        source = ROOT / record["latex"]
        section = record["section_id"]
        output = work / section
        output.mkdir()
        check = {"section_id": section, "latex": record["latex"],
                 "latex_sha256": digest(source.read_bytes()),
                 "temporary_output_directory": str(output)}
        try:
            if check["latex_sha256"] != record["latex_sha256"]:
                raise RuntimeError("Standalone TeX changed after export validation")
            command = [xelatex, "-interaction=nonstopmode", "-halt-on-error",
                       "-output-directory=" + str(output), source.name]
            with (output / "compile.stdout").open("w", encoding="utf-8") as stream:
                proc = subprocess.run(command, cwd=SECTIONS, stdout=stream,
                                      stderr=subprocess.STDOUT)
            log_path = output / (section + ".log")
            log = log_path.read_text(errors="replace") if log_path.exists() else (
                output / "compile.stdout").read_text(errors="replace")
            check["command"] = command
            check["exit_code"] = proc.returncode
            check["missing_glyphs"] = [line for line in log.splitlines()
                                       if "Missing character" in line]
            check["warnings"] = [line for line in log.splitlines() if any(
                marker in line for marker in ("Overfull", "Warning:", "LaTeX Error", "! "))]
            pdf = output / (section + ".pdf")
            check["status"] = "pass" if proc.returncode == 0 and pdf.is_file() and not (
                check["missing_glyphs"]) else "fail"
            if check["status"] == "pass":
                with fitz.open(pdf) as document:
                    check["pdf_pages"] = len(document)
                check["temporary_pdf"] = str(pdf)
                check["pdf_sha256"] = digest(pdf.read_bytes())
                if digest(source.read_bytes()) != check["latex_sha256"]:
                    raise RuntimeError("Standalone TeX changed while being compiled")
            else:
                check["error_context"] = log[-7000:]
        except Exception as exc:
            check.update(status="fail", error=str(exc))
        return check

    def save_progress():
        report["updated_utc"] = datetime.now(timezone.utc).isoformat()
        report["completed_sections"] = len(report["checks"])
        report["passed_sections"] = sum(check["status"] == "pass" for check in report["checks"])
        report["failed_sections"] = [check["section_id"] for check in report["checks"]
                                     if check["status"] != "pass"]
        atomic_text(COMPILE_REPORT, json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    save_progress()
    # Exercise the regression case immediately while the remaining files compile.
    ordered = sorted(records, key=lambda record: record["section_id"] != "12.3.2")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(compile_one, record) for record in ordered]
        for future in as_completed(futures):
            check = future.result()
            report["checks"].append(check)
            if check["status"] != "pass" or check["section_id"] == "12.3.2":
                print(json.dumps(check, ensure_ascii=False), flush=True)
            if check["status"] != "pass" or len(report["checks"]) % 10 == 0:
                save_progress()
                print(f"Compiled {len(report['checks'])}/{len(records)} sections; "
                      f"failures={len(report['failed_sections'])}", flush=True)
    report["checks"].sort(key=lambda check: natural_key(Path(check["section_id"] + ".tex")))
    report["status"] = "pass" if all(check["status"] == "pass" for check in report["checks"]) else "fail"
    report["total_pdf_pages"] = sum(check.get("pdf_pages", 0) for check in report["checks"])
    report["regression_case"] = {
        "section_id": "12.3.2",
        "problem": "Converting the only Table to RawBlock hid its longtable/booktabs/array dependencies from Pandoc.",
        "fix": "Wrap the preserved Table AST with group/arraystretch RawBlocks so the standalone writer emits table dependencies.",
    }
    save_progress()
    print(json.dumps({key: report[key] for key in ("status", "completed_sections", "passed_sections",
                                                  "failed_sections", "total_pdf_pages")},
                     ensure_ascii=False), flush=True)
    return 0 if report["status"] == "pass" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=6, choices=range(1, 7),
                        help="Concurrent Pandoc jobs (maximum 6; default 6)")
    parser.add_argument("--compile-all", action="store_true",
                        help="Also compile all standalone sections once with XeLaTeX; output files go to /tmp")
    args = parser.parse_args()
    pandoc = shutil.which("pandoc")
    if not pandoc:
        parser.error("pandoc is not installed")
    for path in (HEADER, LAYOUT):
        if not path.is_file():
            parser.error(f"Missing shared configuration: {path}")
    sources = sorted(SECTIONS.glob("*.md"), key=natural_key)
    if len(sources) != EXPECTED_SECTIONS:
        parser.error(f"Expected {EXPECTED_SECTIONS} canonical sections; found {len(sources)}")
    config_hashes = {relative(path): digest(path.read_bytes()) for path in (HEADER, LAYOUT)}
    records = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(export_section, source, pandoc): source for source in sources}
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            if record["status"] != "pass":
                print(json.dumps(record, ensure_ascii=False), flush=True)
            elif len(records) % 50 == 0:
                print(f"Validated {len(records)}/{len(sources)} sections", flush=True)
    records.sort(key=lambda record: natural_key(Path(record["section_id"] + ".md")))
    errors = []
    for path in (HEADER, LAYOUT):
        if digest(path.read_bytes()) != config_hashes[relative(path)]:
            errors.append(f"Shared configuration changed during export: {relative(path)}")
    failed = [record["section_id"] for record in records if record["status"] != "pass"]
    representative_review = {"status": "pending", "section_ids": ["2.2.2", "2.2.4"]}
    if REPORT.exists():
        previous_review = json.loads(REPORT.read_text()).get("representative_compile_review", {})
        current_hashes = {record["section_id"]: record.get("latex_sha256") for record in records}
        checks = previous_review.get("checks", [])
        if (previous_review.get("status") == "pass" and
                {check.get("section_id") for check in checks} == {"2.2.2", "2.2.4"} and
                all(check.get("latex_sha256") == current_hashes.get(check.get("section_id")) for check in checks)):
            representative_review = previous_review
    report = {
        "status": "pass" if not failed and not errors else "fail",
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "canonical_source": "verified/sections/*.md",
        "exporter": "tools/export_sections.py",
        "exporter_sha256": digest(Path(__file__).read_bytes()),
        "pandoc_version": subprocess.check_output([pandoc, "--version"], text=True).splitlines()[0],
        "format": {"standalone": True, "documentclass": "ctexart",
                   "classoption": "fontset=fandol", "fontsize": "10pt", "margin": "16mm"},
        "shared_configuration_sha256": config_hashes,
        "sections": len(records), "passed_sections": len(records) - len(failed),
        "failed_sections": failed, "errors": errors,
        "mathematics": {
            "method": "Compare every Pandoc AST Math node with every exported TeX inline/display math fragment, in exact sequence and with math type preserved.",
            "normalization": ["Ignore whitespace", "Ignore layout-only \\allowbreak"],
            "all_math_sequences_match": not failed and not errors,
            "source_math_nodes": sum(r.get("math_check", {}).get("source_math_nodes", 0) for r in records),
            "exported_math_fragments": sum(r.get("math_check", {}).get("exported_math_fragments", 0) for r in records),
            "scope_note": "Chapter and subsection files overlap; this is an export fidelity total, not a count of unique textbook formulas.",
            "correctness": "Mathematical correctness is not established by this export comparison.",
        },
        "image_path_policy": "Image paths are preserved relative to verified/sections; run xelatex from that directory.",
        "representative_compile_review": representative_review,
        "exports": records,
    }
    REPORT.parent.mkdir(exist_ok=True)
    atomic_text(REPORT, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "sections", "passed_sections", "failed_sections", "errors", "mathematics")},
                     ensure_ascii=False), flush=True)
    if report["status"] == "pass" and args.compile_all:
        return compile_all_sections(records, args.jobs)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
