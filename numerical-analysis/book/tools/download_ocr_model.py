#!/usr/bin/env python3
"""Download public model weights only. No document is uploaded."""
from pathlib import Path
import os
import json

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / '.work' / 'huggingface')
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'
from huggingface_hub import HfApi, snapshot_download

repo = 'mlx-community/GLM-OCR-bf16'
revision = HfApi().model_info(repo).sha
target = ROOT / '.work' / 'models' / 'GLM-OCR-bf16'
snapshot_download(repo, revision=revision, local_dir=target,
                  allow_patterns=['*.json', '*.safetensors', '*.model', '*.txt', '*.jinja', 'README.md'])
record = {'model': repo, 'revision': revision, 'local_dir': str(target.relative_to(ROOT)),
          'precision': 'bf16', 'documents_uploaded': False}
(ROOT / 'quality').mkdir(exist_ok=True)
(ROOT / 'quality' / 'ocr-model.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(record, ensure_ascii=False))
