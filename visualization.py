import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def _prepare_numeric(df):
    if df is None or df.empty:
        return None
    return df.apply(pd.to_numeric, errors="coerce")

def plot_individual(student_df):
    df = _prepare_numeric(student_df)
    if df is None:
        print("No valid data to plot.")
        return

    # Define exam-to-color mapping
    exam_colors = {
        "PT1": "blue",
        "PT2": "orange",
        "Term1": "green",
        "Term2": "red"
    }

    # Extract subject and exam type from column names
    subject_labels = [col.split("_")[0] for col in df.columns]
    exam_labels = [col.split("_")[1] for col in df.columns]
    colors = [exam_colors.get(exam, "gray") for exam in exam_labels]

    # Plot bars manually
    x = np.arange(len(df.columns))
    values = df.iloc[0].values  # assuming single student row

    plt.figure(figsize=(12, 6))
    plt.bar(x, values, color=colors)

    # X-axis: show subject names only
    plt.xticks(x, subject_labels, rotation=45, ha="right")
    plt.title("Individual Student Subject-wise PT & Term Marks")
    plt.ylabel("Marks")
    plt.xlabel("Subjects")
    plt.ylim(0, 80)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Legend: show exam types with their colors
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in exam_colors.values()]
    labels = list(exam_colors.keys())
    plt.legend(handles, labels, title="Examination")

    plt.tight_layout()
    plt.show()


def plot_student_yearwise(student_dict):
    if student_dict is None:
        print("No summary data to plot.")
        return
    combined_df = pd.concat([student_dict["PT"], student_dict["Term"], student_dict["Overall"]], axis=1)
    combined_df.columns = ["PT%", "Term%", "Percentage"]
    combined_df.plot(kind="bar", width=0.7)
    plt.title("Student PT%, Term%, and Overall Percentage (2020–2022)")
    plt.ylabel("Percentage")
    plt.xlabel("Year")
    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_all_session_comparison(results):
    """
    Plot PT and Term marks across sessions (A, B, C) for 3 years.
    """
    if results is None:
        print("No data to plot.")
        return
    # PT graph
    pt_df = _prepare_numeric(results["PT"])
    if pt_df is not None and not pt_df.empty:
        pt_df.unstack().plot(kind="bar", figsize=(10, 6))
        plt.title("PT Marks Across Sessions (2020–2022)")
        plt.ylabel("Marks")
        plt.xlabel("Year")
        plt.ylim(0, 80)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.legend(title="Session")
        plt.tight_layout()
        plt.show()
    # Term graph
    term_df = _prepare_numeric(results["Term"])
    if term_df is not None and not term_df.empty:
        term_df.unstack().plot(kind="bar", figsize=(10, 6))
        plt.title("Term Marks Across Sessions (2020–2022)")
        plt.ylabel("Marks")
        plt.xlabel("Year")
        plt.ylim(0, 80)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.legend(title="Session")
        plt.tight_layout()
        plt.show()

def plot_class_subject_analysis(results, subject_choice):
    if results is None:
        print("No data to plot.")
        return
    
    stats_df, subject_choice = results
    
    # Handle MultiIndex columns safely
    if isinstance(stats_df.columns, pd.MultiIndex):
        stats_df.columns = [f"{col}_{stat}" for col, stat in stats_df.columns]
    
    if stats_df.empty:
        print(f"No data available for subject {subject_choice}.")
        return
    
    # Plot
    stats_df.plot(kind="bar", figsize=(12, 6))
    plt.title(f"{subject_choice} PT1, PT2, Term1, Term2 (Least, Top, Avg) Across 3 Years")
    plt.ylabel("Marks")
    plt.xlabel("Year")
    plt.ylim(0, 80)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
