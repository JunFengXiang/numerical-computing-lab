from pathlib import Path
import hashlib, json
BOOK=Path(__file__).resolve().parents[2]
LANE=BOOK/'staging/front'
SOURCE='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'

def save(n, printed, content, headings=None, notes=None):
    path=LANE/'pages'/f'pdf-{n:03}.md'
    pstr='null' if printed is None else str(printed)
    path.write_text(f'''---
pdf_page: {n}
printed_page: {pstr}
source_image: source-images/pdf-{n:03}.jpeg
source_sha256: {SOURCE}
status: agent_reviewed_transcription
---

[查看原页](../../../source-images/pdf-{n:03}.jpeg)

<!-- source-page: {n} -->

'''+content.strip()+'\n',encoding='utf-8')
    receipt=LANE/'review.json'
    data=json.loads(receipt.read_text()) if receipt.exists() else {'lane':'front','reviewer':'Codex agent front','human_review':False,'source_sha256':SOURCE,'pages':[],'unresolved':[],'source_errata':[],'validation_notes':[]}
    entry={'pdf_page':n,'printed_page':printed,'path':str(path.relative_to(BOOK)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_image_sha256':hashlib.sha256((BOOK/'source-images'/f'pdf-{n:03}.jpeg').read_bytes()).hexdigest(),'visual_review':'completed','content_coverage':'complete','headings':headings or [],'formula_ids':[],'figures':[],'tables':[],'notes':notes or []}
    data['pages']=[e for e in data['pages'] if e['pdf_page']!=n]+[entry]
    data['pages'].sort(key=lambda e:e['pdf_page'])
    receipt.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    save(1,None,r'''
普通高等教育“十三五”规划教材  
普通高等院校数学精品教材

十三五

获教育部高等学校优秀教材二等奖  
获全国优秀畅销书奖

# 数值分析

第 5 版

李庆扬　王能超　易大义　编

- 强调基本原理、基本理论，夯实基本素质
- 注重基本方法和技巧，提高应用能力
- 阐述严谨，脉络分明，深入浅出
- 反复锤炼，不断更新，长销 30 余年

华中科技大学出版社  
[http://www.hustp.com](http://www.hustp.com)

> 版式记录（agent 补充）：本页为封面，无印刷页码。“十三五”也出现在封面徽标及背景装饰中；完整图形与字样见原页。
''',[{'id':'front.cover','title':'数值分析（第5版）'}],['封面全部可见文字已对照原图；OCR 候选多出的“获奖”不见于原页，未采用。'])
    save(2,None,r'''
普通高等教育“十三五”规划教材  
普通高等院校数学精品教材

# 数值分析（第 5 版）

——数值算法分析与高效算法设计

李庆扬　王能超　易大义　编

华中科技大学出版社  
中国·武汉
''',[{'id':'front.title','title':'数值分析（第5版）——数值算法分析与高效算法设计'}],['扉页，无印刷页码；背面透印文字不属本页正文。'])
    save(3,None,r'''
# 内容提要

本书是为理工科院校各专业普遍开设的“数值分析”课程而编写的教材。其上篇内容包括插值与逼近、数值积分与数值微分、常微分方程与线性方程组的数值解法、矩阵的特征值与特征向量计算等。每章附有习题并在书末给出部分答案。

本书下篇（高效算法设计）以讲座形式介绍快速算法、并行算法与加速算法方面的几个典型案例，力图普及推广超级计算方面的基础知识。全书阐述严谨，脉络分明，深入浅出，便于教学。

本书可作为理工科院校应用数学、力学、物理、计算机等专业的教材，也可供从事科学计算的科技工作者参考。

## 图书在版编目（CIP）数据

数值分析／李庆扬，王能超，易大义编．—5 版．—武汉：华中科技大学出版社，2018.4  
ISBN 978-7-5680-3946-8

Ⅰ．①数…　Ⅱ．①李…　②王…　③易…　Ⅲ．①数值分析-高等学校-教材　Ⅳ．①O241

中国版本图书馆 CIP 数据核字（2018）第 060527 号

## 数值分析（第 5 版）

Shuzhi Fenxi

李庆扬　王能超　易大义　编

| 项目 | 内容 |
|:---|:---|
| 策划编辑 | 王汉江 |
| 责任编辑 | 王汉江 |
| 封面设计 | 原色设计 |
| 责任校对 | 张会军 |
| 责任监印 | 周治超 |
| 出版发行 | 华中科技大学出版社（中国·武汉） |
| 地址 | 武汉市东湖新技术开发区华工科技园 |
| 电话 | (027)81321913 |
| 邮编 | 430223 |
| 录排 | 武汉市洪山区佳年华文印部 |
| 印刷 | 武汉华工鑫宏印务有限公司 |
| 开本 | $710\,\mathrm{mm}\times1000\,\mathrm{mm}$　$1/16$ |
| 印张 | 20 |
| 字数 | 415 千字 |
| 版次 | 2018 年 4 月第 5 版第 1 次印刷 |
| 定价 | 39.80 元 |

华中出版

本书若有印装质量问题，请向出版社营销中心调换  
全国免费服务热线：400-6679-118　竭诚为您服务  
版权所有　侵权必究
''',[{'id':'front.summary','title':'内容提要'},{'id':'front.cip','title':'图书在版编目（CIP）数据'}],['版权页，无印刷页码。','CIP 分类号 O241 的首字为大写字母 O；省略号是原页书目著录符号。','出版信息表系原版双列信息的线性整理；“地址”为表格整理标签。'])
