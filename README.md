<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:202124,55:1A73E8,100:4285F4&height=210&section=header&text=EduInsight&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Student%20Performance%20Analytics%20%26%20AI%20Feedback%20Suite&descAlignY=63&descSize=17" width="100%" alt="EduInsight Banner" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&duration=3000&pause=1000&color=4285F4&center=true&vCenter=true&width=720&lines=Modern+Desktop+Analytics+App+Built+with+Python+%26+PyWebView;395+Student+Records+%7C+Interactive+Charts+%7C+Cohort+KPIs;Local+Ollama+LLM+Commentary+with+Rule-Based+Fallback" alt="Typing Animation" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyWebView](https://img.shields.io/badge/UI-PyWebView-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%20CSS3%20JS-1A73E8?style=for-the-badge&logo=javascript&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Ollama](https://img.shields.io/badge/AI-Ollama_LLM-202124?style=for-the-badge&logo=ollama&logoColor=white)

<br/>

[Overview](#overview) •
[My Contributions](#contributions) •
[Features](#features) •
[Architecture](#architecture) •
[Project Structure](#structure) •
[Quick Start](#quickstart) •
[Team](#team)

</div>

---

<a id="overview"></a>
## 📌 Overview

**EduInsight** is a native desktop student-performance analytics application built with **Python, Pandas, PyWebView, and local Ollama LLM**. Based on the **UCI Student Performance Dataset** (`student-mat.csv`, 395 records), the project upgrades a legacy terminal/CustomTkinter utility into a clean, responsive desktop interface with interactive analytics, multi-mode student search, automated reporting, and personalized AI commentary.

| Cohort Metric | Value | Breakdown |
| :--- | :---: | :--- |
| **Total Students** | `395` | `187` Male · `208` Female \| `307` Urban · `88` Rural |
| **Average Final Grade (`G3`)** | `10.42 / 20` | Range `0` – `20` |
| **Pass Rate (`G3 ≥ 10`)** | `67.09%` | `265` Passed · `130` Failed |
| **Scholarship Eligible (`G3 ≥ 18`)** | `18` | Top `4.56%` high-achieving students |

---

<a id="contributions"></a>
## 🌟 My Role — UI/UX Redesign & AI Feedback Engine

In this 2-person group project, my primary responsibility was modernizing the desktop interface and building the local AI commentary system:

### 🎨 1. Modern Desktop UI Optimization (`gui.py` & `web/`)
* **PyWebView Migration:** Rebuilt the legacy UI into a responsive native desktop app (`1440×900`, min `1120×680`) powered by **HTML5 / CSS3 / JS** with zero external web-server setup.
* **Python–JS Bridge (`EduInsightAPI`):** Engineered a JSON-serializable bridge connecting backend Pandas analytics, student queries, and report exports directly to the frontend.
* **Cohesive Design System:** Defined a consistent Material-inspired palette for clear visual hierarchy and readability:

| Role | Token | Swatch |
| :--- | :---: | :---: |
| **Primary Accent** | `#4285F4` | ![#4285F4](https://img.shields.io/badge/Hex-4285F4-4285F4?style=flat-square) |
| **Hover / Active** | `#1A73E8` | ![#1A73E8](https://img.shields.io/badge/Hex-1A73E8-1A73E8?style=flat-square) |
| **Sidebar Surface** | `#202124` | ![#202124](https://img.shields.io/badge/Hex-202124-202124?style=flat-square) |
| **Canvas Background** | `#F8F9FA` | ![#F8F9FA](https://img.shields.io/badge/Hex-F8F9FA-F8F9FA?style=flat-square) |

### 🤖 2. AI Custom Commentary Engine (`ai_comment.py`)
* **Local Ollama Integration:** Connected `OllamaAI` (`localhost:11434`, default model `gemma4:e4b`) to generate tailored academic commentary for each student.
* **Structured Prompting:** Injects individual grades, prior failures, study time, absences, health rating, and weighted factors to output structured *Performance Level*, *Comment*, and *Recommendation* insights.
* **Graceful Fallback:** Automatically checks Ollama availability via `/api/tags` and seamlessly switches to deterministic rule-based commentary when offline.

---

<a id="features"></a>
## ✨ Key Features & Factor Weighting Model

* **📊 Analytics Dashboard:** Displays cohort KPIs, grade distributions, gender ratios, study-time vs. grade trends, and pass/fail breakdowns.
* **🔍 Multi-Mode Student Search:** Search by **Student ID (1–395)**, filter by **Final Grade (0–20)**, or list all **Scholarship-Eligible (`G3 ≥ 18`)** students.
* **🤖 AI Student Feedback:** Generates custom LLM feedback or rule-based analysis directly inside the student detail view.
* **🏆 Top 10 Leaderboard:** Ranks top-performing students across schools (`GP` / `MS`).
* **📄 Report Preview & Export:** Generates, previews, and exports the structured 5-section `Student_Report.txt`.
* **💻 Dual-Mode Support:** Run either the modern **PyWebView Desktop App (`gui.py`)** or the retained **Legacy CLI (`main.py`)**.

### ⚖️ 4-Factor Performance Weighting (`PerformanceAnalyzer`)

| Factor | Weight | Impact Scale | Evaluation Criteria |
| :--- | :---: | :---: | :--- |
| **Previous Failures** | `38%` | `████████░░` | Primary academic risk predictor; flags need for extra support |
| **Weekly Study Time** | `27%` | `██████░░░░` | 4-tier scale (`<2h`, `2–5h`, `5–10h`, `>10h`) |
| **Absences** | `22%` | `█████░░░░░` | Evaluates attendance consistency and disengagement risk |
| **Health Status** | `13%` | `███░░░░░░░` | 5-point self-reported scale (`Very Poor` to `Excellent`) |

---

<a id="architecture"></a>
## 🏗️ System Architecture

~~~mermaid
flowchart LR
    CSV[("student-mat.csv<br/>395 Student Records")] --> PD["Pandas DataFrame"]
    PD --> AN["PerformanceAnalyzer<br/>Stats and 4-Factor Model"]
    PD --> RP["ReportGenerator<br/>Student_Report.txt"]
    AN --> API["EduInsightAPI<br/>Python to JS Bridge"]
    RP --> API
    AN --> AI{"Ollama Running?<br/>localhost:11434"}
    AI -->|"Yes (gemma4:e4b)"| LLM["Local LLM Commentary"]
    AI -->|"Offline"| FB["Rule-Based Fallback"]
    LLM --> API
    FB --> API
    API --> UI["PyWebView Desktop App<br/>HTML / CSS / JS"]
~~~

---

<a id="structure"></a>
## 📂 Project Structure

~~~text
EduInsight/
├── gui.py                 # PyWebView desktop entry point & EduInsightAPI JS bridge
├── web/
│   ├── index.html         # Application layout shell
│   ├── styles.css         # Design system (#4285F4 / #202124) & responsive styles
│   └── app.js             # Interactive views, charts & backend API calls
├── ai_comment.py          # OllamaAI (gemma4:e4b) custom feedback & rule-based fallback
├── analyzer.py            # PerformanceAnalyzer: cohort metrics & 4-factor weighting
├── student.py             # Student base class & ExcellentStudent subclass (OOP)
├── report.py              # ReportGenerator: exports formatted Student_Report.txt
├── visualization.py       # Matplotlib chart helpers (used by legacy CLI)
├── main.py                # Legacy terminal interface (retained for compatibility)
├── student-mat.csv        # UCI student mathematics performance dataset (395 rows)
├── Student_Report.txt     # Generated analytics summary output
└── requirements.txt       # Python dependencies (pandas, requests, pywebview)
~~~

---

<a id="quickstart"></a>
## 🚀 Quick Start

### 1. Clone & Install Dependencies

~~~bash
git clone https://github.com/yeowzongzheng0215-droid/EduInsight.git
cd EduInsight
pip install -r requirements.txt
~~~

> [!NOTE]
> On Linux, PyWebView requires a native GUI backend such as GTK (`PyGObject` + GTK3) or Qt.

### 2. Optional — Enable Local AI Feedback (Ollama)

Install [Ollama](https://ollama.ai/), start the local server, and pull the configured model:

~~~bash
ollama serve
ollama pull gemma4:e4b
~~~

> [!TIP]
> If Ollama is not running, EduInsight automatically falls back to built-in analytical commentary without errors.

### 3. Run the Application

~~~bash
# Modern PyWebView Desktop App (Recommended)
python gui.py

# Legacy Terminal Mode
python main.py
~~~

---

<a id="team"></a>
## 👥 Team & Responsibilities

| Developer | Role | Key Contributions |
| :--- | :--- | :--- |
| **YEOW ZONG ZHENG** ([@yeowzongzheng0215-droid](https://github.com/yeowzongzheng0215-droid)) | **UI/UX & AI Integration** | PyWebView desktop UI migration (`gui.py`, `web/`), design system, Python–JS bridge (`EduInsightAPI`), Ollama LLM custom commentary & fallback engine (`ai_comment.py`) |
| **Project Teammate** | **Core Analytics & OOP** | OOP domain modeling (`student.py`), cohort statistics & 4-factor model (`analyzer.py`), legacy CLI (`main.py`), report export (`report.py`) |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4285F4,55:1A73E8,100:202124&height=110&section=footer" width="100%" alt="Footer Wave" />

</div>
