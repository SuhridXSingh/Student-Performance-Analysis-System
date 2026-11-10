import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

FIGURES_DIR = os.path.join("reports", "figures")


def _ensure_output_dir():
    """Helper to ensure the figures directory exists before saving."""
    os.makedirs(FIGURES_DIR, exist_ok=True)


def plot_grade_distribution(df, save=True):
    """
    Plots the frequency distribution of student grades (A, B, C, D, F).
    Displays both count and percentage on top of each bar.
    """
    _ensure_output_dir()
    plt.figure(figsize=(8, 5))

    grade_order = ["A", "B", "C", "D", "F"]
    palette = sns.color_palette("mako", n_colors=len(grade_order))
    
    ax = sns.countplot(
        data=df,
        x="grade",
        order=grade_order,
        palette=palette,
        hue="grade",
        legend=False
    )

    total_students = len(df)
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            percentage = (height / total_students) * 100
            ax.annotate(
                f"{int(height):,}\n({percentage:.1f}%)",
                (p.get_x() + p.get_width() / 2.0, height),
                ha="center",
                va="bottom",
                fontsize=9,
                xytext=(0, 3),
                textcoords="offset points"
            )

    plt.title("Student Grade Distribution", fontsize=14, pad=15, fontweight="bold")
    plt.xlabel("Grade Category", fontsize=11)
    plt.ylabel("Number of Students", fontsize=11)
    plt.ylim(0, total_students * 0.65)
    plt.tight_layout()

    filepath = os.path.join(FIGURES_DIR, "grade_distribution.png")
    if save:
        plt.savefig(filepath, dpi=300)
        print(f"Saved: {filepath}")
    
    plt.close()
    return filepath


def plot_correlation_heatmap(df, save=True):
    """
    Computes and plots a correlation heatmap for all numeric features.
    Excludes identifier columns (student_id, roll_number).
    """
    _ensure_output_dir()
    plt.figure(figsize=(8, 6))

    numeric_df = df.select_dtypes(include=[np.number]).drop(
        columns=["student_id", "roll_number"], errors="ignore"
    )
    corr_matrix = numeric_df.corr()

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        vmin=-1.0,
        vmax=1.0,
        fmt=".2f",
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient"}
    )

    plt.title("Feature Correlation Heatmap", fontsize=14, pad=15, fontweight="bold")
    plt.xticks(rotation=20, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    filepath = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
    if save:
        plt.savefig(filepath, dpi=300)
        print(f"Saved: {filepath}")

    plt.close()
    return filepath


def plot_study_hours_vs_score(df, save=True):
    """
    Visualizes the relationship between weekly self-study hours and total score.
    Bins study hours into brackets and displays score distributions using boxplots.
    """
    _ensure_output_dir()
    plt.figure(figsize=(9, 6))

    # Detect proper study hours column
    hours_col = "weekly_self_study_hours" if "weekly_self_study_hours" in df.columns else "study_hours"
    score_col = "total_score" if "total_score" in df.columns else "score"

    bins = [0, 10, 20, 30, 45]
    labels = ["0-10h", "10-20h", "20-30h", "30-40h+"]
    
    temp_df = df.copy()
    temp_df["study_bracket"] = pd.cut(temp_df[hours_col], bins=bins, labels=labels, right=False)

    sns.boxplot(
        data=temp_df,
        x="study_bracket",
        y=score_col,
        palette="viridis",
        hue="study_bracket",
        legend=False
    )

    plt.title("Total Score Distribution by Study Hour Bracket", fontsize=14, pad=15, fontweight="bold")
    plt.xlabel("Weekly Self-Study Hours Bracket", fontsize=11)
    plt.ylabel("Total Score (0 - 100)", fontsize=11)
    plt.ylim(0, 105)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    filepath = os.path.join(FIGURES_DIR, "study_hours_vs_score.png")
    if save:
        plt.savefig(filepath, dpi=300)
        print(f"Saved: {filepath}")

    plt.close()
    return filepath


def plot_score_distribution(df, save=True):
    """
    Plots the overall distribution (histogram + KDE density curve) of total scores.
    """
    _ensure_output_dir()
    plt.figure(figsize=(8, 5))

    score_col = "total_score" if "total_score" in df.columns else "score"

    sns.histplot(
        df[score_col],
        kde=True,
        bins=30,
        color="royalblue",
        edgecolor="black"
    )

    # Highlight mean and median lines
    mean_val = df[score_col].mean()
    median_val = df[score_col].median()

    plt.axvline(mean_val, color="red", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.1f}")
    plt.axvline(median_val, color="green", linestyle="-", linewidth=1.5, label=f"Median: {median_val:.1f}")

    plt.title("Overall Total Score Distribution", fontsize=14, pad=15, fontweight="bold")
    plt.xlabel("Total Score", fontsize=11)
    plt.ylabel("Student Count", fontsize=11)
    plt.legend(loc="upper left")
    plt.tight_layout()

    filepath = os.path.join(FIGURES_DIR, "score_distribution.png")
    if save:
        plt.savefig(filepath, dpi=300)
        print(f"Saved: {filepath}")

    plt.close()
    return filepath


def generate_all_visualizations(df):
    """
    Generates and saves the full suite of visualization charts.
    Returns a dictionary mapping plot names to their saved image paths.
    """
    print("\n--- Generating Visualizations ---")
    saved_files = {
        "grade_distribution": plot_grade_distribution(df),
        "correlation_heatmap": plot_correlation_heatmap(df),
        "study_hours_vs_score": plot_study_hours_vs_score(df),
        "score_distribution": plot_score_distribution(df),
    }
    print("All visualizations generated successfully!\n")
    return saved_files

