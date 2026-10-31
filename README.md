# 🎓 Student Performance Analysis System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-green.svg)](https://peps.python.org/pep-0008/)

An end-to-end, modular Python application designed for academic student tracking, exploratory performance analytics, and predictive machine learning. 

This repository strictly bridges core Python computer science fundamentals (OOP, error handling, functional programming) with applied data science (NumPy, Pandas, Seaborn, Scikit-Learn).

---

## 📌 What Does This Program Do?

The **Student Performance Analysis System** is built to solve both operational record management and data-driven educational analytics:

1. **Student Record Management (CRUD & Validation)**:
   - Manages student profiles with strict boundary validation (e.g. valid scores `[0, 100]`, valid attendance percentage).
   - Dynamically computes letter grades (`A`, `B`, `C`, `D`, `F`) using functional programming.
   - Serializes and deserializes student records to and from CSV using context managers.
2. **Exploratory Data Analysis (EDA)**:
   - Ingests and processes a 1,000,000-row student academic dataset.
   - Computes statistical summaries (mean, median, standard deviation) and group aggregations (correlating study hours and attendance against final scores).
   - Generates publication-ready visualizations (correlation heatmaps, grade distributions, and factor boxplots).
3. **Predictive Performance Analytics (Machine Learning)**:
   - Uses Scikit-Learn classification and regression models to predict expected grades and scores based on self-study hours, class attendance, and active participation.
   - Enables early intervention for at-risk students.

---

## 🏗️ Project Architecture

```text
student_performance_analysis/
│
├── data/                                 # Datasets
│   ├── student_performance.csv           # 1M row Kaggle dataset for EDA & ML training
│   └── students.csv                      # Operational database for app student records
│
├── src/                                  # Core Application Source Code
│   ├── models/                           # Domain Models (OOP & Encapsulation)
│   │   ├── __init__.py
│   │   └── student.py                    # Person base class & Student subclass
│   │
│   ├── exceptions/                       # Custom Exception Hierarchy
│   │   ├── __init__.py
│   │   └── custom_exceptions.py          # InvalidMarksError, RecordNotFound
│   │
│   ├── utils/                            # Utilities & Persistence
│   │   ├── __init__.py
│   │   └── file_manager.py               # CSV serialization, deserialization & search
│   │
│   ├── analysis/                         # Data Science & Statistics (Unit III)
│   │   └── __init__.py                   # Data processing & Pandas operations
│   │
│   ├── visualization/                    # Visual Analytics (Unit III)
│   │   └── __init__.py                   # Matplotlib & Seaborn plotting routines
│   │
│   └── ml/                               # Machine Learning (Unit III)
│       └── __init__.py                   # Scikit-learn pipelines & inference
│
├── .gitignore                            # Repository ignore rules
├── PROJECT_LOG.md                        # Phase-wise roadmap and session progress
├── requirements.txt                      # Project dependencies
└── README.md                             # Project documentation
```

---

## 🧩 Academic Syllabus Alignment

| Syllabus Unit | Key Concepts Implemented | Modules / Files |
| :--- | :--- | :--- |
| **Unit I: Fundamentals & File I/O** | Environment setup, control flow, functions, `with open(...)` context managers, file streams, type conversion. | `src/utils/file_manager.py` |
| **Unit II: Advanced Python & OOP** | Encapsulation (`@property`), Inheritance (`Person` $\rightarrow$ `Student`), custom exceptions (`raise`/`except`), functional programming (`lambda`, `filter`, `next`). | `src/models/student.py`<br>`src/exceptions/custom_exceptions.py` |
| **Unit III: Data Science & ML** | NumPy array math, Pandas DataFrames/aggregations, Matplotlib/Seaborn charting, Scikit-learn modeling. | `src/analysis/`<br>`src/visualization/`<br>`src/ml/` |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### 1. Clone the Repository
```bash
git clone https://github.com/SuhridXSingh/Student-Performance-Analysis-System.git
cd Student-Performance-Analysis-System
```

### 2. Create and Activate a Virtual Environment

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

## 🚀 Running the Application

Launch the interactive console application:

```bash
python main.py
```

### Interactive CLI Menu
The system provides a menu-driven interface with automated data validation, file persistence, and analytical dispatch:

```text
======================================================
  🎓 Student Performance Analysis & Prediction System
======================================================
[1] 📝 Add New Student Record
[2] 📋 View All Registered Students
[3] 🔍 Search Student by Roll Number
[4] 📊 Run Exploratory Data Analysis & Visualizations
[5] 🤖 Predict Grade & Score for New Student (ML)
[6] 🚪 Exit
======================================================
```

* **Data Entry**: Guided prompts to enter student details (`name`, `age`, `roll_number`, `study_hours`, `attendance`, `participation`, `total_score`). Bounds validation prevents invalid records from being saved.
* **Auto-Grading & Persistence**: Automatically calculates letter grade (`A`–`F`) and appends the record into `data/students.csv`.
* **Analytics & Predictions**: Triggers EDA visual summaries and machine learning inference directly from the console.

---

## 📊 Dataset Information

* **Source**: [Student Performance Dataset – Kaggle](https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset)
* **Dataset Size**: 1,000,000 rows
* **Features**:
  * `weekly_self_study_hours` (0–40): Average weekly hours spent studying.
  * `attendance_percentage` (50–100): Class attendance record.
  * `class_participation` (0–10): Continuous evaluation of classroom engagement.
  * `total_score` (0–100): Continuous final performance mark (Regression target).
  * `grade` (`A`, `B`, `C`, `D`, `F`): Discrete performance tier (Classification target).

---

## 🗺️ Project Roadmap

- [x] **Phase 1: Environment & Custom Exceptions**
  - [x] Virtualenv configuration & dependency management
  - [x] Exception hierarchy (`BaseAppExceptions`, `InvalidMarksError`, `RecordNotFound`)
- [x] **Phase 2: Core OOP & Student Persistence**
  - [x] `Person` base class and `Student` subclass with encapsulation
  - [x] Functional grading logic with `filter()`, `lambda`, and `next()`
  - [x] File persistence manager with context managers and search lookups
- [ ] **Phase 3: Exploratory Data Analysis (EDA)**
  - [ ] Pandas DataFrame loading and data hygiene inspection
  - [ ] Descriptive statistics and grouped aggregations
  - [ ] Seaborn & Matplotlib visual analytical dashboards
- [ ] **Phase 4: Machine Learning Modeling**
  - [ ] Train/test split and feature scaling
  - [ ] Classifier training (Predicting Grade category)
  - [ ] Model evaluation (Confusion matrix, precision, recall, accuracy)
- [ ] **Phase 5: Interactive CLI Application**
  - [ ] Menu loop binding persistence, analytics, and ML inference together
  - [ ] Input validation and robust error recovery

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
