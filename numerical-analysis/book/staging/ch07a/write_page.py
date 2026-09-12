from pathlib import Path
import sys,hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
LANE=ROOT/'staging/ch07a'
SOURCE='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
def save(n, body, headings=None,figures=None,tables=None,notes=None):
 p=LANE/f'pages/pdf-{n:03}.md'
 p.write_text(f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n:03}.jpeg\nsource_sha256: {SOURCE}\nstatus: agent_reviewed_transcription\n---\n\n[原页扫描](../../../source-images/pdf-{n:03}.jpeg)\n\n<!-- source-page: {n} -->\n\n'+body.strip()+'\n',encoding='utf-8')
 rp=LANE/'review.json'
 r=json.loads(rp.read_text()) if rp.exists() else {'lane':'ch07a','reviewer':'Codex agent ch07a','human_review':False,'source_sha256':SOURCE,'pages':[],'unresolved':[],'source_errata':[],'validation_notes':[]}
 page={'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((ROOT/f'source-images/pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings or [],'formula_ids':re.findall(r'\\tag\{([^}]+)\}',body),'figures':figures or [],'tables':tables or [],'notes':notes or []}
 r['pages']=[x for x in r['pages'] if x['pdf_page']!=n]+[page]
 r['pages'].sort(key=lambda x:x['pdf_page'])
 rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(n,len(body))
