from pathlib import Path
import hashlib,json,re
from save_page import SOURCE_HASH
BASE=Path(__file__).resolve().parent
BOOK=BASE.parent.parent
# Only append page numbers after opening and checking the corresponding source image.
REVIEWED=[247,248,249,250,251,252,253,254,255,256,257,258,259,260]
ERRATA=[
 {'id':'ch09b-E12','pdf_page':255,'description':'分块上三角阵第一个二阶对角块原印 B_l，与末块同名；按顺序编号疑应为 B_1。已据交叉复核回看原图，保留原印并校注。','type':'suspected_source_subscript_error'},
 {'id':'ch09b-E11','pdf_page':252,'description':'定理 9.16 证明首句原印由定理 9.12；所用平面旋转矩阵三角化结论对应定理 9.15，原引用保留。','type':'suspected_source_reference_error'},
 {'id':'ch09b-E09','pdf_page':257,'description':'第 i 次左变换原印及 v_k，对应矩阵为 v_i；保留原印下标。','type':'suspected_source_subscript_error'},
 {'id':'ch09b-E10','pdf_page':257,'description':'P_{i,i+1} 的范围原印 i=1,2,...,n+1，按 n 阶矩阵应至 n-1；保留原文。','type':'source_index_bound_error'},
 {'id':'ch09b-E07','pdf_page':253,'description':'QR 分解左变换引用原印为定理 9.13，所指上三角阵结论对应定理 9.15；保留原文。','type':'suspected_source_reference_error'},
 {'id':'ch09b-E08','pdf_page':254,'description':'式（9.4.16）前原印引用式（4.15），本页对应为（9.4.15）；保留原文。','type':'source_reference_typo'},
 {'id':'ch09b-E04','pdf_page':251,'description':'引理 1 证明首式末项原印 c alpha_i，按矩阵乘法及下一行疑应为 c alpha_j；保留原文。','type':'suspected_source_subscript_error'},
 {'id':'ch09b-E05','pdf_page':251,'description':'定理 9.15 证明末行原印 a_{2j}^{(2)}，按第 2 列消元疑应为 a_{j2}^{(2)}；保留原文。','type':'suspected_source_subscript_error'},
 {'id':'ch09b-E06','pdf_page':251,'description':'算法 1 零向量分支未赋值输出 v，按定义应为 0；原步骤保留。','type':'suspected_source_algorithm_omission'},
 {'id':'ch09b-E01','pdf_page':247,'description':'P^T y 展开式原印 lambda_k^{-1}，与初等反射阵使用 rho_k^{-1} 不一致；保留原文。','type':'suspected_source_symbol_error'},
 {'id':'ch09b-E02','pdf_page':248,'description':'算法 3 步 3（2）第一个求和上限原印 n，按下三角存储算法疑应为 i；保留原文。','type':'suspected_source_formula_error'},
 {'id':'ch09b-E03','pdf_page':249,'description':'例 9.5（1）u_1 式原印 sigma_1 rho_1，结合列向量疑应为 sigma_1 e_1；保留原文。','type':'suspected_source_symbol_error'}
]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def headings(n):
 if n<250:return [{'id':'9.3.2','title':'用正交相似变换约化矩阵'}]
 if n<252:return ([{'id':'9.4','title':'QR算法'}] if n==250 else [])+[{'id':'9.4.1','title':'引言'}]
 if n<255:return ([{'id':'9.4.1','title':'引言'}] if n==252 else [])+[{'id':'9.4.2','title':'QR算法'}]
 if n<259:return ([{'id':'9.4.2','title':'QR算法'}] if n==255 else [])+[{'id':'9.4.3','title':'带原点位移的QR方法'}]
 return [{'id':'9.4.3','title':'带原点位移的QR方法'},{'id':'9.summary','title':'小结'},{'id':'9.exercises','title':'习题'}] if n==259 else [{'id':'9.exercises','title':'习题'}]
pages=[]
for n in REVIEWED:
 p=BASE/'pages'/f'pdf-{n}.md';t=p.read_text()
 pages.append({'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(BOOK)),'sha256':digest(p),'source_image_sha256':digest(BOOK/'source-images'/f'pdf-{n}.jpeg'),'visual_review':'completed','content_coverage':'complete','headings':headings(n),'formula_ids':re.findall(r'\\tag\{([^}]+)\}',t),'figures':[],'tables':[],'notes':[e['id']+': '+e['description'] for e in ERRATA if e['pdf_page']==n]})
r={'lane':'ch09b','reviewer':'Codex agent ch09b','human_review':False,'source_sha256':SOURCE_HASH,'pages':pages,'unresolved':[],'source_errata':ERRATA,'validation_notes':['逐页以 tools.view_image 打开原图，关键疑误另打开原尺寸局部裁切核对。未使用 GPU OCR，也未用 OCR 候选替代目视。','PDF247 接续 9.3.2；跨页推导只转录各页实际内容。','PDF247–260 共 14 页均已逐页打开原图并完成正文、公式、算法、例题、小结及习题 1–10 转录；不存在编号图表。矩阵图式已转成 LaTeX，保留方框与分块标示。','所有独立及行内数学已用 XeLaTeX -no-pdf 编译通过；检查文件见 staging/ch09b/validation/math-check.tex 和 math-check.log。编译仅验证语法，不代替内容目视核对。','公式号覆盖 9.3.3 及 9.4.1–9.4.17；逐页图与 Markdown SHA-256 均现场计算。疑似原书错误保持原文，另列 source_errata；这些不是未辨认的文字。']}
(BASE/'review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(f'saved {len(pages)} reviewed pages')
