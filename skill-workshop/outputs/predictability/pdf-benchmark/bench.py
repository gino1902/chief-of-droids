#!/usr/bin/env python3
"""Benchmark PDF text-extraction tools on the fixture PDFs.

Compares text-layer extractors on success, completeness (char count),
table/image awareness, encryption handling, and speed. The Claude Read
(vision) path is not run here; its result comes from the predictability runs
and is added in the report by hand. This measures the library/CLI tier only.
"""
import time, subprocess, sys, os

PDFS = [
    "/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/outputs/predictability/ingest-fixture/raw/transformation-story.pdf",
    "/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/outputs/predictability/ingest-fixture/raw/TSLA-Q1-2026-Update.pdf",
]

def timed(fn):
    t = time.perf_counter()
    try:
        out = fn()
        return time.perf_counter() - t, out, None
    except Exception as e:
        return time.perf_counter() - t, None, repr(e)

def pypdf_extract(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    if r.is_encrypted:
        r.decrypt("")
    return "".join((p.extract_text() or "") for p in r.pages), len(r.pages)

def pymupdf_extract(path):
    import fitz
    doc = fitz.open(path)
    txt = "".join(page.get_text() for page in doc)
    imgs = sum(len(page.get_images(full=True)) for page in doc)
    return txt, doc.page_count, imgs

def pdfplumber_extract(path):
    import pdfplumber
    txt, tables = [], 0
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt.append(page.extract_text() or "")
            tables += len(page.extract_tables())
        n = len(pdf.pages)
    return "\n".join(txt), n, tables

def pdfminer_extract(path):
    from pdfminer.high_level import extract_text
    return extract_text(path), None

def pdftotext_extract(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"],
                         capture_output=True, text=True, timeout=120)
    return out.stdout, out.returncode

def pdfimages_count(path):
    out = subprocess.run(["pdfimages", "-list", path],
                         capture_output=True, text=True, timeout=120)
    lines = [l for l in out.stdout.splitlines() if l.strip()]
    return max(0, len(lines) - 2)  # minus 2 header lines

def run():
    for pdf in PDFS:
        name = os.path.basename(pdf)
        size_mb = os.path.getsize(pdf) / 1e6
        print(f"\n{'='*70}\n{name}  ({size_mb:.1f} MB)\n{'='*70}")

        dt, out, err = timed(lambda: pypdf_extract(pdf))
        if err: print(f"pypdf          ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pypdf          {len(out[0]):>7d} chars  {out[1]:>3d}p  {dt:5.2f}s")

        dt, out, err = timed(lambda: pymupdf_extract(pdf))
        if err: print(f"pymupdf(fitz)  ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pymupdf(fitz)  {len(out[0]):>7d} chars  {out[1]:>3d}p  {dt:5.2f}s  images={out[2]}")

        dt, out, err = timed(lambda: pdfplumber_extract(pdf))
        if err: print(f"pdfplumber     ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pdfplumber     {len(out[0]):>7d} chars  {out[1]:>3d}p  {dt:5.2f}s  tables={out[2]}")

        dt, out, err = timed(lambda: pdfminer_extract(pdf))
        if err: print(f"pdfminer.six   ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pdfminer.six   {len(out[0]):>7d} chars       {dt:5.2f}s")

        dt, out, err = timed(lambda: pdftotext_extract(pdf))
        if err: print(f"pdftotext      ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pdftotext(-lo) {len(out[0]):>7d} chars  rc={out[1]}  {dt:5.2f}s")

        dt, out, err = timed(lambda: pdfimages_count(pdf))
        if err: print(f"pdfimages      ERROR  {dt:5.2f}s  {err}")
        else:   print(f"pdfimages      embedded raster images = {out}")

if __name__ == "__main__":
    run()
