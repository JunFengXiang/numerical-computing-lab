from pathlib import Path
import json,re
from write_front import save,BOOK,LANE
INDEX=json.loads((BOOK/'index/sections.json').read_text())['entries']

def save_toc(n,updates=None,notes=None):
    updates=updates or {}
    entries=[e.copy() for e in INDEX if e['toc_source_pdf_page']==n]
    body=['# 目录' if n==6 else '# 目录（续）','', '> 转录说明（agent 补充）：以下为印刷目录；末列是目录所列的正文书页码。本页底部的目录页码另记在 YAML 中。','']
    if n==6: body+=['## 上篇　数值算法分析','']
    body+=['| 编号 | 标题 | 书页码 |','|:---|:---|---:|']
    for e in entries:
        if n==11 and e['id']=='10':
            body+=['', '## 下篇　高效算法设计', '', '| 编号 | 标题 | 书页码 |', '|:---|:---|---:|']
        e.update(updates.get(e['id'],{}))
        id=e['id']; title=e['title']; kind=e['kind']
        for english in ['Lagrange','Newton','Hermite']:
            title=re.sub(english+r'(?=[\u4e00-\u9fff])',english+' ',title)
        title=re.sub(r'(?<=[\u4e00-\u9fff])([A-Za-z])',r' \1',title)
        title=re.sub(r'([A-Za-z])(?=[\u4e00-\u9fff])',r'\1 ',title)
        title=title.replace('C[a,b]','$C[a,b]$')
        num=id if kind=='section' else ''
        if kind=='chapter':
            num=('\\*' if e.get('source_prefix_star') else '')+'第 '+id+' 章'
            title='**'+title+'**'
        page=e.get('display_page',str(e['printed_page_start']))
        body.append(f'| {num} | {title} | {page} |')
    if notes:
        body+=['','> 校注（agent 补充）：'+ ' '.join(notes)]
    save(n,n-5,'\n'.join(body),[{'id':'front.toc' if n==6 else f'front.toc{n-5}','title':'目录' if n==6 else '目录（续）'}],['目录独立编号 '+str(n-5)+'；目录条目不表示本页含相应正文。']+(notes or []))
    rp=LANE/'review.json'; data=json.loads(rp.read_text())
    for p in data['pages']:
        if p['pdf_page']==n:
            p['toc_only']=True
            p['toc_entry_count']=len(entries)
            p['toc_entries']=[{'id':e['id'],'title':e['title'],'printed_page_start':e['printed_page_start'],'source_prefix_star':e.get('source_prefix_star',False)} for e in entries]
    rp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    # These two pages were individually opened and every item compared to the image.
    save_toc(6)
    save_toc(7)
