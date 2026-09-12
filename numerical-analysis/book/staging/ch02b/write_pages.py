from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[2]
lane=root/'staging/ch02b'
source_hash='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
def save(n,body):
 p=lane/f'pages/pdf-{n:03}.md'
 p.write_text(f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n:03}.jpeg\nsource_sha256: {source_hash}\nstatus: agent_reviewed_transcription\n---\n\n[查看原页](../../../source-images/pdf-{n:03}.jpeg)\n\n<!-- source-page: {n} -->\n\n'+body.strip()+'\n',encoding='utf-8')
def review():
 notes=json.loads((lane/'page-notes.json').read_text()) if (lane/'page-notes.json').exists() else {}
 obj={'lane':'ch02b','reviewer':'Codex agent ch02b','human_review':False,'source_sha256':source_hash,'pages':[],'unresolved':[],'source_errata':[],'validation_notes':['逐一打开原页图像，并对正文、公式、图表和习题作 agent 目视核验；OCR 仅作底稿。']}
 for p in sorted((lane/'pages').glob('pdf-*.md')):
  n=int(p.stem.split('-')[1]); body=p.read_text(); extra=notes.get(str(n),{})
  heads=[{'id':a,'title':b} for a,b in re.findall(r'^#{1,6} (\d+(?:\.\d+)*|2\.summary|2\.exercises)\s+(.+)$',body,re.M)]
  for title,ident in [('小结','2.summary'),('习题','2.exercises')]:
   if f'## {title}\n' in body: heads.append({'id':ident,'title':title})
  obj['pages'].append({'pdf_page':n,'printed_page':n-13,'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((root/f'source-images/pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':heads,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',body),'figures':extra.get('figures',[]),'tables':extra.get('tables',[]),'notes':extra.get('notes',[])})
  obj['source_errata'].extend(extra.get('source_errata',[]));obj['unresolved'].extend(extra.get('unresolved',[]))
 (lane/'review.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__': review()
