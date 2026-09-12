"""Agent checks supporting, but never replacing, visual page review."""
import hashlib
import json
import math
import re
from pathlib import Path

LANE = Path(__file__).resolve().parent
BOOK = LANE.parent.parent
review = json.loads((LANE / 'review.json').read_text())
assert [p['pdf_page'] for p in review['pages']] == list(range(261, 276))
all_tags = []
matrix_count = 0

def sign_matrices(text):
    out = []
    for body in re.findall(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', text, re.S):
        if not re.fullmatch(r'[+\-\s&\\]+', body):
            continue
        rows = [[1 if x.strip() == '+' else -1 for x in row.strip().split('&')]
                for row in body.strip().split('\\\\') if row.strip()]
        assert rows and len({len(row) for row in rows}) == 1
        assert len(rows) == len(rows[0])
        out.append(rows)
    return out

for p in review['pages']:
    path = BOOK / p['path']
    text = path.read_text()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == p['sha256']
    image_path = BOOK / f"source-images/pdf-{p['pdf_page']}.jpeg"
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == p['source_image_sha256']
    assert f"pdf_page: {p['pdf_page']}\n" in text
    assert f"printed_page: {p['printed_page']}\n" in text
    assert f"<!-- source-page: {p['pdf_page']} -->" in text
    assert text.count('$$') % 2 == 0
    assert len(re.findall(r'(?<!\\)\$', text.replace('$$', ''))) % 2 == 0
    assert '[待核:' not in text
    for target in re.findall(r'\]\(([^)]+)\)', text):
        assert (path.parent / target).resolve().exists(), (path, target)
    stack = []
    for op, env in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
        if op == 'begin':
            stack.append(env)
        else:
            assert stack and stack.pop() == env, (path, env)
    assert not stack
    all_tags.extend(re.findall(r'\\tag\{([^}]+)\}', text))
    matrix_count += len(sign_matrices(text))

assert all_tags == ['10.3.1', '10.4.1', '10.4.2', '10.4.3', '10.4.4']
assert [f for p in review['pages'] for f in p['figures']] == [f'10.{i}' for i in range(1, 10)]
assert [t for p in review['pages'] for t in p['tables']] == ['10.1']
assert '\\*第 10 章' in (LANE / 'pages/pdf-261.md').read_text()

W = [[1]]
H = [[1]]
generated_w, generated_h = {}, {}
for n in (2, 4, 8):
    W = [new for row in W for new in (row + row[::-1], row + [-x for x in row[::-1]])]
    H = [row + row for row in H] + [row + [-x for x in row] for row in H]
    generated_w[n] = W
    generated_h[n] = H
for mat in sign_matrices((LANE / 'pages/pdf-265.md').read_text()):
    assert mat == generated_w[len(mat)]
for mat in sign_matrices((LANE / 'pages/pdf-267.md').read_text()):
    assert mat == generated_w[len(mat)]
for mat in sign_matrices((LANE / 'pages/pdf-269.md').read_text()):
    assert mat == generated_h[len(mat)]

for n, mat in generated_w.items():
    for i, row in enumerate(mat):
        sampled = []
        for j in range(n):
            x = (j + 0.5) / n
            val = 1
            for r in range(int(math.log2(n))):
                val *= 1 if math.cos(((i >> r) & 1) * (2**r) * math.pi * x) >= 0 else -1
            sampled.append(val)
        assert sampled == row
for n, mat in generated_h.items():
    for i in range(n):
        for j in range(n):
            assert sum(mat[k][i] * mat[k][j] for k in range(n)) == (n if i == j else 0)

# The source's range 1..2^k is preserved in the transcription.
# Test the separately annotated range 1..2^(k-1) against each basis vector.
for n in (2, 4, 8):
    for q in range(n):
        original = [int(i == q) for i in range(n)]
        x = original[:]
        for k in range(1, int(math.log2(n)) + 1):
            prev, half = n // 2**(k-1), n // 2**k
            out = [None] * n
            for l in range(1, 2**(k-1) + 1):
                for j in range(half):
                    a = (l-1) * prev + j
                    b = a + half
                    out[a], out[b] = x[a] + x[b], x[a] - x[b]
            assert None not in out
            x = out
        assert x == [row[q] for row in generated_h[n]]
source_counterexample = {'N': 8, 'k': 1, 'l': 2, 'j': 0,
                         'first_accessed_index': 8, 'valid_max_index': 7}
result = {
    'status': 'passed', 'human_review': False,
    'reviewed_pdf_pages': list(range(261, 276)),
    'file_and_source_image_hashes_checked': 15,
    'formula_ids': all_tags, 'figure_count': 9, 'table_count': 1,
    'sign_matrix_instances_checked_for_square_shape': matrix_count,
    'matrix_checks': 'Transcribed W2/W4/W8 and H2/H4/H8 agree with the source mirror/block recurrences; Walsh cosine-product midpoint samples agree; H^T H = N I.',
    'algorithm_check': 'The separately annotated l bound 2^(k-1) produces all basis-vector Hadamard transforms for N=2,4,8. No source formulas were silently changed.',
    'source_range_counterexample': source_counterexample,
    'limitations': 'Structural and algebraic checks support agent visual review; no claim of human review or absolute absence of transcription errors.'
}
(LANE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
