# 🤖 Task Automation with Python Scripts — CodeAlpha Task 3

A professional automation toolkit with **3 tools** built into one script.

## Tools Included

### Tool 1 — Move JPG Files 📁
Scans a source folder and moves all `.jpg`/`.jpeg` files into a new destination folder.

### Tool 2 — Extract Email Addresses 📧
Reads a `.txt` file, finds all valid email addresses using Regex, removes duplicates, and saves them to an output file.

### Tool 3 — Scrape Webpage Title 🌐
Fetches any webpage URL and extracts the `<title>` tag, then saves it to a `.txt` file.

---

## How to Run

### Install dependency (Tool 3 only)
```bash
pip install requests
```

### Run the script
```bash
python task_automation.py
```

### Demo mode
Choose option `[4]` in the menu to run all 3 tools automatically using sample data.

---

## Concepts Used
`os` · `shutil` · `re` · `requests` · `file handling` · `functions` · `regex`

## Folder Structure
```
CodeAlpha_TaskAutomation/
├── task_automation.py       ← Main script
├── sample_files/
│   └── emails.txt           ← Sample input for Tool 2
├── jpg_moved/               ← Created by Tool 1 (auto)
├── extracted_emails.txt     ← Created by Tool 2 (auto)
└── webpage_title.txt        ← Created by Tool 3 (auto)
```

---
**CodeAlpha Python Internship**
