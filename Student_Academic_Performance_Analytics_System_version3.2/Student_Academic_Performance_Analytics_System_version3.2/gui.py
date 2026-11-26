"""EduInsight desktop app built with PyWebView (no CustomTkinter dependency)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd
import webview

from analyzer import PerformanceAnalyzer
from ai_comment import OllamaAI
from report import ReportGenerator

BASE_DIR = Path(__file__).resolve().parent


class EduInsightAPI:
    """Small, JSON-serialisable bridge exposed to the JavaScript interface."""

    def __init__(self):
        self.data = pd.read_csv(BASE_DIR / "student-mat.csv", sep=";")
        self.analyzer = PerformanceAnalyzer(self.data)
        self.ai = OllamaAI()
        self.report = ReportGenerator(self.data)

    @staticmethod
    def _clean(value):
        """Convert pandas/numpy scalar values to values JSON can carry."""
        if hasattr(value, "item"):
            return value.item()
        return value

    def get_dashboard(self):
        passed = self.analyzer.pass_students()
        total = len(self.data)
        grades = [int(x) for x in self.data["G3"].tolist()]
        study = self.data.groupby("studytime")["G3"].mean()
        gender = self.data["sex"].value_counts().to_dict()
        return {
            "total": total,
            "average": round(float(self.analyzer.average_grade()), 2),
            "highest": int(self.analyzer.highest_grade()),
            "lowest": int(self.analyzer.lowest_grade()),
            "passed": passed,
            "failed": self.analyzer.fail_students(),
            "pass_rate": round(passed / total * 100, 1),
            "excellent": int((self.data["G3"] >= 18).sum()),
            "grades": grades,
            "study_time": {str(int(k)): round(float(v), 2) for k, v in study.items()},
            "gender": {str(k): int(v) for k, v in gender.items()},
        }

    def get_student(self, student_id):
        try:
            student_id = int(student_id)
        except (TypeError, ValueError):
            return {"ok": False, "message": "Please enter a valid numeric Student ID."}
        if not 1 <= student_id <= len(self.data):
            return {"ok": False, "message": f"Student ID must be between 1 and {len(self.data)}."}

        row = self.data.iloc[student_id - 1]
        factors = self.analyzer.analyze_performance_factors(row)
        student_data = {
            "student_id": student_id, "G3": int(row["G3"]),
            "failures": int(row["failures"]), "studytime": int(row["studytime"]),
            "absences": int(row["absences"]), "health": int(row["health"]),
        }
        # AI module gracefully falls back to rule-based feedback if Ollama is unavailable.
        comment = self.ai.generate_performance_analysis(student_data, factors)
        return {
            "ok": True,
            "student": {
                "id": student_id, "school": str(row["school"]), "age": int(row["age"]),
                "gender": "Female" if row["sex"] == "F" else "Male", "grade": int(row["G3"]),
                "failures": int(row["failures"]), "studytime": int(row["studytime"]),
                "absences": int(row["absences"]), "health": int(row["health"]),
                "scholarship": bool(row["G3"] >= 18),
            },
            "factors": [{k: self._clean(v) for k, v in factor.items()} for factor in factors],
            "comment": comment,
        }

    def find_by_grade(self, grade):
        try:
            grade = int(grade)
        except (TypeError, ValueError):
            return {"ok": False, "message": "Grade must be a number from 0 to 20."}
        if not 0 <= grade <= 20:
            return {"ok": False, "message": "Grade must be between 0 and 20."}
        result = self.data[self.data["G3"] == grade]
        return {"ok": True, "students": self._student_rows(result)}

    def get_scholarship_students(self):
        return {"ok": True, "students": self._student_rows(self.data[self.data["G3"] >= 18])}

    def get_top_students(self):
        return self._student_rows(self.data.sort_values("G3", ascending=False).head(10))

    def _student_rows(self, frame):
        return [{
            "id": int(index + 1), "school": str(row["school"]),
            "gender": "Female" if row["sex"] == "F" else "Male",
            "age": int(row["age"]), "grade": int(row["G3"]),
        } for index, row in frame.iterrows()]

    def generate_report(self):
        """Create the original text report and return it for preview/download."""
        old_cwd = os.getcwd()
        try:
            os.chdir(BASE_DIR)
            self.report.generate_report()
            content = (BASE_DIR / "Student_Report.txt").read_text(encoding="utf-8")
            return {"ok": True, "filename": "Student_Report.txt", "content": content}
        except Exception as exc:
            return {"ok": False, "message": str(exc)}
        finally:
            os.chdir(old_cwd)

    def get_app_info(self):
        return {"dataset": "student-mat.csv", "students": len(self.data), "ollama": self.ai.check_ollama_running()}

    def close_app(self):
        """Close the native PyWebView window when the user chooses Exit."""
        if webview.windows:
            webview.windows[0].destroy()
        return {"ok": True}


def run():
    api = EduInsightAPI()
    window = webview.create_window(
        "EduInsight | Student Analytics",
        (BASE_DIR / "web" / "index.html").as_uri(),
        js_api=api,
        width=1440,
        height=900,
        min_size=(1120, 680),
        background_color="#F8F9FA",
    )
    webview.start(debug=False)


if __name__ == "__main__":
    run()
