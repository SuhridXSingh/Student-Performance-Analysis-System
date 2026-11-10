import pandas as pd 
import numpy as np

def load_dataset(filepath):
    data = pd.read_csv(filepath)
    print(f"Shape: {data.shape}")
    print(f"Columns: {data.columns}")
    print(f"Memory usage: {data.memory_usage(deep=True)}")
    return data

def check_data_health(df):
    print(f"Shape: {df.shape}")
    print(f"Total missing values: {df.isna().sum().sum()}")
    print(f"Columns with missing data:\n{df.isna().sum()[lambda x: x > 0]}")
    print(f"\nMissing % per column:\n{(df.isna().mean() * 100).round(2)}")
    print(f"\nRows with ANY missing value: {df.isna().any(axis=1).sum()}")
    print(f"Rows with ALL values missing: {df.isna().all(axis=1).sum()}")

def compute_summary_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).drop(columns=["student_id"], errors="ignore")
    summary = {}
    for col in numeric_cols.columns:
        summary[col] = {
            "mean":       numeric_cols[col].mean(),
            "median":     numeric_cols[col].median(),
            "std":        np.std(numeric_cols[col].dropna(), ddof=1),
            "q1":         np.percentile(numeric_cols[col].dropna(), 25),
            "q3":         np.percentile(numeric_cols[col].dropna(), 75),
            "iqr":        np.percentile(numeric_cols[col].dropna(), 75)
                         - np.percentile(numeric_cols[col].dropna(), 25),
        }
    if "grade" in df.columns:
        grade_counts = df["grade"].value_counts()
        grade_dist = df["grade"].value_counts(normalize=True)
        grade_summary = pd.DataFrame({
            "count":  grade_counts,
            "pct":    (grade_dist * 100).round(2),
        })
    else:
        grade_summary = None

    return pd.DataFrame(summary).T, grade_summary

def analyze_performance_by_groups(df):
    by_grade = (
        df.groupby("grade")
          .agg(
              n=("total_score", "count"),
              mean_score=("total_score", "mean"),
              median_score=("total_score", "median"),
              std_score=("total_score", "std"),
              min_score=("total_score", "min"),
              max_score=("total_score", "max"),
          )
          .round(2)
    )

    bins = [0, 10, 20, 30, 45]
    labels = ["0-10h", "10-20h", "20-30h", "30-40+"]

    by_hours = (
        df.assign(study_bin=pd.cut(df["weekly_self_study_hours"], bins=bins, labels=labels, right=False))
          .groupby("study_bin", observed=True)
          .agg(
              n=("total_score", "count"),
              mean_score=("total_score", "mean"),
              median_score=("total_score", "median"),
          )
          .round(2)
    )

    return by_grade, by_hours

def compute_correlation_matrix(df):
    return df.select_dtypes(include=[np.number]).drop(columns=["student_id"], errors="ignore").corr()