import fitz  # PyMuPDF
import os
import json
import re

def is_heading(span, prev_y, prev_size):
    """Heuristic: detect if the span looks like a heading."""
    text = span["text"].strip()
    if not text or len(text) < 2:
        return False

    # Bold fonts are more likely to be headings
    is_bold = "bold" in span["font"].lower()

    # Unusually large or upper-case words might indicate headings
    is_upper = text.isupper()
    size = span["size"]
    vertical_jump = abs(span["origin"][1] - prev_y) > (prev_size * 1.2)

    return is_bold or is_upper or vertical_jump or size > 14

def clean_text(text):
    """Remove unwanted whitespace and characters."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_title(doc):
    """Guess title from the first page."""
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]
    max_font = 0
    title = ""
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span['size'] > max_font and span['text'].strip():
                    max_font = span['size']
                    title = span['text'].strip()
    return clean_text(title)

def extract_headings(doc):
    outline = []
    prev_y = -1
    prev_size = 0

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = clean_text(span["text"])
                    if not text or len(text) < 3:
                        continue

                    if is_heading(span, prev_y, prev_size):
                        # Heuristic-based level classification
                        size = span["size"]
                        if size >= 20:
                            level = "H1"
                        elif size >= 16:
                            level = "H2"
                        elif size >= 13:
                            level = "H3"
                        else:
                            level = "H4"

                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

                    prev_y = span["origin"][1]
                    prev_size = span["size"]

    return outline

def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(".pdf"):
            continue

        input_path = os.path.join(input_dir, file_name)
        try:
            doc = fitz.open(input_path)
        except Exception as e:
            print(f"❌ Failed to open {file_name}: {e}")
            continue

        if len(doc) > 50:
            print(f"⚠️ Skipping {file_name}: too many pages ({len(doc)}).")
            continue

        title = extract_title(doc)
        headings = extract_headings(doc)

        result = {
            "title": title or "Untitled",
            "outline": headings
        }

        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Extracted: {file_name} → {output_path}")

if __name__ == "__main__":
    main()
