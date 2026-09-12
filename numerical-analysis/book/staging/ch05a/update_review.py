"""Refresh hashes for explicitly visually reviewed ch05a pages only."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / 'staging/ch05a'
SHA = '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
META = {
    119: {'headings': [{'id': '5', 'title': '常微分方程数值解法'}, {'id': '5.1', 'title': '引言'}, {'id': '5.2', 'title': 'Euler 方法'}, {'id': '5.2.1', 'title': 'Euler 格式'}], 'notes': ['原页已打开核对；式 (5.1.1)、(5.1.2) 原版共用左大括号，按协议分为独立编号公式。末句跨页。']},
    120: {'figures': ['5.1', '5.2'], 'tables': ['5.1'], 'notes': ['原页已打开核对；表 5.1 全部 10 行数值逐项对照；图 5.1、5.2 保存原图裁切。原页开头两处印为“极点”，放大核实后保留。末句跨页。']},
    121: {'headings': [{'id': '5.2.2', 'title': '后退的 Euler 格式'}], 'notes': ['原页已打开核对；局部截断误差、向后差商及迭代上标 (0)、(1) 已二次对照。末句跨页。']},
    122: {'headings': [{'id': '5.2.3', 'title': '梯形格式'}], 'figures': ['5.3'], 'notes': ['原页已打开核对；放大确认偏导数记法为 f_y，无额外撇号；误差式 (5.2.7) 负号已核对。图 5.3 原图裁切与全部标签已保存。末句跨页。']},
    123: {'headings': [{'id': '5.2.4', 'title': '改进的 Euler 格式'}], 'notes': ['原页已打开核对；梯形迭代、收敛因子 hL/2、预测值横线与校正值区别已逐式对照。']},
    124: {'headings': [{'id': '5.2.5', 'title': 'Euler 两步格式'}], 'tables': ['5.2'], 'notes': ['原页已打开核对；表 5.2 全部数值逐项转录并复算；发现两处原书疑误，原文保留并另列校注。关键数字及下标均已额外放大核对。']},
    125: {'notes': ['原页已打开核对；式 (5.2.16)–(5.2.18) 三阶导数、符号与 4/5、1/5 系数二次对照；六环节中的前五项在本页，第六项跨页。']},
    126: {'headings': [{'id': '5.3', 'title': 'Runge-Kutta 方法'}, {'id': '5.3.1', 'title': 'Taylor 级数法'}], 'notes': ['原页已打开核对；六环节末项、Taylor 展开及全导数递推逐项核验；式 (5.3.2) 的偏导阶数与乘积括号已二次对照。末句跨页。']},
    127: {'headings': [{'id': '5.3.2', 'title': 'Runge-Kutta 方法的基本思想'}], 'tables': ['5.3'], 'notes': ['原页已打开核对；定义 5.1、例 5.3 的一至四阶导数、表 5.3 三行数据和平均斜率定义完整转录。末句跨页。']},
    128: {'headings': [{'id': '5.3.3', 'title': '二阶 Runge-Kutta 方法'}], 'notes': ['原页已打开核对；二阶 Runge-Kutta 待定系数、节点 n+p 与 p 的范围已二次对照。末句跨页。']},
    129: {'headings': [{'id': '5.3.4', 'title': '三阶 Runge-Kutta 方法'}], 'notes': ['原页已打开核对；二阶条件、变形 Euler 与三阶格式逐式转录。两处第三阶段节点 n+p 经放大确认为原书下标错误，保留并校注。']},
    130: {'notes': ['原页已打开核对；D、D^2、带横线的 D 和阶段展开系数逐项二次对照；保留原书对 D^2 的显式定义。']},
    131: {'headings': [{'id': '5.3.5', 'title': '四阶 Runge-Kutta 方法'}], 'notes': ['原页已打开核对；三阶 Kutta、经典四阶 RK 和例 5.4 全部阶段公式逐项对照。表 5.4 在次页。']},
    132: {'headings': [{'id': '5.3.6', 'title': '变步长的 Runge-Kutta 方法'}], 'tables': ['5.4'], 'notes': ['原页已打开核对；表 5.4 五行数值与 RK4 独立复算一致；步长折半的上标 h、h/2、误差因子 1/16、1/15 与原页逐式对照。式 (5.3.15) 原印使用等号，保留。']},
    133: {'headings': [{'id': '5.4', 'title': '单步法的收敛性和稳定性'}, {'id': '5.4.1', 'title': '单步法的收敛性'}], 'notes': ['原页已打开核对；变步长两种处理分支、收敛性定义及 Euler 极限论证完整转录。末句跨页。']},
    134: {'notes': ['原页已打开核对；定理 5.1、全部误差递推及页下注完整转录；(5.4.5) 缺绝对值、(5.4.9) 指数 q 已额外放大确认并单列原书校注。末句跨页。']},
    135: {'headings': [{'id': '5.4.2', 'title': '单步法的稳定性'}], 'notes': ['原页已打开核对；页首不等式的 n、h 两处指数已放大确认，正文保留并附正确估计；改进 Euler 的 Lipschitz 常数、稳定性定义和扰动值逐项对照。末句跨页。']},
    136: {'figures': ['5.4'], 'notes': ['原页已打开核对；条件稳定/无条件稳定、时间常数、例 5.5 全部本页内容转录。原句“步长 h 应使 τ 不超过”已放大确认并校注。图 5.4 原图及全部文字刻度标签保存；末句续 PDF 137，表 5.5 在后续 lane。']},
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pages = []
for n, meta in sorted(META.items()):
    path = LANE / f'pages/pdf-{n:03d}.md'
    text = path.read_text()
    pages.append({'pdf_page': n, 'printed_page': n - 13,
                  'path': str(path.relative_to(ROOT)), 'sha256': digest(path),
                  'source_image_sha256': digest(ROOT / f'source-images/pdf-{n:03d}.jpeg'),
                  'visual_review': 'completed', 'content_coverage': 'complete',
                  'headings': meta.get('headings', []),
                  'formula_ids': re.findall(r'\\tag\{([^}]+)\}', text),
                  'figures': meta.get('figures', []), 'tables': meta.get('tables', []),
                  'notes': meta.get('notes', [])})

review = {'lane': 'ch05a', 'reviewer': 'Codex agent ch05a', 'human_review': False,
          'source_sha256': SHA, 'pages': pages, 'unresolved': [], 'source_errata': [
              {'id': 'ch05a-E001', 'pdf_page': 124, 'printed_page': 111, 'location': '表 5.2，x_n=0.8 的 y_n', 'kind': 'suspected_source_numeric_error', 'original': '1.6153', 'suggested': '1.6165', 'evidence': '原页放大确认为 1.6153；按例 5.2 的递推式从 y_0=1、h=0.1 复算得 y_8=1.6164747827…；其余九行与四位小数输出相符。正文保留原值。'},
              {'id': 'ch05a-E002', 'pdf_page': 124, 'printed_page': 111, 'location': '5.2.5 单步法与两步法比较段', 'kind': 'source_index_error', 'original': '更前面一步的信息 y_{n+1}', 'suggested': 'y_{n-1}', 'evidence': '原页放大确认为 n+1；本页式 (5.2.13) 为 y_{n+1}=y_{n-1}+2hf(x_n,y_n)，所指前一步应为 n-1。正文保留原印。'},
              {'id': 'ch05a-E003', 'pdf_page': 129, 'printed_page': 116, 'location': '5.3.4 引入第三阶段节点与预测 K_3 的两处正文', 'kind': 'source_index_error', 'original': 'x_{n+p}=x_n+qh；为了预测点 x_{n+p} 处的斜率值 K_3', 'suggested': '两处 x_{n+p} 应为 x_{n+q}', 'evidence': '两处均已放大确认原印 n+p；同页 K_3=f(x_{n+q},y_{n+q}) 及式 (5.3.7) 明确其节点是 x_n+qh。正文保留原印。'},
              {'id': 'ch05a-E004', 'pdf_page': 134, 'printed_page': 121, 'location': '式 (5.4.5)', 'kind': 'source_missing_absolute_value', 'original': 'L_φ(y−ȳ)', 'suggested': 'L_φ|y−ȳ|', 'evidence': '右端只有圆括号，经原图放大确认；对 y<ȳ 且 L_φ>0 时，原印右端为负，不能作为绝对差上界。正文保留原式并说明。'},
              {'id': 'ch05a-E005', 'pdf_page': 134, 'printed_page': 121, 'location': '式 (5.4.9)', 'kind': 'source_exponent_error', 'original': 'Ch^q/L_φ', 'suggested': 'Ch^p/L_φ', 'evidence': '原印 q 已放大确认；从式 (5.4.8) 等比求和得 Ch^(p+1)/(hL_φ)=Ch^p/L_φ，且次页 (5.4.10) 用 p。正文保留原式。'},
              {'id': 'ch05a-E006', 'pdf_page': 135, 'printed_page': 122, 'location': '页首无编号不等式', 'kind': 'source_exponent_errors', 'original': '(1+hL_φ)^n≤(e^(nL_φ))^n≤e^(hL_φ)', 'suggested': '(1+hL_φ)^n≤(e^(hL_φ))^n=e^(nhL_φ)≤e^(TL_φ)', 'evidence': '原页中间 n 和末项 h 均经放大确认；利用前页 nh≤T 及 1+u≤e^u 得校注所列估计，与式 (5.4.10) 相符。正文保留原式。'},
              {'id': 'ch05a-E007', 'pdf_page': 136, 'printed_page': 123, 'location': '例 5.5 稳定性步长说明', 'kind': 'source_wording_symbol_error', 'original': '步长 h 应使 τ 不超过 2τ=0.02', 'suggested': '步长 h 应不超过 2τ=0.02', 'evidence': '原句“使 τ”经放大确认；本页式 (5.4.13) 的被约束量是 h，正文保留原印并校注。'}],
          'validation_notes': [
              '仅已实际打开原图且完成逐字逐式核对的页列入 pages；此回执为 agent 核验，不是人工核验。',
              '18 页 YAML、页码、文件/源图 SHA-256、原图链接、数学括号/环境和 48 个连续公式编号结构检查通过；详见 staging/ch05a/validation.json。',
              '图 5.1–5.4 的裁切文件均再次打开检查，文字刻度标签完整。',
              '表 5.1–5.4 用 40 位 Decimal 按原页递推式复算；仅表 5.2 在 x=0.8 的原值 1.6153 与复算四位小数 1.6165 不同，已列为 ch05a-E001 并保留原值。',
              '书页 123 的末句和表 5.5 续后续 lane，不凭上下文补写。']}
evidence_images = {
    'ch05a-E001': ['check-p124-table.png'],
    'ch05a-E002': ['check-p124-index.png'],
    'ch05a-E003': ['check-p129-third-node.png', 'check-p129-predict-node.png'],
    'ch05a-E004': ['check-p134-lipschitz.png'],
    'ch05a-E005': ['check-p134-bound.png'],
    'ch05a-E006': ['check-p135-exponents.png'],
    'ch05a-E007': ['check-p136-step.png'],
}
for item in review['source_errata']:
    item['evidence_images'] = [f'staging/ch05a/assets/{name}' for name in evidence_images[item['id']]]
(LANE / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
print(f'Saved review for {len(pages)} pages: {min(META)}–{max(META)}')
