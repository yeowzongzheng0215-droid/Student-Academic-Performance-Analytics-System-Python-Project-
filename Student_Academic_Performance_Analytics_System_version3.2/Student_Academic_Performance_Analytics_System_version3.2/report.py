# =========================
# Class 5: Report Generator
# =========================
# Aggregates all the statistics and writes them to a formatted
# text report file (Student_Report.txt).

class ReportGenerator:

    def __init__(self, dataframe):
        self.data = dataframe


    def generate_report(self):
        # Gather all the statistics needed for the report
        total_students = len(self.data)

        average_grade = self.data["G3"].mean()

        highest_grade = self.data["G3"].max()

        lowest_grade = self.data["G3"].min()


        pass_students = len(self.data[self.data["G3"] >= 10])

        fail_students = len(self.data[self.data["G3"] < 10])


        # Pass/fail rates as percentages
        pass_rate = pass_students / total_students * 100
        fail_rate = fail_students / total_students * 100


        # Gender counts
        male = len(self.data[self.data["sex"]=="M"])

        female = len(self.data[self.data["sex"]=="F"])


        # Urban vs rural address counts
        urban = len(self.data[self.data["address"]=="U"])

        rural = len(self.data[self.data["address"]=="R"])


        # Count of excellent students (grade >= 18)
        excellent = len(self.data[self.data["G3"] >= 18])


        # Sort by grade descending and take the top 10
        top_students = self.data.sort_values(
            by="G3",
            ascending=False
        ).head(10)



        # Open (create/overwrite) the report file and write each section
        with open("Student_Report.txt","w") as file:


            # ---- Section 1: title + overall performance summary ----
            file.write(
"""
==================================================
          EduInsight Student Analytics Report
==================================================

Generated Report: Student Performance Analysis


==================================================
1. Academic Performance Summary
==================================================

"""
            )


            file.write(f"Total Students          : {total_students}\n")

            file.write(f"Average Final Grade     : {average_grade:.2f}\n")

            file.write(f"Highest Final Grade     : {highest_grade}\n")

            file.write(f"Lowest Final Grade      : {lowest_grade}\n\n")




            # ---- Section 2: pass/fail analysis ----
            file.write(
"""
==================================================
2. Pass and Fail Analysis
==================================================

"""
            )

            file.write(f"Pass Students           : {pass_students}\n")

            file.write(f"Fail Students           : {fail_students}\n")

            file.write(f"Pass Rate               : {pass_rate:.2f}%\n")

            file.write(f"Fail Rate               : {fail_rate:.2f}%\n\n")




            # ---- Section 3: demographic statistics (gender / urban-rural) ----
            file.write(
"""
==================================================
3. Student Demographic Statistics
==================================================

"""
            )


            file.write(f"Male Students           : {male}\n")

            file.write(f"Female Students         : {female}\n")

            file.write(f"Urban Students          : {urban}\n")

            file.write(f"Rural Students          : {rural}\n\n")




            # ---- Section 4: excellent-student (scholarship) analysis ----
            file.write(
"""
==================================================
4. Excellent Student Analysis
==================================================

"""
            )


            file.write(f"Students with Grade >=18 : {excellent}\n\n")




            # ---- Section 5: top 10 students list ----
            file.write(
"""
==================================================
5. Top 10 Performing Students
==================================================

Rank    ID    School    Gender    Grade

"""
            )


            rank = 1

            # Iterate the top 10 students and write one line each.
            # index+1 converts the 0-based DataFrame index into a 1-based "student number"
            for index,row in top_students.iterrows():

                file.write(
                    f"{rank:<8}{index+1:<6}"
                    f"{row['school']:<10}"
                    f"{row['sex']:<10}"
                    f"{row['G3']}\n"
                )

                rank += 1




            # ---- Report footer ----
            file.write(
"""
==================================================
End of Report
==================================================
"""
            )


        print("\nReport Generated Successfully!")
        print("File saved as Student_Report.txt")

        # Try to auto-open the report (os.startfile only works on Windows).
        # On other OSes or if it fails, just tell the user to open it manually.
        import os
        try:
            os.startfile("Student_Report.txt")
        except:
            print("Report saved. Open Student_Report.txt to view.")
