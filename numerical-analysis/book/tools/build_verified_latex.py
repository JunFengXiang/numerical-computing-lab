#!/usr/bin/env python3
"""Compatibility entry point: export all 275 sections and the complete book."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--compile',action='store_true')
    args=p.parse_args()
    subprocess.run([sys.executable,str(ROOT/'tools/export_sections.py')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/export_book.py')]+(['--compile'] if args.compile else []),cwd=ROOT,check=True)

if __name__=='__main__':
    main()
