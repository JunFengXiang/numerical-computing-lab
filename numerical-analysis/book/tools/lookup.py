#!/usr/bin/env python3
"""Resolve chapter/section IDs and topics without silently rewriting a supplied ID."""
from pathlib import Path
import argparse
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def resolve(query):
    entries=json.loads((ROOT/'index'/'sections.json').read_text())['entries']
    byid={e['id']:e for e in entries}
    # Formula IDs share the same shape as subsection IDs; explicit formula wording
    # must not be interpreted as a subsection request.
    if re.search(r'公式|式\s*[（(]?\s*\d+\.',query):
        m=re.search(r'\d+\.\d+\.\d+',query)
        number=m[0] if m else None
        formulas=json.loads((ROOT/'index'/'formulas.json').read_text())['formulas']
        matches=[f for f in formulas if f['id']==number]
        entry=matches[0] if len(matches)==1 else None
        return {'query':query,'requested_formula':number,
                'status':'resolved_formula' if entry else ('ambiguous_formula' if matches else 'formula_not_verified'),
                'entry':entry,
                'candidates':matches if len(matches)>1 else [],
                'message':'这是公式编号，与同形的章节编号分开检索。'}
    m=re.search(r'(?<!\d)(\d+(?:\.\d+){1,2})(?!\d)',query)
    requested=m[1] if m else None
    if requested is None:
        chapter=re.search(r'第\s*(\d+)\s*章',query)
        requested=chapter[1] if chapter else None
    terms=[]
    for e in entries:
        # Generic labels such as 引言 do not override a supplied precise ID.
        candidates=e.get('aliases',[])+([e['title']] if len(e['title'])>2 else [])
        terms.extend((len(t),t,e) for t in candidates if t.lower() in query.lower())
    terms.sort(key=lambda x:-x[0])
    topic_entry=terms[0][2] if terms else None
    explicit=byid.get(requested)
    warnings=[]
    if requested and not explicit:
        return {'query':query,'status':'unknown_section','requested_section':requested,
                'message':'本书目录中没有该章节编号，不能自动猜成相近章节。'}
    if explicit and topic_entry and explicit['id']!=topic_entry['id']:
        warnings.append(f'编号 {requested} 对应“{explicit["title"]}”；主题匹配 {topic_entry["id"]}“{topic_entry["title"]}”。')
        chosen=topic_entry
    else:
        chosen=explicit or topic_entry
    if not chosen:
        return {'query':query,'status':'no_match','message':'请给出章节号或更具体的主题。'}
    result={'query':query,'status':'resolved_with_conflict' if warnings else 'resolved',
            'requested_section':requested,'resolved_section':chosen['id'],
            'title':chosen['title'],'warnings':warnings,'entry':chosen}
    if chosen['body_status'] not in ['agent_verified_transcription','independently_agent_verified_transcription']:
        result['use_rule']='正文尚未核验；先读取原页核验所需公式，再计算或绘图。'
    elif chosen.get('source_errata'):
        result['use_rule']='本节含原书疑误；必须同时阅读校注，不能直接使用被指出有误的原书数值或条件。'
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('query')
    args=p.parse_args()
    print(json.dumps(resolve(args.query),ensure_ascii=False,indent=2))
