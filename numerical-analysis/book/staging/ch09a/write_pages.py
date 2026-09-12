from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
LANE=ROOT/'staging/ch09a'
SOURCE_SHA='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
def write_page(n,body,headings=None,notes=None,figures=None,tables=None):
    path=LANE/'pages'/f'pdf-{n:03}.md'
    text=f'''---
pdf_page: {n}
printed_page: {n-13}
source_image: source-images/pdf-{n:03}.jpeg
source_sha256: {SOURCE_SHA}
status: agent_reviewed_transcription
---

[原页图像](../../../source-images/pdf-{n:03}.jpeg)

<!-- source-page: {n} -->

'''+body.strip()+'\n'
    path.write_text(text,encoding='utf-8')
    rp=LANE/'review.json'
    if rp.exists(): review=json.loads(rp.read_text())
    else: review={'lane':'ch09a','reviewer':'Codex agent ch09a','human_review':False,'source_sha256':SOURCE_SHA,'pages':[],'unresolved':[],'source_errata':[],'validation_notes':[]}
    entry={'pdf_page':n,'printed_page':n-13,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((ROOT/f'source-images/pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings or [],'formula_ids':re.findall(r'\\tag\{([^}]+)\}',text),'figures':figures or [],'tables':tables or [],'notes':notes or []}
    review['pages']=[e for e in review['pages'] if e['pdf_page']!=n]+[entry]
    review['pages'].sort(key=lambda e:e['pdf_page'])
    rp.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def add_errata(entries):
    rp=LANE/'review.json'; review=json.loads(rp.read_text())
    for e in entries:
        review['source_errata']=[x for x in review['source_errata'] if x['id']!=e['id']]+[e]
    rp.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    pass
