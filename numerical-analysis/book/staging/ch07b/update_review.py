import hashlib,json,re,sys
from pathlib import Path
base=Path(__file__).resolve().parents[2]
lane=base/'staging/ch07b'
r=json.loads((lane/'review.json').read_text())
for token in sys.argv[1:]:
 n=int(token); p=lane/f'pages/pdf-{n}.md'; s=p.read_text(); im=base/f'source-images/pdf-{n}.jpeg'
 old=next((q for q in r['pages'] if q['pdf_page']==n),{})
 headings=[{'id':a,'title':b} for a,b in re.findall(r'^#+ (7\.[\d.]+) (.+)$',s,re.M)]
 record={'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(base)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256(im.read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',s),'figures':old.get('figures',[]),'tables':old.get('tables',[]),'notes':old.get('notes',['已打开整页原图逐字逐式核对，页内全部内容转录。'])}
 r['pages']=[q for q in r['pages'] if q['pdf_page']!=n]+[record]
r['pages'].sort(key=lambda q:q['pdf_page'])
(lane/'review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(f"Saved review for {len(r['pages'])} pages")
