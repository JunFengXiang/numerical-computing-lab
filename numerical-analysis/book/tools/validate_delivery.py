#!/usr/bin/env python3
"""Validate the current full-book delivery, without modifying its source files.

Run from any directory with Python + PyYAML + PyMuPDF.  The only output is
quality/delivery-checks.json.  Exit 0 means structural delivery checks passed;
it does not certify the mathematics or replace the named agents' visual work.
Legacy six-section aliases in verified/ are deliberately not canonical inputs.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import re

import fitz
import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2"
EXPECTED = {"source_pages": 322, "sections": 275, "formulas": 542, "lanes": 21}
FRONT_EXCEPTION = "front-toc-ch7-exercises-page-damage"
TAG = re.compile(r"\\tag\s*\{([^}]+)\}")
PAGE_MARKER = re.compile(r"<!--\s*source-page:\s*(\d+)\s*-->")


def frontmatter(raw):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", raw, re.S)
    if not match:
        raise ValueError("missing YAML front matter")
    meta = yaml.safe_load(match[1])
    if not isinstance(meta, dict):
        raise ValueError("YAML front matter is not an object")
    return meta, raw[match.end():]


def integer_pages(value):
    if not isinstance(value, list) or any(type(n) is not int for n in value):
        raise ValueError("page list must contain integers, not strings or booleans")
    return value


def owning_pages(record):
    """related_pdf_page(s) describe evidence, not ownership (root decision)."""
    pages = list(integer_pages(record.get("pdf_pages", [])))
    if record.get("pdf_page") is not None:
        if type(record["pdf_page"]) is not int:
            raise ValueError("pdf_page must be an integer")
        pages.append(record["pdf_page"])
    return set(pages)


def visible_id(body, identifier):
    """YAML is removed by the caller; invisible HTML comments do not count."""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return bool(re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(identifier)
                          + r"(?![A-Za-z0-9_.-])", body))


def tagged_formulas(body):
    for match in re.finditer(r"(?<!\\)\$\$(.*?)(?<!\\)\$\$", body, re.S):
        block = match[1].strip()
        for tag in TAG.findall(block):
            yield tag.strip(), block


def annotation_blocks(body):
    """Read marked note headings and contiguous quote blocks independently."""
    lines = body.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if re.match(r"^#{1,6}\s+.*(?:校注|原书疑误)", lines[i]):
            end = i + 1
            while end < len(lines) and not re.match(r"^#{1,6}\s+", lines[end]):
                end += 1
            yield "".join(lines[i:end]).strip()
            i = end
        elif lines[i].startswith(">"):
            end = i + 1
            while end < len(lines) and lines[end].startswith(">"):
                end += 1
            block = "".join(lines[i:end]).strip()
            if "校注" in block or "原书疑误" in block:
                yield block
            i = end
        else:
            i += 1


def comparable_note(text):
    # Relative link destinations change between page and section directories.
    text = re.sub(r"(!?\[[^\]\n]*\])\([^\n]*?\)", r"\1(<link>)", text)
    return re.sub(r"\s+", " ", text).strip()


class DeliveryAudit:
    def __init__(self, root):
        self.root = root.resolve()
        self.errors = []
        self.groups = {}
        self.group = "inputs"
        self.cache = {}
        self.snapshots = {}
        self.counts = Counter()
        self.page_results = []
        self.section_results = []
        self.lane_results = []
        self.canonical = {}
        self.section_bodies = {}
        self.primary_errata = []
        self.exceptions = []

    def check(self, condition, code, message, **where):
        group = self.groups.setdefault(self.group, {"checks": 0, "failures": 0})
        group["checks"] += 1
        if not condition:
            group["failures"] += 1
            self.errors.append({"group": self.group, "code": code,
                                "message": message, **where})
        return bool(condition)

    def path(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("missing file path")
        path = (self.root / value).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("file path leaves the book directory: " + value)
        return path

    def digest(self, path):
        path = Path(path)
        if path not in self.snapshots:
            h = sha256()
            with path.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    h.update(block)
            self.snapshots[path] = h.hexdigest()
        return self.snapshots[path]

    def text(self, value):
        path = self.path(value)
        if path not in self.cache:
            data = path.read_bytes()
            self.snapshots[path] = sha256(data).hexdigest()
            self.cache[path] = data.decode("utf-8")
        return self.cache[path]

    def document(self, value):
        return json.loads(self.text(value))

    def markdown(self, value):
        return frontmatter(self.text(value))

    def keyed(self, rows, key, label):
        if not isinstance(rows, list):
            raise ValueError(label + " must be a list")
        result = {}
        for row in rows:
            if not isinstance(row, dict) or key not in row:
                self.check(False, "invalid_record", label + " has an invalid record")
                continue
            value = row[key]
            if self.check(value not in result, "duplicate_record",
                          label + " has a duplicate key", key=str(value)):
                result[value] = row
        return result

    def source(self):
        self.manifest = self.document("source-manifest.json")
        self.review = self.document("quality/pages-review.json")
        self.sections_doc = self.document("index/sections.json")
        self.formulas_doc = self.document("index/formulas.json")
        self.errata_doc = self.document("quality/source-errata.json")
        self.lanes = self.document("workflow/lanes.json")
        self.pages = self.keyed(self.review["pages"], "pdf_page", "page review")
        self.sections = self.keyed(self.sections_doc["entries"], "id", "sections")
        self.formulas = self.keyed(self.formulas_doc["formulas"], "id", "formulas")
        self.errata = self.keyed(self.errata_doc["source_errata"], "id", "source errata")
        self.source_images = self.keyed(self.manifest["pages"], "pdf_page", "source images")
        for label, doc in [("source manifest", self.manifest), ("page review", self.review),
                           ("source errata", self.errata_doc)]:
            self.check(doc.get("source_sha256") == SOURCE_SHA256, "source_receipt_sha",
                       label + " has the wrong source PDF SHA-256")
        path = self.path(self.manifest["source_file"])
        self.check(self.digest(path) == SOURCE_SHA256, "source_pdf_sha", "source PDF bytes changed")
        self.check(path.stat().st_size == self.manifest.get("source_bytes"), "source_pdf_size",
                   "source PDF byte count differs from manifest")
        with fitz.open(path) as pdf:
            count = len(pdf)
        self.counts["source_pdf_pages"] = count
        self.check(count == EXPECTED["source_pages"] == self.manifest.get("source_pdf_pages"),
                   "source_pdf_pages", "source PDF must contain 322 pages")
        self.check(set(self.pages) == set(range(1, 323)), "page_coverage",
                   "page review must cover each page 1–322 exactly once")
        self.check(set(self.source_images) == set(range(1, 323)), "image_coverage",
                   "source-image manifest must cover pages 1–322")
        self.check(self.review.get("complete_source_page_coverage") is True,
                   "page_review_status", "full source-page coverage is not confirmed")
        self.check(self.review.get("human_review") is False, "review_attribution",
                   "agent page review must not be labeled human review")

    def page_receipts(self):
        lane_map = self.keyed(self.lanes, "lane", "lane plan")
        self.check(len(lane_map) == EXPECTED["lanes"], "lane_count", "expected 21 lanes")
        planned = []
        for name, lane in lane_map.items():
            before = len(self.errors)
            try:
                expected = set(range(lane["start"], lane["end"] + 1))
                planned.extend(expected)
                primary_path = f"staging/{name}/review.json"
                cross_path = f"staging/{name}/cross-review.json"
                primary = self.document(primary_path)
                cross = self.document(cross_path)
                pp = self.keyed(primary["pages"], "pdf_page", name + " primary")
                cp = self.keyed(cross["pages"], "pdf_page", name + " cross review")
                self.check(set(pp) == expected == set(cp), "receipt_page_coverage",
                           "primary/cross page sets differ from lane plan", lane=name)
                self.check(primary.get("lane") == cross.get("lane") == name,
                           "receipt_lane", "review receipt lane mismatch", lane=name)
                self.check(primary.get("source_sha256") == SOURCE_SHA256,
                           "primary_source_sha", "primary receipt source SHA mismatch", lane=name)
                self.check(primary.get("human_review") is False and cross.get("human_review") is False,
                           "review_attribution", "both reviews must be attributed to agents", lane=name)
                self.check(not primary.get("unresolved") and not cross.get("unresolved"),
                           "unresolved_review", "review has unresolved issues", lane=name)
                self.check(cross.get("status") == "pass", "cross_status",
                           "cross review has not passed", lane=name)
                self.check(bool(primary.get("reviewer")) and bool(cross.get("reviewer"))
                           and primary.get("reviewer") != cross.get("reviewer"),
                           "independent_reviewer", "cross reviewer is not independently named", lane=name)
                self.primary_errata.extend({**item, "lane": name}
                                           for item in primary.get("source_errata", []))
                for n in sorted(expected):
                    page_before = len(self.errors)
                    try:
                        row, pr, cr = self.pages[n], pp[n], cp[n]
                        staging = f"staging/{name}/pages/pdf-{n:03d}.md"
                        canonical = f"verified/pages/pdf-{n:03d}.md"
                        self.check(row.get("lane") == name and row.get("path") == staging
                                   and pr.get("path") == staging and row.get("canonical_path") == canonical,
                                   "page_paths", "page is not mapped to its canonical/primary path", pdf_page=n)
                        self.check(row.get("primary_review") == primary_path
                                   and row.get("cross_review") == cross_path,
                                   "page_review_paths", "page review pointers mismatch", pdf_page=n)
                        sm, sb = self.markdown(staging)
                        cm, cb = self.markdown(canonical)
                        sh, ch = self.digest(self.path(staging)), self.digest(self.path(canonical))
                        self.canonical[n] = (cm, cb, canonical)
                        self.check(sh == row.get("sha256") == pr.get("sha256") == cr.get("sha256"),
                                   "primary_cross_sha", "current MD/primary/cross SHA mismatch", pdf_page=n)
                        self.check(ch == row.get("canonical_sha256"), "canonical_sha",
                                   "canonical Markdown SHA is stale", pdf_page=n)
                        self.check(row.get("pass") is True and pr.get("visual_review") == "completed"
                                   and pr.get("content_coverage") == "complete"
                                   and cr.get("source_visual_review") == "completed",
                                   "page_review_status", "page lacks complete named visual review", pdf_page=n)
                        for label, meta in [("primary", sm), ("canonical", cm)]:
                            self.check(meta.get("pdf_page") == n and
                                       meta.get("printed_page") == row.get("printed_page") == pr.get("printed_page"),
                                       "page_metadata", label + " metadata page numbers disagree", pdf_page=n)
                            self.check(meta.get("source_sha256") == SOURCE_SHA256 and
                                       meta.get("source_image") == self.source_images[n]["image"],
                                       "page_source_metadata", label + " source metadata mismatch", pdf_page=n)
                        self.check(cm.get("primary_transcription") == staging and
                                   cm.get("status") == "independently_agent_verified_transcription",
                                   "canonical_provenance", "canonical provenance/status mismatch", pdf_page=n)
                        self.check(n in [int(v) for v in PAGE_MARKER.findall(cb)], "page_marker",
                                   "canonical source-page marker missing", pdf_page=n)
                        image = self.source_images[n]
                        self.check(self.digest(self.path(image["image"])) == image["image_sha256"]
                                   == pr.get("source_image_sha256"), "source_image_sha",
                                   "source image or image receipt hash mismatch", pdf_page=n)
                        tags = [tag for tag, _ in tagged_formulas(cb)]
                        self.check(Counter(tags) == Counter(pr.get("formula_ids", []))
                                   == Counter(row.get("formula_ids", [])), "page_formula_receipt",
                                   "canonical formula IDs differ from page review", pdf_page=n)
                        self.page_results.append({"pdf_page": n, "lane": name,
                                                  "canonical_sha256": ch, "primary_sha256": sh,
                                                  "status": "pass" if len(self.errors) == page_before else "fail"})
                    except (OSError, ValueError, KeyError, TypeError) as exc:
                        self.check(False, "page_unreadable", str(exc), lane=name, pdf_page=n)
                self.counts["primary_cross_lanes_passed"] += len(self.errors) == before
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.check(False, "lane_receipt_unreadable", str(exc), lane=name)
        self.check(Counter(planned) == Counter(range(1, 323)), "lane_plan_coverage",
                   "lane plan must cover all 322 pages once")
        self.counts["canonical_pages_checked"] = len(self.page_results)
        self.counts["canonical_pages_passed"] = sum(p["status"] == "pass" for p in self.page_results)
        actual = {p.name for p in (self.root / "verified/pages").glob("pdf-*.md")}
        self.check(actual == {f"pdf-{n:03d}.md" for n in range(1, 323)},
                   "canonical_directory_coverage", "canonical page directory has missing/extra page files")

    def section_files(self):
        self.check(len(self.sections) == EXPECTED["sections"], "section_count", "expected 275 indexed sections")
        for sid, entry in self.sections.items():
            before = len(self.errors)
            try:
                path = entry["verified_markdown"]
                tex_path = entry["verified_latex"]
                self.check(path == f"verified/sections/{sid}.md" and tex_path == f"verified/sections/{sid}.tex",
                           "section_paths", "section must use full-delivery paths, not legacy subset aliases", section_id=sid)
                meta, body = self.markdown(path)
                self.section_bodies[sid] = body
                pages = integer_pages(entry["pdf_pages"])
                printed = [self.pages[n].get("printed_page") for n in pages]
                self.check(bool(pages) and pages == sorted(set(pages)), "section_page_list",
                           "section PDF pages must be nonempty, ordered and unique", section_id=sid)
                self.check(str(meta.get("section_id")) == sid and meta.get("title") == entry.get("title"),
                           "section_metadata_identity", "section ID/title metadata mismatch", section_id=sid)
                self.check(meta.get("pdf_pages") == pages and meta.get("printed_pages") == printed
                           == entry.get("printed_pages"), "section_page_metadata",
                           "section metadata/index/canonical printed pages disagree", section_id=sid)
                self.check(entry.get("pdf_page_start_hint") == pages[0]
                           and entry.get("printed_page_start") == printed[0], "section_start_page",
                           "section locator start differs from covered page metadata", section_id=sid)
                self.check(set(map(int, PAGE_MARKER.findall(body))) == set(pages), "section_page_markers",
                           "section source-page markers do not match indexed pages", section_id=sid)
                self.check(meta.get("source_sha256") == SOURCE_SHA256
                           and meta.get("status") == "independently_agent_verified_transcription",
                           "section_provenance", "section provenance/status mismatch", section_id=sid)
                md_sha = self.digest(self.path(path))
                self.check(md_sha == entry.get("markdown_sha256"), "section_sha",
                           "section Markdown/index SHA mismatch", section_id=sid)
                tex = self.text(tex_path)
                self.check(bool(tex.strip()), "section_tex_empty", "section TeX is empty", section_id=sid)
                tex_body = tex.partition(r"\begin{document}")[2]
                self.check(bool(tex_body) and r"\end{document}" in tex_body, "section_tex_document",
                           "section TeX has no complete standalone document", section_id=sid)
                self.check(Counter(TAG.findall(tex_body)) == Counter(tag for tag, _ in tagged_formulas(body)),
                           "section_tex_formula_tags", "section TeX lost or duplicated numbered formula tags", section_id=sid)
                for eid in entry.get("source_errata", []):
                    self.check(visible_id(tex_body.replace(r"\_", "_"), eid), "section_tex_erratum_id",
                               "corresponding section TeX lacks an indexed erratum ID", section_id=sid, erratum_id=eid)
                self.counts["section_tex_present"] += 1
                self.section_results.append({"section_id": sid, "pdf_pages": pages,
                    "markdown_sha256": md_sha, "latex_sha256": self.digest(self.path(tex_path)),
                    "status": "pass" if len(self.errors) == before else "fail"})
            except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
                self.check(False, "section_unreadable", str(exc), section_id=sid)
        self.counts["section_markdown_present"] = len(self.section_bodies)
        self.counts["sections_passed"] = sum(s["status"] == "pass" for s in self.section_results)

    def section_errata(self):
        primary = self.keyed(self.primary_errata, "id", "primary source errata")
        self.check(set(primary) == set(self.errata), "errata_catalog_ids",
                   "global errata IDs do not match current primary receipts")
        for eid, item in self.errata.items():
            self.check(item == primary.get(eid), "errata_catalog_record",
                       "global erratum record differs from primary receipt", erratum_id=eid)
        mapped = set()
        for sid, entry in self.sections.items():
            try:
                pages = set(integer_pages(entry["pdf_pages"]))
                expected = {eid for eid, item in self.errata.items() if owning_pages(item) & pages}
                indexed = entry.get("source_errata", [])
                adjacent = [r["id"] for r in entry.get("adjacent_source_errata", [])]
                self.check(set(indexed) == expected and len(indexed) == len(expected)
                           and set(adjacent) == expected and len(adjacent) == len(expected),
                           "section_errata_index", "section errata do not cover every owned source page", section_id=sid)
                meta, body = self.markdown(entry["verified_markdown"])
                self.check(meta.get("source_errata") == indexed, "section_errata_metadata",
                           "section errata metadata differs from index", section_id=sid)
                for eid in sorted(expected):
                    self.counts["section_errata_links_checked"] += 1
                    found = visible_id(body, eid)
                    self.check(found, "section_erratum_id_missing",
                               "erratum ID is absent from readable section text (YAML/comments excluded)",
                               section_id=sid, erratum_id=eid)
                    if found:
                        mapped.add(eid)
                normalized = comparable_note(body)
                for n in sorted(pages):
                    _, page_body, _ = self.canonical[n]
                    blocks = list(annotation_blocks(page_body))
                    page_errata = [eid for eid, item in self.errata.items() if n in owning_pages(item)]
                    self.check(not page_errata or bool(blocks), "source_errata_note_missing",
                               "source errata record has no extractable marked page note", section_id=sid, pdf_page=n)
                    for number, block in enumerate(blocks, 1):
                        self.counts["section_page_notes_checked"] += 1
                        self.check(comparable_note(block) in normalized, "section_page_note_missing",
                                   "a complete marked source-page note is absent from section/body appendix",
                                   section_id=sid, pdf_page=n, note_block=number)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.check(False, "section_errata_unreadable", str(exc), section_id=sid)
        # Explicitly authorized exception: the damaged printed TOC is not a body section.
        exception = self.errata.get(FRONT_EXCEPTION)
        if exception:
            _, body, _ = self.canonical[11]
            exercise = self.sections.get("7.exercises", {})
            preserved = (owning_pages(exception) == {11}
                         and "扫描残损" in body and "末位可辨为 8" in body
                         and bool(re.search(r"PDF\s*第?\s*212\s*页", body))
                         and "书页 199" in body and exercise.get("pdf_page_start_hint") == 212
                         and exercise.get("printed_pages", [None])[0] == 199
                         and bool(re.search(r"^#{1,6}\s+习题\s*$", self.canonical[212][1], re.M)))
            self.check(preserved, "front_toc_exception", "authorized TOC exception has lost its damage/locator evidence")
            if preserved:
                mapped.add(FRONT_EXCEPTION)
                self.exceptions.append({"id": FRONT_EXCEPTION, "pdf_page": 11,
                    "reason": "root explicitly exempts the printed-TOC damage from 275 body sections; canonical damage text and PDF212/book199 locator are checked"})
        self.check(mapped == set(self.errata), "unmapped_errata",
                   "errata without readable section text or an approved canonical-only exception",
                   missing_ids=sorted(set(self.errata) - mapped))
        self.counts["source_errata_records"] = len(self.errata)
        self.counts["source_errata_mapped"] = len(mapped)

    def formula_locations(self):
        self.check(len(self.formulas) == EXPECTED["formulas"], "formula_count", "expected 542 numbered formulas")
        actual = {}
        for n, (_, body, path) in self.canonical.items():
            for tag, block in tagged_formulas(body):
                actual.setdefault(tag, []).append((n, path, block))
        self.check(set(actual) == set(self.formulas), "formula_id_coverage",
                   "formula index and actual canonical display tags differ",
                   missing_ids=sorted(set(actual) - set(self.formulas)),
                   nonexistent_ids=sorted(set(self.formulas) - set(actual)))
        self.check(sum(map(len, actual.values())) == EXPECTED["formulas"], "actual_formula_count",
                   "canonical pages do not have exactly 542 numbered formula occurrences")
        for fid, item in self.formulas.items():
            try:
                found = actual.get(fid, [])
                declared = integer_pages(item["source_pdf_pages"])
                self.check(len(found) == 1 and declared == [p[0] for p in found], "formula_source_page",
                           "numbered formula is missing, duplicated, or indexed on the wrong page", formula_id=fid)
                self.check(bool(found) and item.get("markdown") == found[0][1]
                           and item.get("latex", "").strip() == found[0][2], "formula_source_text",
                           "formula path or actual LaTeX block differs from index", formula_id=fid)
                sid = item.get("section_id")
                self.check(sid in self.sections and set(declared) <= set(self.sections[sid]["pdf_pages"])
                           and fid in [tag for tag, _ in tagged_formulas(self.section_bodies.get(sid, ""))],
                           "formula_section", "formula is absent from its indexed section", formula_id=fid, section_id=sid)
            except (ValueError, KeyError, TypeError) as exc:
                self.check(False, "formula_unreadable", str(exc), formula_id=fid)
        self.counts["numbered_formula_records"] = len(self.formulas)
        self.counts["actual_numbered_formulas"] = sum(map(len, actual.values()))

    def latex_lanes(self):
        expected_names = {lane["lane"] for lane in self.lanes}
        directory = self.root / "quality/latex-lanes"
        actual_names = {p.stem for p in directory.glob("*.json") if not p.stem.endswith("-visual")}
        self.check(actual_names == expected_names and len(actual_names) == EXPECTED["lanes"],
                   "latex_lane_coverage", "expected exactly 21 compilation receipts")
        for lane in self.lanes:
            name = lane["lane"]
            before = len(self.errors)
            try:
                compiled = self.document(f"quality/latex-lanes/{name}.json")
                visual = self.document(f"quality/latex-lanes/{name}-visual.json")
                self.check(compiled.get("lane") == visual.get("lane") == name, "latex_lane_identity",
                           "compilation/visual lane identity mismatch", lane=name)
                self.check(compiled.get("status") == "compiled", "latex_compile_status",
                           "lane has no successful compilation receipt", lane=name)
                pdf_path = self.path(compiled["pdf"])
                pdf_sha = self.digest(pdf_path)
                self.check(pdf_sha == compiled.get("pdf_sha256") == visual.get("pdf_sha256"),
                           "latex_pdf_sha", "current PDF/compilation/visual SHA mismatch", lane=name)
                self.check(self.digest(self.path(compiled["standalone_tex"])) == compiled.get("tex_sha256"),
                           "latex_tex_sha", "compiled TeX hash is stale", lane=name)
                with fitz.open(pdf_path) as pdf:
                    count = len(pdf)
                self.check(count == compiled.get("rendered_pages"), "latex_pdf_page_count",
                           "actual PDF page count differs from compilation receipt", lane=name)
                reviewed = integer_pages(visual.get("rendered_pages_reviewed"))
                self.check(visual.get("status") == "pass" and not visual.get("issues")
                           and bool(visual.get("reviewer")), "latex_visual_status",
                           "visual review is not a named pass with no open issues", lane=name)
                self.check(Counter(reviewed) == Counter(range(1, count + 1)), "latex_visual_pages",
                           "visual review does not cover every rendered page exactly once", lane=name)
                sources = self.keyed(compiled["sources"], "pdf_page", name + " compiled sources")
                self.check(set(sources) == set(range(lane["start"], lane["end"] + 1)), "latex_source_coverage",
                           "compiled source set differs from lane plan", lane=name)
                for n, source in sources.items():
                    self.check(source.get("markdown") == self.pages[n]["path"]
                               and self.digest(self.path(source["markdown"])) == source.get("sha256")
                               == self.pages[n]["sha256"], "latex_source_sha",
                               "compiled source Markdown hash is stale", lane=name, pdf_page=n)
                self.lane_results.append({"lane": name, "pdf_sha256": pdf_sha,
                                          "rendered_pages": count,
                                          "status": "pass" if len(self.errors) == before else "fail"})
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.check(False, "latex_receipt_unreadable", str(exc), lane=name)
        self.counts["latex_lanes_checked"] = len(self.lane_results)
        self.counts["latex_lanes_passed"] = sum(l["status"] == "pass" for l in self.lane_results)

    def stable_snapshot(self):
        # Refuse a pass if the main task regenerated any checked input mid-run.
        for path, expected in self.snapshots.items():
            try:
                h = sha256()
                with path.open("rb") as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b""):
                        h.update(block)
                self.check(h.hexdigest() == expected, "input_changed_during_validation",
                           "checked input changed during validation", path=str(path.relative_to(self.root)))
            except OSError as exc:
                self.check(False, "input_disappeared", str(exc), path=str(path.relative_to(self.root)))

    def run(self):
        stages = [("source", self.source), ("pages", self.page_receipts),
                  ("sections", self.section_files), ("section_errata", self.section_errata),
                  ("formulas", self.formula_locations), ("latex_lanes", self.latex_lanes),
                  ("snapshot", self.stable_snapshot)]
        for name, work in stages:
            self.group = name
            try:
                work()
            except Exception as exc:
                self.check(False, "validation_stage_error", type(exc).__name__ + ": " + str(exc))
        for group in self.groups.values():
            group["status"] = "pass" if not group["failures"] else "fail"
        return {"updated_utc": datetime.now(timezone.utc).isoformat(),
                "validator": "tools/validate_delivery.py", "status": "fail" if self.errors else "pass",
                "scope": "current-file integrity and receipt coverage; not a new visual or mathematical review",
                "human_review": False, "source_sha256": SOURCE_SHA256,
                "expected_counts": EXPECTED, "counts": dict(self.counts),
                "checks": self.groups, "errors": self.errors, "approved_exceptions": self.exceptions,
                "legacy_subset_aliases": "ignored: only index entries under verified/sections are canonical",
                "pages": self.page_results, "sections": self.section_results, "latex_lanes": self.lane_results,
                "input_sha256": {str(p.relative_to(self.root)): h for p, h in sorted(self.snapshots.items())}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="book root; defaults to script parent")
    args = parser.parse_args()
    audit = DeliveryAudit(args.root)
    result = audit.run()
    output = args.root / "quality/delivery-checks.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"],
                      "error_count": len(result["errors"]), "report": str(output.resolve())}, ensure_ascii=False))
    for error in result["errors"]:
        print(json.dumps(error, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
