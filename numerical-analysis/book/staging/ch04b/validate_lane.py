"""Read-only checks of lane transcriptions; writes only lane-local QA artifacts."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

import sympy as sp
import yaml

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[1]
QA = LANE / "validation"
QA.mkdir(exist_ok=True)
SOURCE_SHA256 = "0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2"
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()

review = json.loads((LANE / "review.json").read_text())
assert [p["pdf_page"] for p in review["pages"]] == list(range(106, 119))
source_pdf = next(ROOT.glob("*.pdf"))
assert sha(source_pdf) == SOURCE_SHA256

checks = []
formulas = []
tags = []
tex = [
    r"\documentclass[11pt]{article}",
    r"\usepackage{amsmath,amssymb}",
    r"\usepackage[a4paper,margin=22mm]{geometry}",
    r"\begin{document}",
]
for record in review["pages"]:
    page = record["pdf_page"]
    path = ROOT / record["path"]
    raw = path.read_text()
    metadata_match = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    assert metadata_match, path
    metadata = yaml.safe_load(metadata_match.group(1))
    body = raw[metadata_match.end():]
    assert metadata["pdf_page"] == page
    assert metadata["printed_page"] == page - 13
    assert metadata["source_sha256"] == SOURCE_SHA256
    assert metadata["status"] == "agent_reviewed_transcription"
    assert sha(path) == record["sha256"]
    image = ROOT / metadata["source_image"]
    assert sha(image) == record["source_image_sha256"]
    assert f"<!-- source-page: {page} -->" in body
    assert "[待核:" not in body
    assert body.count("$$") % 2 == 0
    assert body.replace("$$", "").count("$") % 2 == 0
    for target in re.findall(r"\]\(([^)]+)\)", body):
        assert (path.parent / target).resolve().is_file(), (path, target)
    page_tags = re.findall(r"\\tag\{([^}]+)\}", body)
    assert page_tags == record["formula_ids"]
    tags.extend(page_tags)
    tex.extend([r"\clearpage", rf"\section*{{Source PDF page {page}}}"])
    math_count = 0
    for match in re.finditer(r"\$\$(.*?)\$\$|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$", body, re.S):
        display, inline = match.groups()
        expression = display if display is not None else inline
        assert expression is not None
        # Account for literal escaped braces separately from grouping braces.
        braces = re.sub(r"\\[{}]", "", expression)
        depth = 0
        for char in braces:
            depth += (char == "{") - (char == "}")
            assert depth >= 0, (path, expression)
        assert depth == 0, (path, expression)
        math_count += 1
        tex.append(rf"\noindent Formula {page}.{math_count}:\par")
        tex.append(r"\[" + expression + r"\]" if display is not None else "$" + expression + "$\\par")
        formulas.append({"pdf_page": page, "sequence": math_count, "display": display is not None})
    checks.append({"pdf_page": page, "metadata_hash_links_math_delimiters": "passed", "math_expressions": math_count})

assert len(tags) == len(set(tags)), "Repeated formula tags within lane"
tex.append(r"\end{document}")
(QA / "math-syntax.tex").write_text("\n".join(tex) + "\n")

# Check the printed five-point coefficients against independently differentiated
# polynomials. This is supplemental evidence, not a substitute for source review.
t = sp.symbols("t")
first = [[-25,48,-36,16,-3],[-3,-10,18,-6,1],[1,-8,0,8,-1],[-1,6,-18,10,3],[3,-16,36,-48,25]]
second = [[35,-104,114,-56,11],[11,-20,6,4,-1],[-1,16,-30,16,-1],[-1,4,6,-20,11],[11,-56,114,-104,35]]
moments = []
for order, rows in ((1, first), (2, second)):
    for node, row in enumerate(rows):
        for degree in range(5):
            value = sum(sp.Rational(c,12)*(t**degree).subs(t,j) for j,c in enumerate(row))
            target = sp.diff(t**degree,t,order).subs(t,node)
            assert sp.simplify(value-target) == 0
        moments.append({"derivative_order":order,"node":node,"degrees_0_through_4":"passed"})

run = subprocess.run(
    ["/Library/TeX/texbin/xelatex", "-interaction=nonstopmode", "-halt-on-error", "math-syntax.tex"],
    cwd=QA, text=True, capture_output=True,
)
(QA / "math-syntax-build.stdout.txt").write_text(run.stdout + run.stderr)
assert run.returncode == 0, "Math syntax compilation failed; inspect lane validation log"
log = (QA / "math-syntax.log").read_text()
warnings = [line for line in log.splitlines() if "Overfull \\hbox" in line or "Missing character:" in line]
result = {
    "lane": "ch04b", "source_pdf_sha256_verified": SOURCE_SHA256,
    "page_count": len(checks), "checks": checks, "numbered_formula_count":len(tags),
    "numbered_formula_ids": tags, "math_expression_count":len(formulas),
    "fivepoint_polynomial_checks":moments,
    "latex_math_syntax_compile":"passed", "latex_layout_warnings":warnings,
    "scope_note":"Supplemental structural, file integrity, formula syntax and coefficient checks; original-page agent visual review remains the transcription evidence. No exercise answers were generated.",
}
(QA / "validation-report.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ("page_count","numbered_formula_count","math_expression_count","latex_math_syntax_compile","latex_layout_warnings")},ensure_ascii=False,indent=2))
