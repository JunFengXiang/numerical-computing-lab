import hashlib, json, re
from pathlib import Path

lane = Path(__file__).resolve().parent
book = lane.parent.parent
source = '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
# Each of these thirteen original page images was opened with tools.view_image.
visually_reviewed_pages = list(range(93, 106))
notes = {
    93: ['章节首页未印出页码；书页 80 由章节目录及相邻书页 81 定位。', '图 4.1 裁切图已打开核对，标签完整。'],
    94: ['图 4.2 裁切图已打开核对，标签完整。'],
    95: ['式（4.1.7）原印为 f^{n+1}(ξ)，导数阶数无括号；按原式保留并校注。'],
    96: ['表 4.1 的 C_k^(n) 合并表头展开为 k 列；所有分数按原表保留。'],
    97: ['原书称 n≥8 时 Cotes 系数有正有负；保留原文，附 n=9 全正系数反例，详见 CH04A-E01。'],
    100: ['ch03b 独立交叉复核指出首条未编号梯形误差式的求和上下限遗漏；已回看原图补全 k=0 至 n-1。', '例 4.1 有效数字判断疑误已保留原文并校注；本书 1.3.3 定义由 ch01 原图核验回执交叉确认。', '表 4.2 及两条脚注完整转录。'],
    102: ['表 4.3 的 9.9456909 已放大原图确认并保留；相关原书疑误 CH04A-E03、CH04A-E04 单列。', 'ch03b 独立交叉复核指出 k=5 的原表数值疑误；已重开原图确认 0.9460596，独立以 80 位精度复算 n=32 并新增 CH04A-E07 校注。'],
    103: ['表 4.4 表头原字位 T_2^k、S_2^(k-1)、C_2^(k-2)、R_2^(k-3) 已放大确认并照录，另注明其对应分段数含义。', '由 Simpson 值构造 Cotes 值一段原引用（4.3.3），已保留，另指出本页实际系数见（4.3.5）。'],
    104: ['式（4.3.8）α_1、α_2、带帽 α_3、相邻文字带帽 α_k，以及后文带帽 β_2 / 未带帽 β_3 均放大核对并照录。', '递推指标范围与渐近展开含义另见 CH04A-E05、CH04A-E06。'],
    105: ['无编号 T 三角数表、全部四步算法和 Taylor 展开逐项转录。', '4.3.4 的后续推导位于 PDF 106，超出本 lane。']
}
errata = [
    {'id':'CH04A-E01','pdf_page':97,'printed_page':84,'location':'表 4.1 后首段','source_statement':'当 n≥8 时，Cotes 系数有正有负','finding':'n=9 是全部系数为正的反例；原文已保留并单列校注。','verification':'按式（4.2.2）用 SymPy 有理数符号积分计算全部十个系数。','status':'documented'},
    {'id':'CH04A-E02','pdf_page':100,'printed_page':87,'location':'例 4.1 解答第二段','source_statement':'T8=0.9456909 只有两位有效数字','finding':'按本书式（1.3.2），0.0003922 < 0.0005 且大于 0.00005，应具有三位有效数字。','verification':'与本页 I=0.9460831 作有理数差值，并经 ch01 核验的 1.3.3 定义交叉确认。','status':'documented'},
    {'id':'CH04A-E03','pdf_page':102,'printed_page':89,'location':'表 4.3，k=3 的 T_n','source_statement':'9.9456909','finding':'首位原印为 9，应为 0；本页下段和例 4.1 都列 T8=0.9456909。原表值已照录。','verification':'原图局部放大；本章相同 T8 数值交叉核对。','status':'documented'},
    {'id':'CH04A-E04','pdf_page':102,'printed_page':89,'location':'表 4.3 后首句','source_statement':'用变步长方法二分 9 次得到了这个结果','finding':'按本页 k 定义和表格，k=9 为 0.9460830，k=10 才列 0.9460831。原句已保留。','verification':'与同页表 4.3 及 k 为二分次数的定义比较。','status':'documented'},
    {'id':'CH04A-E05','pdf_page':104,'printed_page':91,'location':'式（4.3.13）的指标范围','source_statement':'k=1,2,…','finding':'下一页三角表和算法需要 T_m^(0)，相同递推式必须允许 k=0。原范围已保留。','verification':'对照 PDF 105 三角表及算法步 3 的右侧对角元素。','status':'documented'},
    {'id':'CH04A-E06','pdf_page':104,'printed_page':91,'related_pdf_pages':[105],'location':'定理 4.3 / 式（4.3.7），并涉及式（4.3.14）','source_statement':'仅设 f∈C∞[a,b]，即以等式写出无穷余项级数','finding':'C∞ 不能单独保证该无穷级数收敛并等于函数；外推分析应采用有限阶截断带余项的渐近展开解释。原条件、等式均保留。','verification':'区分任意有限阶 Taylor / Euler-Maclaurin 余项展开与无穷级数收敛；属于原书表述的数学限定问题。','status':'documented'},
    {'id':'CH04A-E07','pdf_page':102,'printed_page':89,'location':'表 4.3，k=5 的 T_n','source_statement':'0.9460596','finding':'复化梯形 n=32 得 0.946058560962768067178414064814380405…，七位小数应为 0.9460586。原表值已保留并单列校注。','verification':'ch03b 提出后重新打开原图确认；按 f(x)=sin(x)/x、f(0)=1、区间 [0,1] 独立使用 80 位精度计算，见 validation.json。','status':'documented'}
]
review = {'lane':'ch04a','reviewer':'Codex agent ch04a','human_review':False,'source_sha256':source,'pages':[], 'unresolved':[], 'source_errata':errata, 'validation_notes':[
    '全部 13 张指定 source-images 原图均已分别打开；两幅裁切图已再次打开，公式和表格疑难字位另有放大核对。',
    '此结果为 agent 核验转录；不是人工核验，也不声明数学上绝对无误。',
    '逐页保留跨页词句、公式编号、表号、原书数值与原书疑误；校注与原书正文分开。',
    '表 4.1 系数及余项符号的可计算验证见 validation.json。'
]}
for n in visually_reviewed_pages:
    p = lane / f'pages/pdf-{n:03}.md'
    s = p.read_text()
    im = book / f'source-images/pdf-{n:03}.jpeg'
    hs = []
    for line in s.splitlines():
        m = re.match(r'^#{1,6} (\d+(?:\.\d+)*) (.+)$', line)
        if m: hs.append({'id':m[1],'title':m[2]})
        m = re.match(r'^# 第 (\d+) 章 (.+)$', line)
        if m: hs.append({'id':m[1],'title':m[2]})
    tables = list(dict.fromkeys(re.findall(r'^表 ([0-9.]+)', s, re.M)))
    if n == 105: tables.append('T 数表（无编号）')
    review['pages'].append({'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(book)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':hs,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',s),'figures':list(dict.fromkeys(re.findall(r'!\[图 ([0-9.]+)',s))),'tables':tables,'notes':notes.get(n,[])})
(lane / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
print('review saved', len(review['pages']), 'pages;', len(errata), 'documented source errata')
