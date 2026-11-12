import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.models.student import Student
from src.exceptions.custom_exceptions import InvalidMarksError, RecordNotFound
from src.utils.file_manager import save_students_to_csv, load_students_from_csv, find_student_by_roll
from src.analysis.data_analyzer import (
    load_dataset, check_data_health, compute_summary_stats,
    analyze_performance_by_groups, compute_correlation_matrix
)
from src.visualization.visualizer import (
    plot_grade_distribution, plot_correlation_heatmap,
    plot_study_hours_vs_score, plot_score_distribution
)
from src.ml.model_trainer import StudentPerformanceModel, DEFAULT_MODEL_PATH

# Application Configuration
st.set_page_config(
    page_title="Student Performance Analysis System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Zero Emojis, Clean Professional Academic Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.8rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .grade-badge-a { color: #166534; background-color: #DCFCE7; font-weight: bold; padding: 4px 10px; border-radius: 4px; }
    .grade-badge-b { color: #1E40AF; background-color: #DBEAFE; font-weight: bold; padding: 4px 10px; border-radius: 4px; }
    .grade-badge-c { color: #854D0E; background-color: #FEF9C3; font-weight: bold; padding: 4px 10px; border-radius: 4px; }
    .grade-badge-d { color: #9A3412; background-color: #FFEDD5; font-weight: bold; padding: 4px 10px; border-radius: 4px; }
    .grade-badge-f { color: #991B1B; background-color: #FEE2E2; font-weight: bold; padding: 4px 10px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

STUDENTS_CSV = "data/students.csv"
DATASET_CSV = "data/student_performance.csv"


@st.cache_data
def get_cached_dataset():
    """Load dataset with Streamlit caching for instant page transitions."""
    if os.path.exists(DATASET_CSV):
        return pd.read_csv(DATASET_CSV)
    return None


@st.cache_resource
def get_cached_model():
    """Load or initialize pre-trained machine learning model."""
    model = StudentPerformanceModel(df=None, model_type="random_forest")
    if os.path.exists(DEFAULT_MODEL_PATH):
        try:
            model.load_model()
            return model
        except Exception:
            pass
    return None


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Select Module",
        [
            "Overview Dashboard",
            "Student Records",
            "Exploratory Data Analysis",
            "Visualizations",
            "Performance Predictor"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Student Performance Analysis System")
    st.sidebar.caption("Coursework Units 1, 2, and 3")

    if selection == "Overview Dashboard":
        render_overview()
    elif selection == "Student Records":
        render_student_records()
    elif selection == "Exploratory Data Analysis":
        render_eda()
    elif selection == "Visualizations":
        render_visualizations()
    elif selection == "Performance Predictor":
        render_predictor()


def render_overview():
    st.markdown('<div class="main-header">Student Performance Analysis System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Integrated Academic Performance Analytics, OOP Records, and ML Inference Engine</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    df = get_cached_dataset()

    with col1:
        st.metric("Total Dataset Records", f"{len(df):,}" if df is not None else "0")
    with col2:
        try:
            local_students = load_students_from_csv(STUDENTS_CSV)
            st.metric("Local Student Records", len(local_students))
        except RecordNotFound:
            st.metric("Local Student Records", "0")
    with col3:
        if df is not None and "total_score" in df.columns:
            st.metric("Average Dataset Score", f"{df['total_score'].mean():.1f} / 100")
        else:
            st.metric("Average Dataset Score", "N/A")
    with col4:
        model = get_cached_model()
        st.metric("Trained Model Status", "Ready (Random Forest)" if model and model.model else "Not Loaded")

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.subheader("System Architecture & Syllabus Coverage")
        st.markdown("""
        - **Unit 1: Foundations**: Environment configuration, file input/output, control structures, and error handling.
        - **Unit 2: Object-Oriented Programming**: Inheritance hierarchy (`Person` to `Student`), encapsulation with properties, functional grading (`lambda`, `filter`, `next`), and custom domain exceptions (`InvalidMarksError`, `RecordNotFound`).
        - **Unit 3: Data Analysis & Machine Learning**: NumPy statistics, Pandas aggregations, Seaborn and Matplotlib visualizations, and Scikit-learn predictive modeling.
        """)

    with col_right:
        st.subheader("Grading Scale Reference")
        grading_data = pd.DataFrame({
            "Grade": ["A", "B", "C", "D", "F"],
            "Score Range": [">= 85", "70 - 84.9", "55 - 69.9", "40 - 54.9", "< 40"],
            "Classification": ["Distinction", "Merit", "Satisfactory", "Pass", "Fail"]
        })
        st.dataframe(grading_data, hide_index=True, use_container_width=True)


def render_student_records():
    st.markdown('<div class="main-header">Student Record Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Object-Oriented Record Creation, CSV Persistence, and Query Operations</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["View All Records", "Add New Student", "Search by Roll Number"])

    with tab1:
        st.subheader("Current Local Database Records")
        try:
            students = load_students_from_csv(STUDENTS_CSV)
            if students:
                records = []
                for s in students:
                    records.append({
                        "Roll Number": s._roll_number,
                        "Name": s.name,
                        "Age": s.age,
                        "Weekly Study Hours": s._study_hours,
                        "Attendance %": s._attendance,
                        "Participation Score": s._participation,
                        "Total Score": s._total_score,
                        "Calculated Grade": s.calc_grade()
                    })
                records_df = pd.DataFrame(records)
                st.dataframe(records_df, use_container_width=True, hide_index=True)
                st.caption(f"Total Local Records: {len(records_df)}")
            else:
                st.info("No records found in local database.")
        except RecordNotFound:
            st.info("No database file exists yet. Use the 'Add New Student' tab to create your first record.")

    with tab2:
        st.subheader("Add Student Profile")
        with st.form("add_student_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name").strip()
                age = st.number_input("Age", min_value=15, max_value=80, value=20, step=1)
                roll_number = st.number_input("Roll Number", min_value=1, max_value=999999, value=101, step=1)
                study_hours = st.number_input("Weekly Self-Study Hours", min_value=0.0, max_value=60.0, value=15.0, step=0.5)

            with col_b:
                attendance = st.number_input("Attendance Percentage (0 - 100)", min_value=0.0, max_value=100.0, value=85.0, step=0.5)
                participation = st.number_input("Class Participation Score (0 - 10)", min_value=0.0, max_value=10.0, value=6.0, step=0.1)
                total_score = st.number_input("Total Score (0 - 100)", min_value=0.0, max_value=100.0, value=85.0, step=0.5)

            submitted = st.form_submit_button("Save Student Record")

            if submitted:
                if not name:
                    st.error("Validation Error: Student name cannot be empty.")
                else:
                    try:
                        std = Student(name, int(age), int(roll_number), float(study_hours), float(attendance), float(participation), float(total_score))

                        try:
                            students = load_students_from_csv(STUDENTS_CSV)
                        except RecordNotFound:
                            students = []

                        if any(s._roll_number == int(roll_number) for s in students):
                            st.error(f"Duplicate Error: Student with Roll Number {roll_number} already exists.")
                        else:
                            students.append(std)
                            save_students_to_csv(STUDENTS_CSV, students)
                            st.success(f"Success: Added {name} (Roll: {roll_number}, Grade: {std.calc_grade()}) to database.")
                            st.rerun()

                    except InvalidMarksError as e:
                        st.error(f"Validation Error: {e}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab3:
        st.subheader("Query Student by Roll Number")
        search_roll = st.number_input("Enter Roll Number to Search", min_value=1, step=1, value=101)
        if st.button("Search Database"):
            try:
                student = find_student_by_roll(STUDENTS_CSV, int(search_roll))
                st.success("Record Found")
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Name:** {student.name}")
                    st.write(f"**Age:** {student.age}")
                    st.write(f"**Roll Number:** {student._roll_number}")
                    st.write(f"**Study Hours:** {student._study_hours} hrs/week")
                with c2:
                    st.write(f"**Attendance:** {student._attendance}%")
                    st.write(f"**Participation:** {student._participation} / 10")
                    st.write(f"**Total Score:** {student._total_score} / 100")
                    st.write(f"**Final Grade:** **{student.calc_grade()}**")
            except RecordNotFound as e:
                st.warning(f"Not Found: {e}")


def render_eda():
    st.markdown('<div class="main-header">Exploratory Data Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Dataset Health Checks, Descriptive Statistics, and Cross-Feature Aggregations</div>', unsafe_allow_html=True)

    df = get_cached_dataset()
    if df is None:
        st.error(f"Dataset file missing at {DATASET_CSV}.")
        return

    st.subheader("1. Dataset Integrity & Dimension Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Feature Columns", df.shape[1])
    with col3:
        st.metric("Total Missing Values", int(df.isna().sum().sum()))
    with col4:
        st.metric("Memory Footprint", f"{df.memory_usage(deep=True).sum() / (1024**2):.1f} MB")

    st.markdown("---")

    st.subheader("2. Statistical Distribution")
    summary_df, grade_dist = compute_summary_stats(df)

    col_stat1, col_stat2 = st.columns([3, 2])
    with col_stat1:
        st.write("**Numerical Summary (Mean, Median, Standard Deviation, Quartiles, IQR)**")
        st.dataframe(summary_df, use_container_width=True)

    with col_stat2:
        st.write("**Categorical Grade Distribution**")
        if grade_dist is not None:
            st.dataframe(grade_dist, use_container_width=True)

    st.markdown("---")

    st.subheader("3. Group Aggregations")
    by_grade, by_hours = analyze_performance_by_groups(df)

    col_grp1, col_grp2 = st.columns(2)
    with col_grp1:
        st.write("**Score Statistics by Grade Tier**")
        st.dataframe(by_grade, use_container_width=True)

    with col_grp2:
        st.write("**Score Statistics by Study Hours Bracket**")
        st.dataframe(by_hours, use_container_width=True)

    st.markdown("---")

    st.subheader("4. Feature Correlation Matrix")
    corr_matrix = compute_correlation_matrix(df).round(3)
    
    col_corr1, col_corr2 = st.columns([3, 2])
    with col_corr1:
        st.write("**Full Pearson Correlation Table**")
        st.dataframe(corr_matrix, use_container_width=True)

    with col_corr2:
        st.write("**Direct Correlation with Final Total Score**")
        score_col = "total_score" if "total_score" in corr_matrix.columns else "score"
        target_corr = corr_matrix[score_col].sort_values(ascending=False).to_frame(name="Correlation Coefficient")
        st.dataframe(target_corr, use_container_width=True)


def render_visualizations():
    st.markdown('<div class="main-header">Data Visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Matplotlib and Seaborn Diagnostic Figures (300 DPI Publication Quality)</div>', unsafe_allow_html=True)

    df = get_cached_dataset()
    if df is None:
        st.error(f"Dataset missing at {DATASET_CSV}.")
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        "Grade Distribution",
        "Feature Correlation Heatmap",
        "Study Hours vs Score",
        "Score Distribution Curve"
    ])

    with tab1:
        st.subheader("Student Grade Category Breakdown")
        fig, ax = plt.subplots(figsize=(9, 5))
        grade_order = ["A", "B", "C", "D", "F"]
        palette = sns.color_palette("mako", n_colors=len(grade_order))
        sns.countplot(data=df, x="grade", order=grade_order, palette=palette, hue="grade", legend=False, ax=ax)
        total = len(df)
        for p in ax.patches:
            h = p.get_height()
            if h > 0:
                ax.annotate(f"{int(h):,}\n({h/total*100:.1f}%)", (p.get_x() + p.get_width() / 2.0, h),
                            ha="center", va="bottom", fontsize=9, xytext=(0, 3), textcoords="offset points")
        ax.set_title("Student Grade Distribution", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Grade Classification")
        ax.set_ylabel("Student Count")
        ax.set_ylim(0, total * 0.65)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Distribution shows grade tier proportions across 1,000,000 records. Note class imbalance towards Grade A (54.9%).")

    with tab2:
        st.subheader("Pearson Correlation Heatmap")
        numeric_df = df.select_dtypes(include=[np.number]).drop(columns=["student_id", "roll_number"], errors="ignore")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", vmin=-1.0, vmax=1.0, fmt=".2f",
                    square=True, linewidths=0.5, cbar_kws={"shrink": 0.8, "label": "Pearson Correlation (r)"}, ax=ax)
        ax.set_title("Numeric Feature Correlation Matrix", fontsize=13, fontweight="bold", pad=12)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Weekly study hours exhibits a dominant linear correlation (+0.81) with final score, while attendance and participation show near-zero single-variable linear correlation.")

    with tab3:
        st.subheader("Score Spread across Study Hour Bins")
        hours_col = "weekly_self_study_hours" if "weekly_self_study_hours" in df.columns else "study_hours"
        score_col = "total_score" if "total_score" in df.columns else "score"
        bins = [0, 10, 20, 30, 45]
        labels = ["0-10h", "10-20h", "20-30h", "30-40h+"]
        temp_df = df.copy()
        temp_df["study_bracket"] = pd.cut(temp_df[hours_col], bins=bins, labels=labels, right=False)

        fig, ax = plt.subplots(figsize=(9, 5.5))
        sns.boxplot(data=temp_df, x="study_bracket", y=score_col, palette="viridis", hue="study_bracket", legend=False, ax=ax)
        ax.set_title("Total Score Distribution by Weekly Study Bracket", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Weekly Self-Study Bracket")
        ax.set_ylabel("Total Score (0 - 100)")
        ax.set_ylim(0, 105)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Clear monotonic increase in median score from 65.0 (0-10h) to 99.9 (30h+), showing a performance ceiling near 25-30 study hours.")

    with tab4:
        st.subheader("Total Score Frequency Distribution & KDE Curve")
        score_col = "total_score" if "total_score" in df.columns else "score"
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.histplot(df[score_col], kde=True, bins=30, color="royalblue", edgecolor="black", ax=ax)
        mean_s = df[score_col].mean()
        med_s = df[score_col].median()
        ax.axvline(mean_s, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {mean_s:.1f}")
        ax.axvline(med_s, color="green", linestyle="-", linewidth=1.5, label=f"Median: {med_s:.1f}")
        ax.set_title("Overall Total Score Distribution", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Total Score")
        ax.set_ylabel("Frequency Count")
        ax.legend(loc="upper left")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Distribution displays moderate negative skewness (mean < median), indicating the majority of scores cluster in the 75-100 bracket.")


def render_predictor():
    st.markdown('<div class="main-header">Machine Learning Performance Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive Inference Engine Powered by Random Forest Regressor & Functional Grading</div>', unsafe_allow_html=True)

    model = get_cached_model()

    if model is None or model.model is None:
        st.warning("Pre-trained model not detected in local directory.")
        if st.button("Train and Save Random Forest Model Now"):
            df = get_cached_dataset()
            if df is None:
                st.error("Cannot train: Dataset file missing.")
                return
            with st.spinner("Training Random Forest on dataset..."):
                model = StudentPerformanceModel(df=df, model_type="random_forest")
                model.prep_data()
                model.train()
                model.save_model()
                st.success("Model trained and serialized successfully to models/student_model.pkl")
                st.rerun()
        return

    st.subheader("Input Student Parameters")
    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        input_hours = st.slider("Weekly Self-Study Hours", min_value=0.0, max_value=45.0, value=18.5, step=0.5)
    with col_in2:
        input_att = st.slider("Class Attendance Percentage (%)", min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    with col_in3:
        input_part = st.slider("Class Participation Score (0 - 10)", min_value=0.0, max_value=10.0, value=6.5, step=0.1)

    st.markdown("---")

    result = model.predict_student(input_hours, input_att, input_part)
    predicted_score = result["predicted_score"]
    predicted_grade = result["predicted_grade"]

    st.subheader("Prediction Results")
    col_out1, col_out2, col_out3 = st.columns(3)

    with col_out1:
        st.metric("Predicted Total Score", f"{predicted_score:.1f} / 100")

    with col_out2:
        st.metric("Predicted Grade Classification", f"Grade {predicted_grade}")

    with col_out3:
        status_map = {
            "A": "Excellent (Distinction Tier)",
            "B": "Good (Merit Tier)",
            "C": "Satisfactory (Pass Tier)",
            "D": "Marginal (Needs Improvement)",
            "F": "At Risk (Failing Tier)"
        }
        st.metric("Academic Standing", status_map.get(predicted_grade, "Standard"))

    st.markdown("---")
    st.caption("Inference execution latency: < 5 milliseconds. Model trained using stratified 80/20 train-test split.")


if __name__ == "__main__":
    main()
