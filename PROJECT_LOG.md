# Student Performance Analysis System - Project Log & Roadmap

## 1. Project Overview & Scope
A modular Python application designed for university coursework adhering strictly to syllabus Units I, II, and III:
- **Unit I**: Environment, data types, control flow, functions, basic file I/O, error handling.
- **Unit II**: Advanced functions (`*args`, `**kwargs`, `lambda`, `map`/`filter`), OOP (inheritance, encapsulation), custom exceptions (`raise`, `finally`).
- **Unit III**: NumPy, Pandas, Matplotlib, Seaborn, and Scikit-learn (classifiers / regressors).

---

## 2. Decision Log
- **UI Decision**: Start with an **interactive CLI menu** first. 
  - *Rationale*: Guarantees 100% adherence to Units I & II (loops, input, custom exceptions, OOP dispatch). The core logic will be decoupled into modules/classes so a Streamlit UI or Jupyter Notebook can be effortlessly added later as a bonus layer.
- **Role Alignment**: Collaborative pair-programming and mentorship. The AI provides structural templates, reviews, feedback, and concept explanations, while the user writes and masters the implementation.

---

## 3. High-Level Architecture & Modules
```text
student_performance_analysis/
│
├── data/                         # CSV datasets (raw / processed)
│   ├── students.csv
│   └── student_performance_kaggle.csv
│
├── src/
│   ├── models/                   # Unit II: OOP classes (Student, GradeCalculator, etc.)
│   ├── exceptions/               # Unit II: Custom exception definitions
│   ├── analysis/                 # Unit III: Pandas & NumPy data operations
│   ├── visualization/            # Unit III: Matplotlib & Seaborn plots
│   ├── ml/                       # Unit III: Scikit-learn training & inference
│   └── utils/                    # Unit I: File I/O helpers, validation
│
├── main.py                       # Unit I & II: CLI entrypoint & menu loop
├── PROJECT_LOG.md                # Progress tracker & decisions
└── requirements.txt              # Virtualenv dependencies
```

---

## 3.5 Dataset Selection & Feature Analysis
**Source:** [Student Performance Dataset – Kaggle](https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset)
**Size:** 1,000,000 rows (synthetic, realistic)
**Selected:** 2026-10-29

### Columns
| Column | Type | Range | Description |
| :--- | :--- | :--- | :--- |
| `student_id` | int | unique | Unique student identifier |
| `weekly_self_study_hours` | float | 0–40 | Average weekly self-study hours |
| `attendance_percentage` | float | 50–100 | Class attendance % |
| `class_participation` | float | 0–10 | Active participation score |
| `total_score` | float | 0–100 | Final performance score (target for regression) |
| `grade` | str | A/B/C/D/F | Categorical label (target for classification) |

### Grade Thresholds (from dataset)
- **A:** ≥ 85 | **B:** ≥ 70 | **C:** ≥ 55 | **D:** ≥ 40 | **F:** < 40

### ML Task Mapping
- **Classification:** Predict `grade` (A–F) from study hours + attendance + participation
- **Regression (bonus):** Predict `total_score` from the same features

---

## 4. Phase-wise Roadmap & Checklist

### Phase 1: Project Setup & Custom Exceptions (Unit I & II)
- [x] Create virtual environment & `requirements.txt` ✅ (Completed 2026-10-28)
- [x] Define custom exceptions (`InvalidMarksError`, `RecordNotFound`) ✅ (Completed 2026-10-29, took 2 review rounds)

### Phase 2: Core OOP & Student Grading (Unit I & II)
- [x] Implement `Person` base class and `Student` subclass (encapsulation & inheritance) ✅ (Completed 2026-10-29)
- [x] Grading logic using functional programming (`filter`, `lambda`, `next`) ✅ (Completed 2026-10-31)
- [x] File I/O manager to save and load student records via CSV/JSON (`with open...`) ✅ (Completed 2026-10-31)

### Phase 3: Exploratory Data Analysis (EDA) (Unit III)
- [x] Load student dataset into Pandas DataFrame ✅ (Completed 2026-11-06)
- [x] Summary statistics, grouping by study hours/attendance with NumPy & Pandas ✅ (Completed 2026-11-06)
- [x] Matplotlib & Seaborn visualizations (grade distribution, correlation heatmaps, boxplots) ✅ (Completed 2026-11-10)

### Phase 4: Machine Learning Model (Unit III)
- [x] Train regression model (Linear Regression & Random Forest) to predict score ✅ (Completed 2026-11-11)
- [x] Model evaluation (MAE, RMSE, R2) with stratified splitting on grade distribution ✅ (Completed 2026-11-11)
- [x] Function to predict score and grade for a new student profile (`predict_student`) ✅ (Completed 2026-11-11)

### Phase 5: CLI Integration & Polish
- [x] Interactive CLI menu binding all components (`main.py`) ✅ (Completed 2026-11-12)
- [x] Robust error handling for all user inputs (`InvalidMarksError`, `RecordNotFound`, `ValueError`) ✅ (Completed 2026-11-12)
- [x] Interactive Streamlit web dashboard in `app.py` (zero emojis, publication theme) ✅ (Completed 2026-11-12)

---

## 5. Session Log & Handover Notes

### Session 1 (2026-10-28 to 2026-10-29) - Summary of Accomplishments:
1. **Environment Setup (Phase 1):**
   - Configured `.venv`, fixed `requirements.txt` dependencies (`scikit-learn`, `matplotlib`, `seaborn`), and successfully installed all packages.
2. **Custom Exceptions (Phase 1):**
   - Implemented `src/exceptions/custom_exceptions.py` with base class `BaseAppExceptions` and subclasses `InvalidMarksError` and `RecordNotFound`. Verified import and exception raising.
3. **Dataset Selection & Verification (Phase 3 Prep):**
   - Downloaded and placed `student_performance.csv` (1,000,000 rows, Kaggle) in `data/`. Verified headers (`weekly_self_study_hours`, `attendance_percentage`, `class_participation`, `total_score`, `grade`).
4. **Core OOP Modeling (Phase 2):**
   - Implemented `src/models/student.py` featuring `Person` (encapsulation with `@property`) and `Student` subclass (inheritance via `super().__init__`, score & attendance validation, and `calc_grade()`). Verified execution and exception handling from project root.

### Session 2 (2026-10-31) - Summary of Accomplishments:
1. **Functional Grading Logic (Phase 2):**
   - Refactored `Student.calc_grade()` using `lambda`, `filter()`, and `next()` with fallback defaults, replacing `if/elif` branching.
2. **Student Persistence & File I/O (Phase 2):**
   - Created `src/utils/file_manager.py` with `save_students_to_csv()`, `load_students_from_csv()`, and `find_student_by_roll()`.
   - Implemented context managers (`with open...`), `csv.DictReader` deserialization, and custom `RecordNotFound` handling.
   - Tested happy paths, file existence errors, and search misses with 100% pass rate.
3. **Repository Cleanliness:**
   - Separated mentor performance evaluation to `.gitignore`.

### Session 3 (2026-11-06) - Summary of Accomplishments:
1. **Data Ingestion & Integrity Checks (Phase 3 - Unit III):**
   - Implemented `load_dataset()` and `check_data_health()` in `src/analysis/data_analyzer.py`. Verified zero missing values across 1M rows.
2. **Statistical Analysis & Group Aggregations (Phase 3 - Unit III):**
   - Implemented `compute_summary_stats()` computing mean, median, sample std (`ddof=1`), quartiles (Q1, Q3), and IQR with Pandas and NumPy, excluding identifiers (`student_id`).
   - Implemented `analyze_performance_by_groups()` with grade breakdown and study hours binning via `pd.cut()` (`0-10h`, `10-20h`, `20-30h`, `30-40h+`).
   - Implemented `compute_correlation_matrix()`. Discovered key insight: strong positive correlation (**0.81**) between `weekly_self_study_hours` and `total_score`.
   - Verified 100% test execution on 1,000,000 records in under 3 seconds.

### Session 4 (2026-11-10) - Summary of Accomplishments:
1. **Visualization Module (Phase 3 - Unit III):**
   - Implemented `src/visualization/visualizer.py` with Matplotlib and Seaborn.
   - Built 4 automated plotting functions:
     - `plot_grade_distribution()`: Categorical count plot with count & percentage annotations on each bar.
     - `plot_correlation_heatmap()`: Annotated Pearson correlation matrix heatmap (`coolwarm`).
     - `plot_study_hours_vs_score()`: Box plot illustrating score distribution across binned study hours.
     - `plot_score_distribution()`: Histogram + KDE density curve with mean and median benchmark lines.
     - `generate_all_visualizations()`: Automated pipeline saving publication-grade 300 DPI figures to `reports/figures/`.
   - Verified end-to-end execution on 1M rows with zero errors.

### Session 5 (2026-11-11) - Summary of Accomplishments:
1. **Machine Learning Pipeline (Phase 4 - Unit III):**
   - Implemented `StudentPerformanceModel` in `src/ml/model_trainer.py`.
   - Built `prep_data()` with stratified train-test splitting based on the categorical `grade` distribution to preserve class balance.
   - Implemented `train()` supporting both `LinearRegression` baseline and `RandomForestRegressor`.
   - Built `evaluate()` calculating MAE, RMSE, and $R^2$.
   - Implemented `predict_student()` predicting continuous scores and mapping them into grade tiers using functional threshold logic.
   - Implemented model persistence (`save_model`, `load_model`) using `joblib`.
   - Verified end-to-end predictions and error metrics on test profiles.

### Session 6 (2026-11-12) - Summary of Accomplishments:
1. **Main CLI Application (Phase 5 - Core Polish):**
   - Implemented unified interactive terminal application in `main.py`.
   - Bound all project modules into a clean 7-option menu using `match...case`:
     - Option 1: Add Student with validation and CSV persistence.
     - Option 2: Search Student by Roll Number with `RecordNotFound` handling.
     - Option 3: View All Local Records in formatted table view.
     - Option 4: Full EDA pipeline with health check, descriptive stats, and correlation.
     - Option 5: Auto-generate 4 publication-quality 300 DPI figures to `reports/figures/`.
     - Option 6: Predict Student Performance via pre-trained Scikit-learn model with zero-lag inference.
     - Option 7: Clean exit and graceful `KeyboardInterrupt` handling.
   - Tested happy paths, duplicate rejection, invalid marks catching, and automated smoke test with 100% pass rate.

### Next Session Agenda:
- [ ] *(Optional bonus)* Streamlit interactive web dashboard or demo video/presentation prep.
- [ ] Final project documentation review and packaging.


