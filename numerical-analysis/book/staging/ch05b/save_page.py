from pathlib import Path
import sys,json,hashlib,re
root=Path(__file__).resolve().parents[2]
lane=root/'staging/ch05b'
n=int(sys.argv[1]); body=sys.stdin.read().strip()+'\n'
sha='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
page=lane/'pages'/f'pdf-{n:03}.md'
page.write_text(f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n:03}.jpeg\nsource_sha256: {sha}\nstatus: agent_reviewed_transcription\n---\n\n[原页](../../../source-images/pdf-{n:03}.jpeg)\n\n<!-- source-page: {n} -->\n\n'+body)
rpath=lane/'review.json'
r=json.loads(rpath.read_text()) if rpath.exists() else {'lane':'ch05b','reviewer':'Codex agent ch05b','human_review':False,'source_sha256':sha,'pages':[],'unresolved':[],'source_errata':[],'validation_notes':[]}
headings=[]
for m in re.finditer(r'^#{1,6}\s+(\S+)\s+(.+)$',body,re.M):
    headings.append({'id':m[1],'title':m[2]})
p={'pdf_page':n,'printed_page':n-13,'path':str(page.relative_to(root)),'sha256':hashlib.sha256(page.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((root/'source-images'/f'pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings,'formula_ids':re.findall(r'\\tag\{([^}]+)\}',body),'figures':sorted(set(re.findall(r'图\s*(5\.\d+)',body))),'tables':sorted(set(re.findall(r'表\s*(5\.\d+)',body))),'notes':[]}
r['pages']=[v for v in r['pages'] if v['pdf_page']!=n]+[p]
r['pages'].sort(key=lambda v:v['pdf_page'])
rpath.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(f'Saved {page.name}; reviewed pages {len(r["pages"])}')
