from CodeX import (
    Individual_stud_3,
    extract_student_yearwise,
    extract_all_session_comparison,
    class_subject_analysis,
    get_admission_number,
    load_all_data
)
from CodeP import (
    plot_individual,
    plot_student_yearwise,
    plot_all_session_comparison,
    plot_class_subject_analysis
)

def main():
    df_all = load_all_data()

    if df_all is None or df_all.empty:
        print("No data loaded. Please check file paths and names.")
        return

    while True:
        print("\nChoose analysis type (or type 'EXIT' to quit):")
        print("1. Individual Student Analysis (PT & Term marks)")
        print("2. Student PT% and Term% Across Years")
        print("3. All Sessions Comparison (PT1/PT2 & Term marks)")
        print("4. Class Subject Analysis (Least, Top, Average Marks)")

        choice = input("Enter choice: ")

        if choice.upper() == "EXIT":
            break

        elif choice == "1":
            adm_no = get_admission_number(df_all)
            if adm_no:
                student_df = Individual_stud_3(df_all, adm_no)
                plot_individual(student_df)

        elif choice == "2":
            adm_no = get_admission_number(df_all)
            if adm_no:
                student_dict = extract_student_yearwise(df_all, adm_no)
                plot_student_yearwise(student_dict)

        elif choice == "3":
            adm_no = get_admission_number(df_all)
            if adm_no:
                results = extract_all_session_comparison(df_all, adm_no)
                plot_all_session_comparison(results)

        elif choice == "4":
            subject_results = class_subject_analysis(df_all)
            if subject_results:
                subject_choice = subject_results[1]
                plot_class_subject_analysis(subject_results, subject_choice)

if __name__ == "__main__":
    main()