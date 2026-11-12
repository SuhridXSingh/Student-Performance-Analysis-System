import sys
import os
import pandas as pd
from src.models.student import Student
from src.exceptions.custom_exceptions import InvalidMarksError, RecordNotFound
from src.utils.file_manager import save_students_to_csv, load_students_from_csv, find_student_by_roll
from src.analysis.data_analyzer import (
    load_dataset, check_data_health, compute_summary_stats, 
    analyze_performance_by_groups, compute_correlation_matrix
)
from src.visualization.visualizer import generate_all_visualizations
from src.ml.model_trainer import StudentPerformanceModel, DEFAULT_MODEL_PATH
STUDENTS_CSV = "data/students.csv"
DATASET_CSV = "data/student_performance.csv"

def handle_add_student():
    try:
        name = str(input("Enter name of Student: "))
        age = int(input("Enter age: "))
        roll_number = int(input("Enter roll number: "))
        study_hours = float(input("Enter hours of study per week: "))
        attendance = float(input("Enter attendance percentage: "))
        participation = float(input("Enter class participation score: "))
        total_score = float(input("Enter total score: "))

        std = Student(name, age, roll_number, study_hours, attendance, participation, total_score)
        try:
            students = load_students_from_csv(STUDENTS_CSV)
        except RecordNotFound:
            students = []

        if any(s._roll_number == roll_number for s in students):
            print(f"\nError: Student with roll number {roll_number} already exists!")
            return
        
        students.append(std)
        save_students_to_csv(STUDENTS_CSV, students)
        print(f"Successfully added student {name} with roll {roll_number} to database.")
    
    except InvalidMarksError as e:
        print("Validation Error: "+ str(e))
    except ValueError:
        print("Input Error: Please enter valid numerical values for age, marks, and hours.")

def handle_search_student():
    try:
        roll = int(input("\nEnter roll number to search: "))
        student = find_student_by_roll(STUDENTS_CSV, roll)
        
        print("\n" + "-" * 40)
        print("Student Record Found:")
        print(f"Name:          {student.name}")
        print(f"Age:           {student.age}")
        print(f"Roll Number:   {student._roll_number}")
        print(f"Study Hours:   {student._study_hours} hrs/week")
        print(f"Attendance:    {student._attendance}%")
        print(f"Participation: {student._participation} / 10")
        print(f"Total Score:   {student._total_score} / 100")
        print(f"Grade:         {student.calc_grade()}")
        print("-" * 40)
    except RecordNotFound as e:
        print(f"\n{e}")
    except ValueError:
        print("\nInput Error: Roll number must be a valid integer.")

def handle_view_all_students():
    try:
        students = load_students_from_csv(STUDENTS_CSV)
        if not students:
            print("\n No student records found in the database.")
            return
        print("\n" + "=" * 80)
        print(f"{'Roll':<8} {'Name':<18} {'Age':<6} {'Hours':<8} {'Att%':<8} {'Part':<6} {'Score':<8} {'Grade':<6}")
        print("=" * 80)
        for s in students:
            print(f"{s._roll_number:<8} {s.name:<18} {s.age:<6} {s._study_hours:<8.1f} {s._attendance:<8.1f} {s._participation:<6.1f} {s._total_score:<8.1f} {s.calc_grade():<6}")
        print("=" * 80)
        print(f"Total Local Records: {len(students)}")
    except RecordNotFound:
        print("\n No database file found yet. Add a student first to create it.")

def handle_eda_analysis():
    if not os.path.exists(DATASET_CSV):
        print(f"\nDataset file not found at: {DATASET_CSV}")
        return
    print("\nLoading Kaggle dataset for Exploratory Data Analysis...")
    df = load_dataset(DATASET_CSV)
    print("\n" + "=" * 50)
    print("1. DATA INTEGRITY & HEALTH CHECK")
    print("=" * 50)
    check_data_health(df)
    print("\n" + "=" * 50)
    print("2. DESCRIPTIVE SUMMARY STATISTICS")
    print("=" * 50)
    summary_df, grade_dist = compute_summary_stats(df)
    print(summary_df)
    print("\n--- Grade Distribution Breakdown ---")
    print(grade_dist)
    print("\n" + "=" * 50)
    print("3. GROUP AGGREGATIONS")
    print("=" * 50)
    by_grade, by_hours = analyze_performance_by_groups(df)
    print("\n[Average Scores by Grade Category]")
    print(by_grade)
    print("\n[Average Scores by Study Hour Bracket]")
    print(by_hours)
    print("\n" + "=" * 50)
    print("4. FEATURE CORRELATION MATRIX")
    print("=" * 50)
    corr = compute_correlation_matrix(df)
    print(corr)

def handle_generate_visualizations():
    if not os.path.exists(DATASET_CSV):
        print(f"\nDataset file not found at: {DATASET_CSV}")
        return
    print("\nLoading dataset to generate visualization charts...")
    df = load_dataset(DATASET_CSV)
    saved = generate_all_visualizations(df)
    print("\nAll plots saved in high-res (300 DPI) to reports/figures/:")
    for name, path in saved.items():
        print(f"  • {name:<22} -> {path}")

def handle_predict_performance():
    model = StudentPerformanceModel(df=None, model_type="random_forest")
    if os.path.exists(DEFAULT_MODEL_PATH):
        try:
            model.load_model()
        except Exception:
            model.model = None
    if model.model is None:
        if not os.path.exists(DATASET_CSV):
            print(f"\nCannot train model: dataset missing at {DATASET_CSV}")
            return
        
        print("\n No pre-trained model found.")
        confirm = input("Train a new model on the dataset now? (y/n): ").strip().lower()
        if confirm != "y":
            print("Prediction aborted.")
            return
        
        print("Training model...")
        df = load_dataset(DATASET_CSV)
        model.df = df
        model.prep_data()
        model.train()
        model.save_model()
    
    try:
        print("\n--- Enter Student Profile for Prediction ---")
        study_hours = float(input("Enter weekly self-study hours (0 - 45): "))
        attendance = float(input("Enter attendance percentage (0 - 100): "))
        participation = float(input("Enter class participation score (0 - 10): "))
        if study_hours < 0 or study_hours > 50:
            raise ValueError("Study hours must be between 0 and 50.")
        if attendance < 0 or attendance > 100:
            raise InvalidMarksError(attendance)
        if participation < 0 or participation > 10:
            raise ValueError("Participation score must be between 0 and 10.")
        res = model.predict_student(study_hours, attendance, participation)
        print("\n" + "=" * 45)
        print("PREDICTION RESULTS")
        print("=" * 45)
        print(f"Predicted Total Score:  {res['predicted_score']} / 100")
        print(f"Predicted Grade Tier:   {res['predicted_grade']}")
        print("=" * 45)
    except InvalidMarksError as e:
        print(f"\nValidation Error: {e}")
    except ValueError as e:
        print(f"\nInput Error: {e}")

def display_menu():
    print("\n" + "=" * 55)
    print("STUDENT PERFORMANCE ANALYSIS & PREDICTION SYSTEM")
    print("=" * 55)
    print("1. Add New Student Record")
    print("2. Search Student by Roll Number")
    print("3. View All Student Records (CSV)")
    print("4. Run Exploratory Data Analysis (EDA)")
    print("5. Generate & Save Visualizations")
    print("6. Predict Student Performance (ML)")
    print("7. Exit")
    print("=" * 55)

def main():
    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            match choice:
                case "1":
                    handle_add_student()
                case "2":
                    handle_search_student()
                case "3":
                    handle_view_all_students()
                case "4":
                    handle_eda_analysis()
                case "5":
                    handle_generate_visualizations()
                case "6":
                    handle_predict_performance()
                case "7":
                    print("\nThank you for using the system. Goodbye!")
                    sys.exit(0)
                case _:
                    print("\n Invalid choice! Please enter a number between 1 and 7.")
        except KeyboardInterrupt:
            print("\n\nProcess interrupted. Exiting cleanly. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
if __name__ == "__main__":
    main()