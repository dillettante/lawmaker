#!/usr/bin/env python3
"""Chunked, page-marked docling extraction for the lawmaker skill build.

Stable config for born-digital Korean legal PDFs on Python 3.14 + docling:
  - do_ocr=False  : rapidocr(PP-OCRv6) model mismatch crashes docling, and these
                    PDFs are born-digital so OCR is unnecessary.
  - 10-page chunks: whole-document conversion crashes on large books (memory);
                    chunking bounds it and yields page ranges for citations.
  - single-thread + KMP_DUPLICATE_LIB_OK: torch/opencv both link libomp on macOS
                    (OMP Error #15); this avoids the abort.

Emits per-doc markdown with `===== [원문: <label> p.N-M] =====` page markers so the
generated chapters can carry `원문 근거: p.NN` pointers, plus a combined full_text.txt
and metadata.json.

Usage:
  python3 build/extract_docling.py <out_dir> "<label>=<pdf_path>" ["<label>=<pdf>" ...]

Note: avoid glob metacharacters ( [ ] * ? ) in the PDF path — docling globs its input.
Copy the file to a plain path first if needed.
"""
import os, sys, json, time

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pypdf import PdfReader

CHUNK = 10


def build_converter():
    opts = PdfPipelineOptions()
    opts.do_ocr = False
    opts.do_table_structure = True
    return DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})


def extract(out_dir, docs):
    os.makedirs(out_dir, exist_ok=True)
    conv = build_converter()
    sources, combined = [], []
    for i, (label, path) in enumerate(docs):
        n = len(PdfReader(path).pages)
        print(f"[{label}] {n} pages -> chunks of {CHUNK}", flush=True)
        parts, t0 = [], time.time()
        for s in range(1, n + 1, CHUNK):
            e = min(s + CHUNK - 1, n)
            try:
                md = conv.convert(path, page_range=(s, e)).document.export_to_markdown()
            except Exception as ex:  # keep going; a failed chunk is visible in output
                md = f"[EXTRACTION FAILED p.{s}-{e}: {type(ex).__name__}: {ex}]"
                print(f"  ! chunk {s}-{e} failed: {ex}", flush=True)
            parts.append(f"\n\n===== [원문: {label} p.{s}-{e}] =====\n\n{md}")
            print(f"  p.{s}-{e} done ({time.time()-t0:.0f}s)", flush=True)
        doc_md = f"# {label}\n" + "".join(parts)
        out = os.path.join(out_dir, f"p{i+1}.md")
        with open(out, "w") as f:
            f.write(doc_md)
        sources.append({"label": label, "pages": n, "words": len(doc_md.split()),
                        "tokens_est": len(doc_md) // 3, "md_file": os.path.basename(out)})
        combined.append(f"\n\n################ {label} ################\n{doc_md}")
        print(f"[{label}] done -> {out}", flush=True)
    full = "".join(combined)
    with open(os.path.join(out_dir, "full_text.txt"), "w") as f:
        f.write(full)
    meta = {"sources": sources,
            "total_pages": sum(s["pages"] for s in sources),
            "total_words": len(full.split()),
            "estimated_tokens": len(full) // 3,
            "extraction_mode": "technical(docling,do_ocr=False,chunk10,pagemarkers)"}
    with open(os.path.join(out_dir, "metadata.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("=== DONE ===")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


def main(argv):
    if len(argv) < 3:
        print('usage: extract_docling.py <out_dir> "<label>=<pdf>" ["<label>=<pdf>" ...]', file=sys.stderr)
        return 2
    out_dir = argv[1]
    docs = []
    for a in argv[2:]:
        label, sep, path = a.partition("=")
        if not sep or not path:
            print(f"bad arg (need label=path): {a}", file=sys.stderr)
            return 2
        docs.append((label, path))
    extract(out_dir, docs)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
