from pathlib import Path
import hashlib,json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
LANE=Path(__file__).resolve().parent
SOURCE='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'

def normalize(n):
    s=(ROOT/f'ocr/glm-fullpage/pdf-{n:03}.md').read_text()
    s=s.split(f'[查看原页](../../source-images/pdf-{n:03}.jpeg)',1)[1].strip()
    s=re.sub(r'^\s*[•·] ?\d+ ?[•·]\s*$', '', s, flags=re.M)
    s=re.sub(r'^第\s*(\d+)\s*章\s*(.+)$',r'# 第 \1 章 \2',s,flags=re.M)
    s=re.sub(r'^(\d+\.\d+(?:\.\d+)?)\s+(.+)$',lambda m:'#'*(m.group(1).count('.')+1)+' '+m.group(1)+' '+m.group(2),s,flags=re.M)
    # Convert full-line single-dollar displays before moving their printed equation numbers.
    s=re.sub(r'^\$([^$\n]+)\$(\s*[,.;，。；]?\s*)(\(\d+\.\d+\.\d+\))?\s*$',lambda m:'$$\n'+m.group(1)+(' '+m.group(2).strip() if m.group(2).strip() else '')+(' \\tag{'+m.group(3)[1:-1]+'}' if m.group(3) else '')+'\n$$',s,flags=re.M)
    # Number outside a display.
    s=re.sub(r'\$\$(.*?)\$\$\s*\((\d+\.\d+\.\d+)\)',lambda m:'$$'+m.group(1).rstrip()+' \\tag{'+m.group(2)+'}\n$$',s,flags=re.S)
    # Number inside a display.
    s=re.sub(r'(?:\\quad\s*)?\((\d+\.\d+\.\d+)\)(?=\s*\$\$)',r'\\tag{\1}',s)
    # Normalize display delimiters for readability.
    s=re.sub(r'\$\$(.*?)\$\$',lambda m:'$$\n'+m.group(1).strip()+'\n$$',s,flags=re.S)
    return s.strip()

def save(n,body):
    header=f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n:03}.jpeg\nsource_sha256: {SOURCE}\nstatus: agent_reviewed_transcription\n---\n\n[查看原页](../../../source-images/pdf-{n:03}.jpeg)\n\n<!-- source-page: {n} -->\n\n'
    (LANE/f'pages/pdf-{n:03}.md').write_text(header+body.strip()+'\n')

meta_path=LANE/'page_meta.json'
meta=json.loads(meta_path.read_text()) if meta_path.exists() else {}
def register(n,notes=None,figures=None,tables=None):
    meta[str(n)]={'notes':notes or [],'figures':figures or [],'tables':tables or []}
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    review()

def review():
    pages=[]
    for ns,m in sorted(meta.items(),key=lambda kv:int(kv[0])):
        n=int(ns); path=LANE/f'pages/pdf-{n:03}.md';s=path.read_text()
        headings=[]
        for _,title in re.findall(r'^(#+) (.+)$',s,flags=re.M):
            match=re.match(r'(\d+(?:\.\d+)*)\s+(.+)',title)
            cm=re.match(r'第\s*(\d+)\s*章\s*(.+)',title)
            if match: headings.append({'id':match[1],'title':match[2]})
            elif cm: headings.append({'id':cm[1],'title':cm[2]})
        pages.append({'pdf_page':n,'printed_page':n-13,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((ROOT/f'source-images/pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',s),'figures':m['figures'],'tables':m['tables'],'notes':m['notes']})
    errata_path=LANE/'source_errata.json'
    errata=json.loads(errata_path.read_text()) if errata_path.exists() else []
    (LANE/'review.json').write_text(json.dumps({'lane':'ch03a','reviewer':'Codex agent ch03a','human_review':False,'source_sha256':SOURCE,'pages':pages,'unresolved':[],'source_errata':errata,'validation_notes':['每页原图已实际打开并逐字逐式与 OCR 候选对照；OCR 只作底稿。','单页保留跨页边界；图为原页裁切；页眉页脚重复文字略去。']},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    for n in (58,59,60,61):
        s=normalize(n)
        if n==58:
            s=s.replace('\n\n图3.1','\n\n![图 3.1 原图裁切](../assets/fig-3-1.png)\n\n图 3.1（原图）。图中为上文误差分布曲线，横轴 $x$、纵轴 $y$；标签为 $-1$、$1$、$O$。曲线在负半轴下方、正半轴上方，通过原点；在 $x=-1$ 和 $x=1$ 处有竖向辅助线。')
            s += '\n\n<!-- 本页末句续 PDF 59。 -->'
            Image.open(ROOT/'source-images/pdf-058.jpeg').crop((1120,1850,1650,2390)).save(LANE/'assets/fig-3-1.png')
        elif n==59:
            s += '\n\n<!-- 本页末句续 PDF 60。 -->\n\n> 校注（agent 补充，原书疑误）：原页 Lagrange 插值式后的求和明确印为 $\\sum_{k=0}^{n}l_k(x_k)=1$，此处按原文保留。由基函数性质 $l_k(x_k)=1$，左端应为 $n+1$；通常的恒等式应为 $\\sum_{k=0}^{n}l_k(x)=1$。这不是 OCR 误识。'
        elif n==60:
            s=s.replace(r'\|\|f\|_\infty - \|g\|_\infty \leqslant \|f-g\|_\infty',r'\bigl|\|f\|_\infty - \|g\|_\infty\bigr| \leqslant \|f-g\|_\infty')
            s+='\n\n<!-- 本页末句续 PDF 61。 -->'
        save(n,s)
        register(n,notes=(["本页 Lagrange 基函数求和式印为 sum l_k(x_k)=1；保留并添加原书疑误校注。"] if n==59 else (["纠正 OCR 式 (3.1.10) 丢失绝对值外括线。"] if n==60 else [])),figures=['3.1'] if n==58 else [])
    (LANE/'source_errata.json').write_text(json.dumps([{'id':'ch03a-E01','pdf_page':59,'printed_page':46,'kind':'source_typographical_error','location':'Lagrange 插值多项式后无编号求和式','source':r'\sum_{k=0}^{n} l_k(x_k)=1','note':'原图确印 x_k；由 l_k(x_k)=1 左端为 n+1，通常恒等式应为 sum l_k(x)=1。转录保留原文。'}],ensure_ascii=False,indent=2)+'\n')
    review()
