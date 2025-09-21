#!/usr/bin/env python3
"""
PDF Merger Script
-----------------
Merge multiple PDF files into a single PDF.

Usage:
  python pdf_merger.py -i file1.pdf file2.pdf ... -o merged.pdf
  python pdf_merger.py -d ./pdfs -o merged.pdf
  python pdf_merger.py -d ./pdfs -o merged.pdf --sort name
  python pdf_merger.py -d ./pdfs -o merged.pdf --sort mtime --reverse

Requirements:
  pip install PyPDF2

Notes:
  - Skips encrypted PDFs unless you provide --password.
  - Ignores non-PDF files quietly.
"""

import argparse
import os
from typing import List
from PyPDF2 import PdfReader, PdfWriter

def find_pdfs_in_dir(directory: str) -> List[str]:
    pdfs = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return pdfs

def sort_files(files: List[str], key: str, reverse: bool) -> List[str]:
    if key == "name":
        return sorted(files, key=lambda p: os.path.basename(p).lower(), reverse=reverse)
    elif key == "mtime":
        return sorted(files, key=lambda p: os.path.getmtime(p), reverse=reverse)
    elif key == "size":
        return sorted(files, key=lambda p: os.path.getsize(p), reverse=reverse)
    else:
        return files

def merge_pdfs(inputs: List[str], output: str, password: str = None, strict: bool = False) -> int:
    writer = PdfWriter()
    pages_added = 0
    for path in inputs:
        if not path.lower().endswith(".pdf"):
            continue
        if not os.path.exists(path):
            print(f"[WARN] Not found: {path}")
            continue
        try:
            reader = PdfReader(path)
            if reader.is_encrypted:
                if password:
                    try:
                        reader.decrypt(password)
                    except Exception as e:
                        print(f"[WARN] Could not decrypt {path}: {e}")
                        if strict:
                            raise
                        continue
                else:
                    print(f"[WARN] Encrypted PDF skipped (no password): {path}")
                    if strict:
                        raise RuntimeError(f"Encrypted PDF requires password: {path}")
                    continue
            for page in reader.pages:
                writer.add_page(page)
                pages_added += 1
            print(f"[OK] Added {len(reader.pages)} pages from {path}")
        except Exception as e:
            print(f"[ERROR] Failed to read {path}: {e}")
            if strict:
                raise

    if pages_added == 0:
        raise RuntimeError("No pages added. Check inputs.")
    with open(output, "wb") as f:
        writer.write(f)
    print(f"[DONE] Wrote {output} with {pages_added} pages.")
    return pages_added

def main():
    ap = argparse.ArgumentParser(description="Merge multiple PDFs into one.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("-i", "--inputs", nargs="+", help="List of PDF files to merge (in order).")
    src.add_argument("-d", "--directory", help="Directory to search for PDFs (recursively).")
    ap.add_argument("-o", "--output", required=True, help="Output PDF file path.")
    ap.add_argument("--sort", choices=["name", "mtime", "size"], default="name", help="Sort when using --directory.")
    ap.add_argument("--reverse", action="store_true", help="Reverse sort order.")
    ap.add_argument("--password", help="Password for encrypted PDFs (optional).")
    ap.add_argument("--strict", action="store_true", help="Fail on any error.")
    args = ap.parse_args()

    if args.inputs:
        files = [f for f in args.inputs if f.lower().endswith(".pdf")]
    else:
        files = find_pdfs_in_dir(args.directory)
        files = sort_files(files, key=args.sort, reverse=args.reverse)

    if not files:
        raise SystemExit("No PDF files found to merge.")

    print("[INFO] Files to merge in order:")
    for f in files:
        print(" -", f)
    merge_pdfs(files, args.output, password=args.password, strict=args.strict)

if __name__ == "__main__":
    main()
