# 📘 1A_adobe – PDF Outline Extractor

> 🚀 Submission for Adobe GenAI Hackathon – Round 1A  
> 🎯 Theme: *"Connecting the Dots Through Docs"*

## 🧠 Challenge Brief

PDFs are everywhere — but machines don't *understand* them the way humans do.  
Your mission: Build a tool that extracts a structured outline from a PDF — like a machine would.

This includes:
- ✅ **Title**
- ✅ **Headings** with levels (`H1`, `H2`, `H3`) and corresponding **page numbers**

This structured format powers smarter applications like:
- Semantic search
- Recommendations
- Content-aware summarization

---

## 📥 Input Specification

- Accepts a **PDF** file (max 50 pages)
- Parses and outputs:
  - Document Title
  - Headings with:
    - `level`: H1, H2, H3
    - `text`: Heading content
    - `page`: Page number

### 📤 Output Format (JSON)

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
