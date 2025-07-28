# 📘 PDF Outline Extractor – Adobe GenAI Hackathon (Round 1A)

> 🎯 Challenge: **Understand Your Document**  
> 🧩 Theme: *"Connecting the Dots Through Docs"*

## 🧠 Problem Statement

You’re given a PDF. Your task is to extract a structured outline like a machine would:
- Extract the **Title**
- Extract all headings (**H1, H2, H3**) along with their **levels** and **page numbers**
- Output the result in a structured **JSON** format.

---

## ✅ Our Approach

We designed a lightweight and fast rule-based solution without heavy ML models. Here's how it works:

### 📊 1. Font-Based Heuristics
- Analyze **font sizes** and **styles** (bold, position, size) using `PyMuPDF`.
- Cluster font sizes to define H1, H2, H3 levels.
- Headings are detected based on:
  - Large, bold text
  - Distance from other blocks
  - Position on the page (left-aligned = heading)

### 🏷️ 2. Title Extraction
- The **largest centered or top-left text** on Page 1 is selected as the title.
- We avoid generic titles like "Table of Contents" or "Abstract" using keyword filters.

### 📦 3. JSON Output
- Data is saved in the following format:
```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Main Section", "page": 1 },
    { "level": "H2", "text": "Subsection", "page": 2 },
    { "level": "H3", "text": "Detail", "page": 2 }
  ]
}
