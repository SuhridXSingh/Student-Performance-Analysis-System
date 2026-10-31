import csv
import os
from src.exceptions.custom_exceptions import RecordNotFound
from src.models.student import Student

HEADERS = ["name", "age", "roll_number", "study_hours", "attendance", "participation", "total_score", "grade"]

def save_students_to_csv(filepath, students):
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow(["Name", "Age", "Roll Number", "Total Score", "Grade"])

            for student in students:
                writer.writerow([
                    student.name,
                    student.age,
                    student._roll_number,
                    student._total_score,
                    student.calc_grade()
                ])
    except RecordNotFound as e:
        return f"{e}"

def load_students_from_csv(filepath):
    