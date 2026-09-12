# 并行转录协议

唯一写入范围：staging/<lane>/。不得改 source-images、原 PDF、verified、中央索引、STATUS、tools 或别人的 lane。不得另启 GPU OCR，不下载模型、不提交 Git、不创建子 agent。root 正在本机顺序生成 ocr/glm-fullpage/pdf-NNN.md，已存在者可作底稿；OCR 漏行和符号错即使未触发截断也常见。

必须逐一打开指定范围每张 source-images/pdf-NNN.jpeg；放大辨认每个公式、表和脚注。原扫描是唯一文字依据；知识用于发现疑误而非替换原文。完整转录，不能以摘要、省略号、‘见图’替代原正文/公式/表格/习题。重复页眉、页脚可去掉但页码须记录。印刷目录和正文分清。跨页处只转录本页部分并说明续页，不要杜撰补完。中文标点、数学排版可规范，数学符号与英文大小写不可随意换。

每页文件 pages/pdf-NNN.md。YAML：pdf_page（数字），printed_page（原页目视核对，前言无编号可 null），source_image（从 book 根计 source-images/pdf-NNN.jpeg），source_sha256（原 PDF 哈希），status: agent_reviewed_transcription。YAML 后加原页链接 ../../../source-images/pdf-NNN.jpeg；保留实际章节标题层级，页内用 <!-- source-page: N --> 标记。公式行内 $...$，独立 $$...$$，编号用 \tag{原编号}，使用标准 amsmath。不要在单个 aligned 内放多个 tag；多条编号拆为独立块。图表原编号不可变。

图：用 Python/PIL 或 PyMuPDF 从原图裁切到 assets/，MD 用 ../assets/... 引用；注明原图，提供忠实可检索的图意和全部符号标签文字。不要创造函数和数值。数值表、公式表必须转成可读 Markdown 或 LaTeX 表格（不要只有图片）。保留算法步骤、习题全部条件和小题。

疑似原书错误：保留原式，另写‘校注（agent 补充）’，明确原书错误还是 OCR 错。不能确定的字标 [待核:...] 并记 unresolved，不能伪装已确定。文字与数学尽量二次对照完成后才写 review 状态；题目只转录不要代做。既有 verified 六节可参考且须回看原图，不改其文件。

每完成数页保存 review.json，最终格式：{"lane":"...","reviewer":"Codex agent <lane>","human_review":false,"source_sha256":"0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2","pages":[{"pdf_page":N,"printed_page":N-13,"path":"staging/<lane>/pages/pdf-NNN.md","sha256":"文件 SHA256","source_image_sha256":"图 SHA256","visual_review":"completed","content_coverage":"complete","headings":[{"id":"实际章节号如3.2.1","title":"原题名"}],"formula_ids":["..."],"figures":["..."],"tables":["..."],"notes":[]}],"unresolved":[],"source_errata":[],"validation_notes":[]}. 每页回执必须来自实际打开图片，不得批量捏造 reviewed。

可用 /usr/bin/python3（fitz/PIL）与 book/.venv-ocr/bin/python（SymPy、PyYAML、matplotlib）。采用 tools.view_image 来看本地页图；调用经 functions.exec 返回 image(result.image_url)。无需联网。最终反馈完成页数、未决项、疑误和回执路径；不要声称人工核验或绝对零错。
