#!/usr/bin/env python3
"""Resume a local GLM-OCR candidate pass, saving each page independently.

This script never promotes content to verified. The raw output is immutable unless
--force is deliberately specified. Per-page metadata records truncation and hashes.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import os
import time
import importlib.metadata

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / '.work' / 'huggingface')
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


def numbers(value):
    pages = []
    for piece in value.split(','):
        pair = [int(x) for x in piece.split('-')]
        pages.extend(range(pair[0], pair[-1]+1))
    if any(p < 1 or p > 322 for p in pages):
        raise ValueError('PDF page numbers must be 1..322, inclusive.')
    return list(dict.fromkeys(pages))


def write_atomic(path, value):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(value)
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', default='1-322')
    parser.add_argument('--max-tokens', type=int, default=8192)
    parser.add_argument('--pass-name', default='glm-fullpage')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    dest = ROOT / 'ocr' / args.pass_name
    dest.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / 'source-manifest.json').read_text())
    model_meta = json.loads((ROOT / 'quality' / 'ocr-model.json').read_text())
    pending = [p for p in numbers(args.pages) if args.force or not (dest / f'pdf-{p:03d}.json').exists()]
    if not pending:
        print('All requested candidate pages already exist; none were reprocessed.')
        return
    import mlx.core as mx
    from mlx_vlm import load, generate
    from mlx_vlm.prompt_utils import apply_chat_template
    print(f'Loading local model; pending pages: {len(pending)}', flush=True)
    model, processor = load(str(ROOT / model_meta['local_dir']), trust_remote_code=False)
    prompt = apply_chat_template(processor, model.config, 'Text Recognition:', num_images=1)
    for num in pending:
        page = manifest['pages'][num-1]
        img = ROOT / page['image']
        if sha256(img.read_bytes()).hexdigest() != page['image_sha256']:
            raise ValueError(f'Original image checksum changed: {num}')
        start = time.monotonic()
        result = generate(model, processor, prompt, image=[str(img)],
                          max_tokens=args.max_tokens, temperature=0.0, verbose=False)
        elapsed = time.monotonic() - start
        raw = result.text
        count = getattr(result, 'generation_tokens', None)
        meta = {
            'pdf_page': num, 'source_image': page['image'],
            'source_sha256': manifest['source_sha256'], 'source_image_sha256': page['image_sha256'],
            'status': 'unverified_ocr_candidate', 'engine': 'GLM-OCR / MLX-VLM',
            'model': model_meta['model'], 'model_revision': model_meta['revision'],
            'mlx_vlm_version': importlib.metadata.version('mlx-vlm'),
            'prompt': 'Text Recognition:', 'temperature': 0.0,
            'max_tokens': args.max_tokens, 'generation_tokens': count,
            'possibly_truncated': count is None or count >= args.max_tokens,
            'elapsed_seconds': round(elapsed, 3),
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'raw_text_sha256': sha256(raw.encode()).hexdigest(), 'raw_text': raw,
        }
        md = ('---\nstatus: unverified_ocr_candidate\n'
              f'pdf_page: {num}\nsource_image: ../../{page["image"]}\n---\n\n'
              '> 未经逐页校对的 OCR 候选；数学符号和图表不得直接用于推导或绘图。\n\n'
              f'[查看原页](../../{page["image"]})\n\n'+raw+'\n')
        write_atomic(dest / f'pdf-{num:03d}.md', md)
        write_atomic(dest / f'pdf-{num:03d}.json', json.dumps(meta, ensure_ascii=False, indent=2)+'\n')
        # A small independent progress file avoids overwriting manual review status.
        done = len(list(dest.glob('pdf-*.json')))
        write_atomic(dest / 'progress.json', json.dumps({'candidate_pages': done, 'last_page': num,
                     'last_updated_utc': meta['created_utc'], 'verified_pages': 0}, indent=2)+'\n')
        print(json.dumps({k:meta[k] for k in ['pdf_page','generation_tokens','possibly_truncated','elapsed_seconds']}), flush=True)
        mx.clear_cache()


if __name__ == '__main__':
    main()
