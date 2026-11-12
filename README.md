# Student Performance Analysis System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-green.svg)](https://peps.python.org/pep-0008/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)

An end-to-end, modular Python application designed for academic student tracking, exploratory performance analytics, and predictive machine learning.

This project strictly bridges core computer science fundamentals (Object-Oriented Programming, custom exception handling, functional programming) with applied data science (NumPy, Pandas, Seaborn, Matplotlib, Scikit-Learn) and offers dual user interfaces: an interactive terminal CLI and a modern Streamlit web dashboard.

---

## What Does This Program Do?

The **Student Performance Analysis System** addresses both operational record management and data-driven educational analytics:

1. **Student Record Management (CRUD & Validation)**:
   - Manages student profiles with strict boundary validation (scores `[0, 100]`, attendance percentages, study hours).
   - Dynamically computes letter grades (`A`, `B`, `C`, `D`, `F`) using functional programming (`lambda`, `filter`, `next`).
   - Serializes and deserializes student records to and from CSV using context managers.
2. **Exploratory Data Analysis (EDA)**:
   - Ingests and processes a 1,000,000-row student academic dataset from Kaggle.
   - Computes statistical summaries (mean, median, standard deviation, quartiles, IQR) and group aggregations across grade tiers and study hour brackets.
   - Computes feature correlation matrices to identify primary performance drivers.
3. **Publication-Quality Visualizations**:
   - Generates and exports high-resolution (300 DPI) figures to `reports/figures/`:
     - Student Grade Distribution (annotated count & percentage bars)
     - Feature Correlation Heatmap (annotated Pearson $r$)
     - Study Hours vs. Score Distribution (Tukey boxplots across brackets)
     - Overall Total Score Distribution (histogram + Kernel Density Estimation curve)
4. **Predictive Machine Learning Engine**:
   - Trains Scikit-Learn regression models (Linear Regression baseline and Random Forest Regressor) with stratified train-test splits based on grade distribution.
   - Serializes and loads pre-trained models using `joblib` for sub-5ms real-time inference.
   - Predicts continuous total scores and automatically classifies students into academic performance tiers.

---

## Project Architecture

```text
student_performance_analysis/
│
├── data/                                 # Datasets
│   ├── student_performance.csv           # 1M row Kaggle dataset for EDA & ML training
│   └── students.csv                      # Operational database for local student records
│
├── models/                               # Serialized Machine Learning Artifacts
│   └── student_model.pkl                 # Trained Random Forest Regressor model (joblib)
│
├── reports/                              # Generated Visual Outputs
│   └── figures/                          # Exported 300 DPI visualization figures
│       ├── grade_distribution.png
│       ├── correlation_heatmap.png
│       ├── study_hours_vs_score.png
│       └── score_distribution.png
│
├── src/                                  # Core Application Source Code
│   ├── models/                           # Domain Models (OOP & Encapsulation)
│   │   ├── __init__.py
│   │   └── student.py                    # Person base class & Student subclass
│   │
│   ├── exceptions/                       # Custom Exception Hierarchy
│   │   ├── __init__.py
│   │   └── custom_exceptions.py          # BaseAppExceptions, InvalidMarksError, RecordNotFound
│   │
│   ├── utils/                            # File I/O & Persistence
│   │   ├── __init__.py
│   │   └── file_manager.py               # CSV serialization, deserialization & search lookups
│   │
│   ├── analysis/                         # Data Science & Statistics (Unit III)
│   │   ├── __init__.py
│   │   └── data_analyzer.py              # Health check, summary statistics, group aggregations
│   │
│   ├── visualization/                    # Visual Analytics (Unit III)
│   │   ├── __init__.py
│   │   └── visualizer.py                 # Matplotlib & Seaborn plotting routines
│   │
│   └── ml/                               # Machine Learning (Unit III)
│       ├── __init__.py
│       └── model_trainer.py              # Scikit-learn training, evaluation, persistence & inference
│
├── app.py                                # Streamlit Web Application (Interactive Dashboard)
├── main.py                               # Terminal CLI Entrypoint (Menu Loop & Handlers)
├── PROJECT_LOG.md                        # Phase-wise development roadmap & session logs
├── requirements.txt                      # Project dependencies
└── README.md                             # Project documentation
```

---

## Academic Syllabus Alignment

| Syllabus Unit | Key Concepts Implemented | Modules / Files |
| :--- | :--- | :--- |
| **Unit I: Fundamentals & File I/O** | Environment setup, control flow, functions, `with open(...)` context managers, CSV streams, type casting, error handling. | `src/utils/file_manager.py`<br>`main.py` |
| **Unit II: Advanced Python & OOP** | Encapsulation (`@property`), Inheritance (`Person` $\rightarrow$ `Student`), custom exceptions (`raise`/`except`), functional programming (`lambda`, `filter`, `next`). | `src/models/student.py`<br>`src/exceptions/custom_exceptions.py` |
| **Unit III: Data Science & ML** | NumPy array operations, Pandas DataFrames & group aggregations, Seaborn & Matplotlib visualizations, Scikit-learn Regression & model persistence (`joblib`). | `src/analysis/data_analyzer.py`<br>`src/visualization/visualizer.py`<br>`src/ml/model_trainer.py` |

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher installed
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/SuhridXSingh/Student-Performance-Analysis-System.git
cd Student-Performance-Analysis-System
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

The system can be operated in two modes:

### Mode 1: Interactive Terminal CLI
Launch the menu-driven console application:

```bash
python main.py
```

```text
=======================================================
STUDENT PERFORMANCE ANALYSIS & PREDICTION SYSTEM
=======================================================
1. Add New Student Record
2. Search Student by Roll Number
3. View All Student Records (CSV)
4. Run Exploratory Data Analysis (EDA)
5. Generate & Save Visualizations
6. Predict Student Performance (ML)
7. Exit
=======================================================
```

### Mode 2: Interactive Streamlit Web Dashboard
Launch the web interface in your default browser:

```bash
streamlit run app.py
```

The web dashboard opens at `http://localhost:8501` featuring:
- **Overview Dashboard**: High-level KPIs, syllabus coverage mapping, and grading scale tables.
- **Student Records**: Interactive data grid, new student input form, and roll number search.
- **Exploratory Data Analysis**: Dataset health, summary metrics, group distributions, and full correlation matrix.
- **Visualizations**: Dedicated interactive tabs rendering Matplotlib and Seaborn figures.
- **Performance Predictor**: Sliders for study hours, attendance %, and participation score providing instant predicted scores, grade tiers, and academic standing assessments.

---

## Dataset Information

- **Source**: [Student Performance Dataset – Kaggle](https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset)
- **Dataset Size**: 1,000,000 rows
- **Features**:
  - `weekly_self_study_hours` (0–40): Average weekly hours spent self-studying.
  - `attendance_percentage` (50–100): Class attendance record.
  - `class_participation` (0–10): Classroom engagement score.
  - `total_score` (0–100): Continuous final performance score (Target for Regression).
  - `grade` (`A`, `B`, `C`, `D`, `F`): Categorical academic grade tier (Target for Classification).

### Grade Thresholds
- **A**: $\ge 85$
- **B**: $\ge 70$
- **C**: $\ge 55$
- **D**: $\ge 40$
- **F**: $< 40$

---

## Project Roadmap

- [x] **Phase 1: Environment & Custom Exceptions**
  - [x] Virtualenv configuration and dependency hygiene
  - [x] Exception hierarchy (`BaseAppExceptions`, `InvalidMarksError`, `RecordNotFound`)
- [x] **Phase 2: Core OOP & Student Persistence**
  - [x] `Person` base class and `Student` subclass with encapsulation
  - [x] Functional grading logic with `filter()`, `lambda`, and `next()`
  - [x] File persistence manager with context managers and search lookups
- [x] **Phase 3: Exploratory Data Analysis & Visualizations**
  - [x] Pandas DataFrame loading and data hygiene inspection (1M rows)
  - [x] Descriptive statistics, quartiles, and grouped aggregations
  - [x] Matplotlib and Seaborn visual suite (4 exported 300 DPI figures)
- [x] **Phase 4: Machine Learning Modeling**
  - [x] Stratified train-test split preserving class distribution
  - [x] Linear Regression and Random Forest Regressor implementation
  - [x] Model evaluation metrics (MAE, RMSE, $R^2$)
  - [x] Model serialization and persistence (`joblib`)
- [x] **Phase 5: CLI Integration & Web UI**
  - [x] Unified interactive terminal application (`main.py`)
  - [x] Robust input validation and error recovery
  - [x] Interactive Streamlit web dashboard (`app.py`)

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
