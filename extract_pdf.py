"""
Simplified PDF extraction - extracts raw text from page ranges
for manual parsing and translation.
"""
import pdfplumber
import sys
import json
import os

PDF_PATH = "/Users/mushu/Documents/project/german-laguage/german-language/Goethe-Zertifikat_B1_Wortliste.pdf"
PROGRESS_FILE = "/Users/mushu/Documents/project/german-laguage/german-language/progress.json"


def extract_page_text(page_num):
    """Extract text from a single page."""
    with pdfplumber.open(PDF_PATH) as pdf:
        if page_num < 1 or page_num > len(pdf.pages):
            return None, None

        page = pdf.pages[page_num - 1]

        # Try word-level extraction with column separation
        words = page.extract_words(keep_blank_chars=True, x_tolerance=3)

        # Separate left/right columns (split at x=300)
        left_words = []
        right_words = []

        for w in words:
            entry_text = w["text"]
            entry = {
                "text": entry_text,
                "x0": round(w["x0"], 1),
                "top": round(w["top"], 1),
            }
            if w["x0"] < 300:
                left_words.append(entry)
            else:
                right_words.append(entry)

        # Group into lines and reconstruct text
        def reconstruct_column(col_words):
            if not col_words:
                return ""
            col_words = sorted(col_words, key=lambda w: (w["top"], w["x0"]))
            lines = []
            current_line = [col_words[0]]
            current_top = col_words[0]["top"]

            for w in col_words[1:]:
                if abs(w["top"] - current_top) <= 6:
                    current_line.append(w)
                else:
                    lines.append(" ".join(w["text"] for w in current_line))
                    current_line = [w]
                    current_top = w["top"]
            lines.append(" ".join(w["text"] for w in current_line))
            return "\n".join(lines)

        left_text = reconstruct_column(left_words)
        right_text = reconstruct_column(right_words)

        # Also get raw text as fallback
        raw_text = page.extract_text()

        return {
            "page": page_num,
            "left_column": left_text,
            "right_column": right_text,
            "raw_text": raw_text,
        }


def extract_page_range(start, end):
    """Extract text from a range of pages."""
    results = []
    for p in range(start, end + 1):
        data = extract_page_text(p)
        if data:
            results.append(data)
    return results


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {
        "last_page": 0,
        "completed_pages": [],
        "total_words": 0,
        "current_section": "",
    }


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        start = int(sys.argv[1])
        end = int(sys.argv[2]) if len(sys.argv) >= 3 else start
    else:
        start = 8
        end = 9

    results = extract_page_range(start, end)
    for r in results:
        print(f"\n{'='*70}")
        print(f"PAGE {r['page']}")
        print(f"{'='*70}")
        if r["left_column"]:
            print(f"\n--- LEFT COLUMN ---")
            print(r["left_column"][:3000])
        if r["right_column"]:
            print(f"\n--- RIGHT COLUMN ---")
            print(r["right_column"][:3000])
        if not r["left_column"] and not r["right_column"]:
            print(r["raw_text"][:3000])
