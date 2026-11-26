import matplotlib.pyplot as plt

# =========================
# Class 4: Visualization
# =========================
# Responsible for generating charts (bar chart / histogram / line chart)

class Visualization:

    def __init__(self, dataframe):
        self.data = dataframe  # Reference to the dataset used for plotting

    def pass_fail_chart(self):
        # Bar chart comparing the number of passing vs failing students
        pass_students = len(self.data[self.data["G3"] >= 10])
        fail_students = len(self.data[self.data["G3"] < 10])

        plt.figure(figsize=(6,4))
        plt.bar(["Pass","Fail"], [pass_students, fail_students])

        # Bar chart
        plt.title("Student Pass and Fail Analysis")
        plt.xlabel("Result")
        plt.ylabel("Number of Students")
        plt.savefig(
    "pass_fail_chart.png"
)
        plt.close()  # Close the figure to free memory and avoid overlapping plots


    def grade_distribution(self):
        # Histogram showing how final grades (G3) are distributed across the class
        plt.figure(figsize=(7,4))
        plt.hist(self.data["G3"], bins=10)

        # Histogram
        plt.title("Student Final Grade Distribution")
        plt.xlabel("Final Grade")
        plt.ylabel("Number of Students")
        plt.savefig(
    "grade_distribution.png"
)

        plt.close()


    def study_time_chart(self):
        # Group students by study-time level, compute the average grade per group,
        # and plot it as a line chart to visualize the trend
        average_grade = self.data.groupby("studytime")["G3"].mean()

        plt.figure(figsize=(7,4))

        plt.plot(
            average_grade.index,
            average_grade.values,
            marker="o"
        )

        # Line chart
        plt.title("Study Time vs Average Grade")
        plt.xlabel("Study Time")
        plt.ylabel("Average Grade")
        plt.grid(True)

        plt.savefig(
    "study_time.png"
)


        plt.close()