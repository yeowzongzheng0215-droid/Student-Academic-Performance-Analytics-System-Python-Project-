# =========================
# Class 1: Student
# =========================
# Base class representing a single student's core attributes,
# with a method to print them out nicely.

class Student:

    def __init__(self, student_id, school, age, sex, grade, failures, studytime, absences, health):
        # student_id here is actually the row number the user entered, not a real database ID
        self.student_id = student_id
        self.school = school        # School the student attends
        self.age = age              # Age
        self.sex = sex              # Gender
        self.grade = grade          # Final grade (G3)
        self.failures = failures    # Number of past class failures
        self.studytime = studytime  # Weekly study time (scale 1-4)
        self.absences = absences    # Number of absences
        self.health = health        # Health status (scale 1-5)

    def display_info(self):
        # Print all of the student's attributes in a readable format
        print("--------------------")
        print("Student ID:", self.student_id)
        print("School:", self.school)
        print("Age:", self.age)
        print("Gender:", self.sex)
        print("Final Grade:", self.grade)
        print("Previous Failures:", self.failures)
        print("Weekly Study Time:", self.studytime, "hours")
        print("Absences:", self.absences)
        print("Health Status:", self.health)


# =========================
# Class 3: ExcellentStudent (Inheritance)
# =========================
# Subclass of Student representing a top-performing student who
# may qualify for a scholarship. Demonstrates class inheritance.

class ExcellentStudent(Student):

    def scholarship(self):
        # Check whether this student meets the scholarship threshold (grade >= 18)
        if self.grade >= 18:
            print("\nScholarship Eligible!")