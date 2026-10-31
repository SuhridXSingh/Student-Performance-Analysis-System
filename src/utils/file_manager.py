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

            writer.writerow(HEADERS)

            for student in students:
                writer.writerow([
                    student.name,
                    student.age,
                    student._roll_number,
                    student._study_hours,
                    student._attendance,
                    student._participation,
                    student._total_score,
                    student.calc_grade()
                ])
    except (IOError, OSError) as e:
        return f"{e}"

def load_students_from_csv(filepath):
    if not os.path.exists(filepath):
        raise RecordNotFound(f"Database file not found: {filepath}")

    students = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            student = Student(
                name=row['name'],
                age=int(row['age']),
                roll_number=int(row['roll_number']),
                study_hours=float(row['study_hours']),
                attendance=float(row['attendance']),
                participation=float(row['participation']),
                total_score=float(row['total_score'])
            )
            students.append(student)

    return students

def find_student_by_roll(filepath, roll_number):
    students = load_students_from_csv(filepath)

    for student in students:
        if student._roll_number == int(roll_number):
            return student

    raise RecordNotFound(roll_number)