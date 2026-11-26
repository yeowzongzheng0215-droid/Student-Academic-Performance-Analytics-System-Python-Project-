# EduInsight — PyWebView Edition

A desktop student-performance analytics application rebuilt from the original CustomTkinter interface using **PyWebView + HTML/CSS/JavaScript**.  The application keeps the existing Python analysis, Ollama fallback, report generation and `student-mat.csv` dataset, while presenting them in a professional, minimal desktop interface.

## Design system

| Token | Value |
| --- | --- |
| Primary | `#4285F4` |
| Sidebar | `#202124` |
| Background | `#F8F9FA` |
| Card | `#FFFFFF` |
| Hover | `#1A73E8` |

## Features

- Dashboard with cohort KPIs, grade distribution and pass/fail overview
- Student lookup by ID with profile, factor analysis and AI/rule-based comment
- Search by final grade and scholarship-eligible student list
- Analytics screen with visual trends and top-10 table
- Report preview, local `Student_Report.txt` generation and download
- Ollama integration when it is available; reliable built-in analysis otherwise

## Installation and launch

```bash
pip install -r requirements.txt
python gui.py
```

Run the command from this project folder. On Linux, PyWebView also needs a GUI backend such as GTK (`PyGObject`/GTK3) or Qt. The native desktop window is opened by PyWebView; no web server is needed.

## Project structure

```text
gui.py                 Python PyWebView entry point and JS API bridge
web/index.html         application shell
web/styles.css         professional visual system
web/app.js             client-side views and charts
analyzer.py            existing analytics logic
ai_comment.py          Ollama / fallback student comments
report.py              report generator
student-mat.csv        student data
```

The legacy terminal `main.py` is retained for compatibility. `gui.py` is now fully PyWebView and has no CustomTkinter imports.
