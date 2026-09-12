#!/usr/bin/env python3
"""Read and parse the actual transcribed LaTeX; never substitute hand-coded formulas."""
from pathlib import Path
import re
import sympy as sp
from sympy.parsing.latex import parse_latex

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'verified' / 'sections' / '2.2.2.md'


def math_blocks(text):
    return re.findall(r'\$\$(.*?)\$\$', text, flags=re.S)


def tagged(blocks, number):
    matches = [b for b in blocks if r'\tag{'+number+'}' in b]
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one equation {number}; got {len(matches)}.')
    return matches[0]


def parse_rhs(latex, mapping):
    """Only the short explicitly selected algebraic equations are accepted here."""
    expr = latex.split('=', 1)[1]
    expr = re.sub(r'\\tag\{[^}]+\}', '', expr)
    expr = expr.split(r'\quad\text', 1)[0]
    expr = expr.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '')
    expr = expr.replace('&', '').replace(r'\\', ' ')
    expr = expr.replace('{}', '')  # Empty alignment atom in ={} adds spacing only.
    expr = expr.strip().rstrip(',.')
    for old, new in sorted(mapping.items(), key=lambda x: -len(x[0])):
        expr = expr.replace(old, new)
    return parse_latex(expr, strict=True)


def load_linear():
    blocks = math_blocks(SOURCE.read_text())
    mapping = {r'l_{k+1}(x)': 'q', r'l_k(x)': 'p',
               r'x_{k+1}': 'b', r'x_k': 'a',
               r'y_{k+1}': 'v', r'y_k': 'u'}
    basis_block = next(b for b in blocks
                       if b.strip().startswith('l_k(x)=') and r'\frac' in b
                       and r'x_{k-1}' not in b)
    basis_parts = basis_block.split(r'\qquad')
    if len(basis_parts) != 2:
        raise ValueError('Expected two linear basis formulas.')
    basis = [parse_rhs(b, mapping) for b in basis_parts]
    expressions = {num:parse_rhs(tagged(blocks, num), mapping)
                   for num in ['2.2.3','2.2.4','2.2.5']}
    expressions['2.2.5'] = expressions['2.2.5'].subs(
        {sp.Symbol('p'):basis[0], sp.Symbol('q'):basis[1]})
    return expressions, basis


def load_quadratic():
    blocks = math_blocks(SOURCE.read_text())
    mapping = {r'l_{k-1}(x)':'p', r'l_k(x)':'q', r'l_{k+1}(x)':'r',
               r'x_{k-1}':'a', r'x_k':'b', r'x_{k+1}':'c',
               r'y_{k-1}':'u', r'y_k':'v', r'y_{k+1}':'w'}
    first = next(b for b in blocks
                 if b.strip().startswith('l_{k-1}(x)=') and r'\frac' in b)
    pair = next(b for b in blocks
                if b.strip().startswith('l_k(x)=') and r'\frac' in b and r'x_{k-1}' in b)
    parts = [first]+pair.split(r'\qquad')
    if len(parts) != 3:
        raise ValueError('Expected three quadratic basis formulas.')
    basis = [parse_rhs(b, mapping) for b in parts]
    expr = parse_rhs(tagged(blocks, '2.2.7'), mapping)
    expr = expr.subs(dict(zip(sp.symbols('p q r'), basis)))
    expanded = next(b for b in blocks if r'\begin{aligned}' in b and 'L_2(x)' in b)
    return expr, basis, parse_rhs(expanded, mapping)
