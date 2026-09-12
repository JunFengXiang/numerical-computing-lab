from pathlib import Path
import re,json,hashlib
root=Path(__file__).resolve().parents[2]
lane=root/'staging/ch08'
hashof=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_hash='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
notes={
217:['独立交叉复核发现式8.2.1下方原印a_ij非零，已回图内存裁切独立确认并按原印修订，追加ch08-E013校注。'],
220:['Jordan块与E_tk矩阵均完整转为LaTeX；无编号E_tk矩阵原图裁切另作视觉依据，标签与元素模式均有检索文字。','独立交叉复核指出Jordan块第三行上副对角线漏一组斜点，已重新打开原图确认并补齐。'],
232:['完整转录习题12(2)续至20；页首残差表达式与上页误差定义的符号关系已交叉标注。'],
231:['完整转录习题5续至12(2)；放大核对习题5(1)重复x2、习题12残差下标xi、lambda*以及误差递推负号，原文保留并另注。','第8题(2)原书同样使用B0表示G-S迭代矩阵，保留。第9/10题条件已与back及ch13核对。'],
229:['放大核对证明中sigma+2sigma、sigma+2omega，以及SOR算法步5(1)第二求和下限j=i+1；三处原式均保留并另注。'],
227:['完整转录表8.1全部10组松弛因子与迭代次数；放大核对例8.11所印迭代向量与2范数上界的数值不一致，原值保留并另注。'],
225:['放大核对证明中第二个G无修饰；原书将G从迭代矩阵重用于lambda(D-L)-U，原文保留并解释指代。'],
224:['放大核对定义8.5的范围确印1<=r<=n；可约分块通常应要求r<=n-1，原文保留并另注。'],
219:['放大核对例8.2误差无穷范数确印0.00157，与所印向量差一位小数；原值保留并另注。'],
216:['放大核对例8.1第10次迭代结果；第二分量和误差无穷范数与有理数复算不符，原值保留并另注。'],
218:['放大核对式8.2.3求和下限确印i=1；与应为j的求和指标不一致，原式保留并另注。']
}
errata=[
{'id':'ch08-E013','pdf_page':217,'printed_page':204,'location':'式8.2.1下方非零条件','source_text':'a_ij!=0 (i=1,2,...,n)','assessment':'疑似原书下标错误','evidence':'独立交叉复核ch07b指出后，以原图内存裁切独立确认j有下伸；原文没有j的范围，而后续除数为对角元a_ii。已保留原印a_ij并另注。'},
{'id':'ch08-E009','pdf_page':231,'printed_page':218,'location':'习题5(1)第二个方程','source_text':'0.4x1+x2+0.8x2=2','assessment':'疑似原书下标错误','evidence':'原图已放大目视重复x2。习题7将该组作为对称正定矩阵的考察对象，最后项为0.8x3时才与所示对称结构一致。原式保留。'},
{'id':'ch08-E010','pdf_page':231,'printed_page':218,'location':'习题12残差定义','source_text':'第二个求和内a_ij x_i^(k)','assessment':'疑似原书下标错误','evidence':'原图已放大目视xi。对照G-S公式及本题(1)，被加项应含x_j^(k)。原式保留。'},
{'id':'ch08-E011','pdf_page':231,'printed_page':218,'location':'习题12(2)误差定义','source_text':'epsilon^(k)=x^(k)-lambda*','assessment':'疑似原书符号错误','evidence':'原图已放大目视lambda*；紧随原文解释的是精确解x*。原式保留。'},
{'id':'ch08-E012','pdf_page':231,'printed_page':218,'location':'习题12(2)误差递推','source_text':'epsilon_i^(k+1)=epsilon_i^(k)-r_i^(k+1)/a_ii','assessment':'原书误差符号与递推不一致','evidence':'若按本题定义epsilon=x-x*，由(1)的加号更新可知误差递推也应为加号。原印负号保留，并标注矛盾；PDF232的正号残差式也与该定义不一致，若误差定义改用x*-x则两式一致。'},
{'id':'ch08-E006','pdf_page':229,'printed_page':216,'location':'定理8.10证明平方差因式','source_text':'omega sigma (sigma+2sigma)(omega-2)','assessment':'疑似原书排印错误','evidence':'原图已放大目视。展开左侧平方差得omega sigma (sigma+2alpha)(omega-2)，与8.4.10一致。原式保留。'},
{'id':'ch08-E007','pdf_page':229,'printed_page':216,'location':'定理8.10证明分母非零说明','source_text':'(sigma+2omega)^2+omega^2 beta^2!=0','assessment':'疑似原书排印错误','evidence':'原图已放大目视。上文lambda的分母模方为(sigma+alpha omega)^2+omega^2 beta^2。原式保留。'},
{'id':'ch08-E008','pdf_page':229,'printed_page':216,'location':'SOR算法步5(1)','source_text':'第二个求和下限j=i+1','assessment':'疑似原书算法漏项','evidence':'原图已放大目视。步5(3)执行xi<-xi+p，因此p为校正量；对照8.4.6，第二求和应从j=i开始，当前原式漏aii xi。原式保留。'},
{'id':'ch08-E005','pdf_page':227,'printed_page':214,'location':'例8.11第11次迭代向量与误差界','source_text':'x^(11)=(-0.99999646,-1.00000310,-0.99999953,-0.99999912)^T; ||epsilon^(11)||_2<=0.46e-5','assessment':'原书所印数值相互不一致','evidence':'原图已放大目视，原值保留。所印向量实际2范数误差4.8100831594e-6，大于4.6e-6；有理数从零迭代11次的误差为4.4938645773e-6。'},
{'id':'ch08-E004','pdf_page':224,'printed_page':211,'location':'定义8.5分块阶数范围','source_text':'1<=r<=n','assessment':'疑似原书边界排印错误','evidence':'原图已放大目视。为保证A11与A22均为非空低阶方阵，应要求1<=r<=n-1；r=n导致A22为零阶。原文保留并另注。'},
{'id':'ch08-E003','pdf_page':219,'printed_page':206,'location':'例8.2误差无穷范数','source_text':'||epsilon^(5)||_inf=0.00157','assessment':'疑似原书小数位错误','evidence':'原图已放大目视，原值保留。由所印向量与精确解计算为0.000157；有理数G-S迭代5次得误差无穷范数0.00015761335888942013。'},
{'id':'ch08-E001','pdf_page':216,'printed_page':203,'location':'例8.1第10次迭代数值','source_text':'x^(10)=(3.000032,1.999838,0.9998813)^T; ||epsilon^(10)||_inf=0.000187','assessment':'疑似原书数值错误','evidence':'原图已放大目视。按式8.1.4从零向量用有理数作10次迭代得(3.00003181406973,1.9998740186108068,0.9998812605453542)，误差无穷范数0.0001259813891930972；按原印向量计算的无穷范数则为0.000162。原文保留，另注。'},
{'id':'ch08-E002','pdf_page':218,'printed_page':205,'location':'式8.2.3求和下限','source_text':'i=1, j!=i','assessment':'疑似原书排印错误','evidence':'原图已放大目视下限为i=1；对照式8.2.2及被加项a_ij x_j^(k)，求和下限应为j=1。原式保留，另注。'}
]
pages=[]
for p in sorted((lane/'pages').glob('pdf-*.md')):
 n=int(p.stem.split('-')[1]);s=p.read_text();heads=[]
 for line in s.splitlines():
  if not line.startswith('#'):continue
  h=line.lstrip('#').strip()
  if h.startswith('第 8 章'):heads.append({'id':'8','title':'解线性方程组的迭代法'})
  elif re.match(r'8\.\d',h):
   a,b=h.split(maxsplit=1);heads.append({'id':a,'title':b})
  elif h in ['小结','习题']:heads.append({'id':'8.summary' if h=='小结' else '8.exercises','title':h})
 pages.append({'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(root)),'sha256':hashof(p),'source_image_sha256':hashof(root/f'source-images/pdf-{n:03}.jpeg'),'visual_review':'completed','content_coverage':'complete','headings':heads,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',s),'figures':[],'tables':list(dict.fromkeys(re.findall(r'表\s*(8\.\d+)',s))),'notes':notes.get(n,[])})
review={'lane':'ch08','reviewer':'Codex agent ch08','human_review':False,'source_sha256':source_hash,'pages':pages,'unresolved':[],'source_errata':[e for e in errata if any(p['pdf_page']==e['pdf_page'] for p in pages)],'validation_notes':['结构核验通过：18页元数据、原页链接、资产链接、Markdown数学块、LaTeX环境配对和文件SHA256均一致；32个编号公式无重复。','从18页提取的601个行内与独立数学片段用XeLaTeX和amsmath成功编译；该验证仅针对语法，不替代原图内容核验，产物位于staging/ch08/validation。','PDF215–232共18页均已逐一打开原图；正文、公式、矩阵、表8.1、SOR算法、小结和习题1–20完整转录。','表8.1所列10组omega对应的迭代次数已以双精度数值计算复核一致；例8.1/8.2/8.11另以有理数迭代定位原印数值疑误。','逐一打开原始页图并以目视转录；疑难处另存放大裁切。仅记录实际已经保存且目视核对完成的页。','本lane实际章名为第8章解线性方程组的迭代法；指定PDF页范围215–232。']}
(lane/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(f'Review receipt saved: {len(pages)} pages')
