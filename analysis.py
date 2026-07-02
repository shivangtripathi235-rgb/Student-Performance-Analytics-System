import pandas as pd

BASE_PATHS = [
    r"C:\Users\ShivAnusha\OneDrive - CAMBRIDGE SCHOOL\StudentProject\CODE ANNALYSIS",
    r"C:\Users\CSGN\OneDrive - CAMBRIDGE SCHOOL\StudentProject\CODE ANNALYSIS"
]
SESSIONS = ["A", "B", "C"]
CLASS_MAP = {2020: "VIII", 2021: "IX", 2022: "X"}

def load_all_data():
    dfs = []
    for year, class_name in CLASS_MAP.items():
        for session in SESSIONS:
            file_name = f"{class_name}{session}{year}.csv"
            for base in BASE_PATHS:
                try:
                    full_path = fr"{base}\{file_name}"
                    df = pd.read_csv(full_path)
                    df.set_index("Addm No", inplace=True)
                    df["Session"] = session
                    df["Year"] = year
                    df["Class"] = class_name
                    dfs.append(df)
                    print(f"Loaded {file_name}")
                    break
                except FileNotFoundError:
                    continue
    if dfs:
        return pd.concat(dfs)
    else:
        print("No files loaded. Please check file paths and names.")
        return pd.DataFrame()

def list_admin_numbers(df):
    if df is None or df.empty:
        print("No data available to list admission numbers.")
        return {}
    sections = {}
    for section in ["A", "B", "C"]:
        adm_nos = sorted(set(df[df["Session"] == section].index.tolist()))
        sections[section] = adm_nos
    return sections

def get_admission_number(df):
    if df is None or df.empty:
        print("No data available. Please load files correctly.")
        return None
    print("Available Admission Numbers:")
    sections = list_admin_numbers(df)
    for sec, nums in sections.items():
        print(f"Section {sec}: {nums}")
    adm_no = input("Enter Admission Number: ")
    return adm_no

def Individual_stud_3(df, adm_no):
    try:
        student = df.loc[[int(adm_no)]]
        pt_cols = [c for c in student.columns if "PT" in c]
        term_cols = [c for c in student.columns if "Term" in c]
        return student[pt_cols + term_cols]
    except (KeyError, ValueError):
        print("Admission number not found or invalid.")
        return None

def extract_student_yearwise(df, adm_no):
    try:
        student_df = df.loc[[int(adm_no)]]
        pt_cols = [c for c in student_df.columns if "PT" in c]
        term_cols = [c for c in student_df.columns if "Term" in c]

        student_df["PT%"] = student_df[pt_cols].sum(axis=1) / student_df["Total"] * 100
        student_df["Term%"] = student_df[term_cols].sum(axis=1) / student_df["Total"] * 100

        pt_df = student_df.groupby("Year")[["PT%"]].mean()
        term_df = student_df.groupby("Year")[["Term%"]].mean()
        overall_df = ((pt_df["PT%"] + term_df["Term%"]) / 2).to_frame(name="Percentage")

        return {"PT": pt_df, "Term": term_df, "Overall": overall_df}
    except Exception:
        print("Admission number not found or invalid.")
        return None

def extract_all_session_comparison(df, adm_no):
    """
    For a chosen student, return PT and Term marks across sessions (A, B, C) for 3 years.
    """
    try:
        student_df = df.loc[[int(adm_no)]]
        # PT columns
        pt_cols = [c for c in student_df.columns if "PT" in c]
        # Term columns
        term_cols = [c for c in student_df.columns if "Term" in c]

        if not pt_cols and not term_cols:
            print("No PT/Term columns found.")
            return None
        # Group by Session + Year
        pt_df = student_df.groupby(["Year", "Session"])[pt_cols].mean(numeric_only=True)
        term_df = student_df.groupby(["Year", "Session"])[term_cols].mean(numeric_only=True)

        return {"PT": pt_df, "Term": term_df}
    except Exception:
        print("Admission number not found or invalid.")
        return None

def class_subject_analysis(df):
    if df is None or df.empty:
        print("No data available.")
        return None

    classes = df["Class"].unique().tolist()
    print("Available Classes:", classes)
    class_choice = input("Enter Class (e.g., VIII, IX, X): ")

    subjects = set([c.split("_")[0] for c in df.columns if "_" in c])
    print("Available Subjects:", subjects)
    subject_choice = input("Enter Subject (e.g., Maths, Science): ")

    class_df = df[df["Class"] == class_choice]
    subject_cols = [c for c in class_df.columns if c.startswith(subject_choice)]

    if not subject_cols:
        print("No PT/Term columns found for this subject.")
        return None

    stats_df = class_df.groupby("Year")[subject_cols].agg(["min", "max", "mean"])
    return stats_df, subject_choice
