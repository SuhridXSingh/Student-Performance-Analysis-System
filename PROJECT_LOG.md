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
- [ ] Matplotlib & Seaborn visualizations (grade distribution, correlation heatmaps, boxplots)

### Phase 4: Machine Learning Model (Unit III)
- [ ] Train a classification model (e.g. predict Pass/Fail or Grade Tier based on study time, attendance, past scores)
- [ ] Model evaluation (Accuracy score, confusion matrix)
- [ ] Function to predict performance for a new student profile

### Phase 5: CLI Integration & Polish
- [ ] Interactive CLI menu binding all components
- [ ] Robust error handling for all user inputs
- [ ] *(Optional bonus)* Streamlit dashboard or Jupyter demo notebook

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

### Next Session Agenda (Phase 3 - Visualizations):
- [ ] **Plotting Module**: Implement `src/visualization/visualizer.py` using Matplotlib and Seaborn.
- [ ] **Grade Distribution**: Categorical count / frequency distribution plot.
- [ ] **Correlation Heatmap**: Visualizing correlation matrix between numerical features.
- [ ] **Performance vs. Study Hours**: Box plot or violin plot showing score distributions across study brackets.
- [ ] **Report Output**: Auto-save generated plots into `reports/figures/`.


