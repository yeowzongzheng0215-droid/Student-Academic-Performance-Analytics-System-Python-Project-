# =========================
# Class 2: Performance Analyzer
# =========================
# Runs statistics on the whole dataset (DataFrame), and also provides
# a per-student "performance factor" breakdown (failures / study time / absences / health).

class PerformanceAnalyzer:

    def __init__(self, dataframe):
        self.data = dataframe  # Reference to the full student dataset

    def average_grade(self):
        # Mean of the final grade (G3) across all students
        return self.data["G3"].mean()

    def highest_grade(self):
        # Highest final grade in the dataset
        return self.data["G3"].max()

    def lowest_grade(self):
        # Lowest final grade in the dataset
        return self.data["G3"].min()

    def pass_students(self):
        # Count of students who passed (G3 >= 10)
        return len(self.data[self.data["G3"] >= 10])

    def fail_students(self):
        # Count of students who failed (G3 < 10)
        return len(self.data[self.data["G3"] < 10])

    def analyze_performance_factors(self, student_data):
        """Analyze performance factors for a specific student"""
        # Build a breakdown of the 4 key factors affecting this student's grade.
        # Each factor carries a fixed "importance" weight used purely for display.
        factors = []
        
        # Factor 1: Failures (Importance: 38%)
        # Highest weight - past failures are treated as the strongest predictor
        if student_data['failures'] > 0:
            factors.append({
                'factor': 'Failures',
                'importance': 38,
                'value': student_data['failures'],
                'analysis': f"Student has {student_data['failures']} previous failures, which may impact performance.",
                'recommendation': "Student should receive additional academic support."
            })
        else:
            factors.append({
                'factor': 'Failures',
                'importance': 38,
                'value': student_data['failures'],
                'analysis': "Student has no previous failures, which is positive.",
                'recommendation': "Maintain good academic performance to avoid failures."
            })
        
        # Factor 2: Study Time (Importance: 27%)
        study_time_map = {1: '<2 hours', 2: '2-5 hours', 3: '5-10 hours', 4: '>10 hours'}
        factors.append({
            'factor': 'Study Time',
            'importance': 27,
            'value': student_data['studytime'],
            'analysis': f"Weekly study time: {study_time_map.get(student_data['studytime'], 'Unknown')}",
            'recommendation': "Encourage students to increase their weekly study hours."
        })
        
        # Factor 3: Absences (Importance: 22%)
        factors.append({
            'factor': 'Absences',
            'importance': 22,
            'value': student_data['absences'],
            'analysis': f"Student has {student_data['absences']} absences.",
            'recommendation': "Students should maintain regular attendance."
        })
        
        # Factor 4: Health (Importance: 13%)
        # Lowest weight
        health_map = {1: 'Very Poor', 2: 'Poor', 3: 'Average', 4: 'Good', 5: 'Excellent'}
        factors.append({
            'factor': 'Health',
            'importance': 13,
            'value': student_data['health'],
            'analysis': f"Health condition: {health_map.get(student_data['health'], 'Unknown')}",
            'recommendation': "Schools should provide support for students with health issues."
        })
        
        return factors  # Return the list of 4 factor breakdowns, used for display and for the AI prompt
