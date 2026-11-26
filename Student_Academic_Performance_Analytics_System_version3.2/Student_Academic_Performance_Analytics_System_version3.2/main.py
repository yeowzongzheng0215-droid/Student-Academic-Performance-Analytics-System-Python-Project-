import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import subprocess
import warnings
warnings.filterwarnings('ignore')  # Suppress warning messages to keep console output clean

from student import Student, ExcellentStudent
from analyzer import PerformanceAnalyzer
from visualization import Visualization
from ai_comment import OllamaAI
from report import ReportGenerator

# =========================
# Helper Functions
# =========================

def pause():
    """Pause execution and wait for user input"""
    # Pause and wait for Enter before returning to the menu.
    # EOFError is caught for non-interactive environments (e.g. automated tests)
    # where input() would otherwise raise an error.
    try:
        input("\nPress Enter to return to menu...")
    except EOFError:
        pass

# =========================
# Main Program
# =========================

def main():
    """Main function to run the EduInsight Student Analytics System"""
    
    # Load Dataset
    # Read the dataset (semicolon-separated CSV - the standard format for
    # the UCI student performance dataset)
    try:
        data = pd.read_csv("student-mat.csv", sep=";")
        print("✓ Dataset loaded successfully!")
    except FileNotFoundError:
        print("Error: student-mat.csv not found.")
        return

    # Create Objects
    # Instantiate the feature-module objects once, reused for the whole program run
    analyzer = PerformanceAnalyzer(data)
    visual = Visualization(data)
    report = ReportGenerator(data)
    ollama_ai = OllamaAI()

    # Check Ollama availability
    # One-time check at startup just to inform the user; each actual AI call
    # re-checks availability on its own
    print("\n" + "="*50)
    print("      EduInsight Student Analytics System")
    print("="*50)
    if ollama_ai.check_ollama_running():
        print("\n✓ Ollama AI is running! AI-powered analysis is available.")
    else:
        print("\n⚠ Ollama AI is not running. Using built-in analysis.")
        print("  To enable AI features, install Ollama from https://ollama.ai")
        print("  Then run: ollama serve")
        print("  And pull a model: ollama pull llama2")

    # Main Menu Loop
    # Core interactive loop - dispatches to a feature branch based on the user's number choice
    while True:

        print("\n==================================================")
        print("      EduInsight Student Analytics System")
        print("==================================================")
        print("1. Search Student")
        print("2. Academic Performance Analysis")
        print("3. Student Statistics")
        print("4. Top Performing Students")
        print("5. Data Visualization")
        print("6. Generate Report")
        print("7. Exit")

        try:
            choice = int(input("\nEnter your choice: "))

        except ValueError:
            print("Please enter a valid number.")
            continue

        # ---------- Option 1: Student search submenu ----------
        if choice == 1:

            while True:

                print("\n========== Student Search ==========")
                print("1. Search by Student ID")
                print("2. Search by Grade")
                print("3. Search Scholarship Eligible Students")
                print("4. Back")

                try:
                    search_choice = int(input("\nEnter your choice: "))

                except ValueError:
                    print("Please enter a number.")
                    continue


                # Search by Student ID
                # Look up a single student by ID (a 1-based row number within the dataset)
                if search_choice == 1:

                    try:
                        student_id = int(input(f"\nEnter Student ID (1-{len(data)}): "))

                    except ValueError:
                        print("Please enter a valid Student ID.")
                        continue

                    if 1 <= student_id <= len(data):

                        # DataFrame indices are 0-based, user input is 1-based, hence -1
                        row = data.iloc[student_id - 1]
                        
                        # Create student object with all attributes
                        # If the grade qualifies, build an ExcellentStudent instead of a
                        # plain Student - this is polymorphism: both types support display_info()
                        if row["G3"] >= 18:

                            student = ExcellentStudent(
                                student_id,
                                row["school"],
                                row["age"],
                                row["sex"],
                                row["G3"],
                                row["failures"],
                                row["studytime"],
                                row["absences"],
                                row["health"]
                            )

                            print()
                            student.display_info()

                            student.scholarship()  # Extra check/announcement of scholarship eligibility

                        else:

                            student = Student(
                                student_id,
                                row["school"],
                                row["age"],
                                row["sex"],
                                row["G3"],
                                row["failures"],
                                row["studytime"],
                                row["absences"],
                                row["health"]
                            )

                            print()
                            student.display_info()


                        # =========================
                        # AI Performance Analysis
                        # =========================
                        
                        print("\n" + "="*50)
                        print("========== Performance Factors Analysis ==========")
                        print("="*50)
                        
                        # Get performance factors analysis
                        # Ask the analyzer for the 4-factor breakdown for this student
                        factors = analyzer.analyze_performance_factors(row)
                        
                        # Display factors
                        # Print each factor's name, weight, analysis and recommendation
                        for factor in factors:
                            print(f"\n{factor['factor']}")
                            print(f"  Importance: {factor['importance']}%")
                            print(f"  Analysis: {factor['analysis']}")
                            print(f"  Recommendation: {factor['recommendation']}")
                        
                        # Generate AI-powered analysis
                        # Package this student's key data and hand it to Ollama
                        # (or the fallback) to produce a written comment
                        print("\n" + "="*50)
                        print("========== Student Performance Comment ==========")
                        print("="*50)
                        
                        student_data_dict = {
                            'student_id': student_id,
                            'G3': row["G3"],
                            'failures': row["failures"],
                            'studytime': row["studytime"],
                            'absences': row["absences"],
                            'health': row["health"]
                        }
                        
                        ai_analysis = ollama_ai.generate_performance_analysis(student_data_dict, factors)
                        print(f"\n{ai_analysis}")
                        
                        print("="*50)

                    else:

                        print("Invalid Student ID.")



                # Search by Grade
                # List every student who got a specific grade
                elif search_choice == 2:

                    try:

                        grade = int(input("\nEnter Final Grade (0-20): "))

                    except ValueError:
                        print("Please enter a valid grade.")
                        continue

                    result = data[data["G3"] == grade]

                    if result.empty:

                        print("No student found.")


                    else:

                        print("\nStudents with Grade", grade)

                        print("--------------------------------")
                        print("ID\tSchool\tGender\tAge\tGrade")
                        print("--------------------------------")

                        for index, row in result.iterrows():

                            print(
                                index + 1,
                                "\t",
                                row["school"],
                                "\t",
                                row["sex"],
                                "\t",
                                row["age"],
                                "\t",
                                row["G3"]
                            )

                # List all students eligible for a scholarship (G3 >= 18)
                elif search_choice == 3:

                    print("\n========== Scholarship Eligible Students ==========")

                    scholarship_students = data[data["G3"] >= 18]


                    if scholarship_students.empty:

                        print("No scholarship eligible students found.")


                    else:

                        print("ID\tSchool\tGender\tAge\tGrade")
                        print("----------------------------------------")

                        for index, row in scholarship_students.iterrows():

                            print(
                                index + 1,
                                "\t",
                                row["school"],
                                "\t",
                                row["sex"],
                                "\t",
                                row["age"],
                                "\t",
                                row["G3"]
                            )


                elif search_choice == 4:

                    break  # Back to the main menu

            pause()

        # ---------- Option 2: Overall academic performance statistics ----------
        elif choice == 2:

            print("\n========== Academic Performance Analysis ==========")

            average = analyzer.average_grade()
            highest = analyzer.highest_grade()
            lowest = analyzer.lowest_grade()

            pass_count = analyzer.pass_students()
            fail_count = analyzer.fail_students()

            pass_rate = pass_count / len(data) * 100
            fail_rate = fail_count / len(data) * 100


            print("Average Grade:",round(average,2))

            print("Highest Grade:",highest)

            print("Lowest Grade:",lowest)

            print("Pass Students:",pass_count)

            print("Fail Students:",fail_count)

            print("Pass Rate:", round(pass_rate,2), "%")

            print("Fail Rate:", round(fail_rate,2), "%")

            pause()


        # ---------- Option 3: Student demographic statistics ----------
        elif choice == 3:

            print("\n========== Student Statistics ==========")

            total_students = len(data)

            male_students = len(data[data["sex"] == "M"])
            female_students = len(data[data["sex"] == "F"])

            urban_students = len(data[data["address"] == "U"])
            rural_students = len(data[data["address"] == "R"])

            average_age = round(data["age"].mean(), 2)

            excellent_students = len(data[data["G3"] >= 18])

            print("Total Students      :", total_students)
            print("Male Students       :", male_students)
            print("Female Students     :", female_students)
            print("Urban Students      :", urban_students)
            print("Rural Students      :", rural_students)
            print("Average Age         :", average_age)
            print("Excellent Students  :", excellent_students)

            pause()


        # ---------- Option 4: View the top 10 students ----------
        elif choice == 4:

            print("\n========== Top 10 Students ==========\n")

            top_students = data.sort_values(by="G3", ascending=False).head(10)

            print("ID\tSchool\tGender\tGrade")

            for index, row in top_students.iterrows():

                print(
                    index + 1,
                    "\t",
                    row["school"],
                    "\t",
                    row["sex"],
                    "\t",
                    row["G3"]
                )

            pause()

        # ---------- Option 5: Data visualization submenu ----------
        elif choice == 5:

            while True:

                print("\n========== Data Visualization ==========")
                print("1. Pass vs Fail Chart")
                print("2. Grade Distribution")
                print("3. Study Time Analysis")
                print("4. Back")

                try:
                    chart = int(input("\nEnter your choice: "))

                except ValueError:
                    print("Please enter a number.")
                    continue

                if chart == 1:
                    visual.pass_fail_chart()

                elif chart == 2:
                    visual.grade_distribution()

                elif chart == 3:
                    visual.study_time_chart()

                elif chart == 4:
                    break  # Back to the main menu

                else:
                    print("Invalid choice.")


        # ---------- Option 6: Generate the text report ----------
        elif choice == 6:

            report.generate_report()

            pause()


        # ---------- Option 7: Exit the program ----------
        elif choice == 7:

            print("\nThank you for using EduInsight Student Analytics System.")
            break


if __name__ == "__main__":
    main()