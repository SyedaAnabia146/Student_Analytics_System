from data_manager import load_data, view_all_students, add_student, update_marks, delete_student
from analytics import (
    enrich_records, show_performance_table, show_top_performers,
    show_weak_students, show_subject_averages, show_class_comparison,
    export_summary_report
)
from visualizer import run_visualizations


def print_menu():
    print("\n")
    print("   Student Performance Analytics System")
    print("")
    print(" 1. View All Students")
    print(" 2. Add New Student")
    print(" 3. Update Student Marks")
    print(" 4. Delete Student")
    print(" ")
    print(" 5. Performance Summary (Grades & Totals)")
    print(" 6. Analytics Dashboard")
    print(" 7. Export Summary Report (CSV)")
    print(" 8. Show Visualizations (Charts)")
    print(" 0. Exit")
    print("")


def analytics_dashboard(records):
    if not records:
        print("\n No data to analyze.")
        return
    enriched = enrich_records(records)
    show_top_performers(enriched)
    show_weak_students(enriched)
    show_subject_averages(enriched)
    show_class_comparison(enriched)


def main():
    records = load_data()
    print(f"\n Data loaded. {len(records)} student records found.")

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            view_all_students(records)

        elif choice == "2":
            records = add_student(records)

        elif choice == "3":
            records = update_marks(records)

        elif choice == "4":
            records = delete_student(records)

        elif choice == "5":
            if not records:
                print("\n No records available.")
            else:
                show_performance_table(enrich_records(records))

        elif choice == "6":
            analytics_dashboard(records)

        elif choice == "7":
            if not records:
                print("\n No records to export.")
            else:
                export_summary_report(enrich_records(records))

        elif choice == "8":
            if not records:
                print("\n No records available.")
            else:
                run_visualizations(enrich_records(records))

        elif choice == "0":
            print("\nExiting system. Goodbye!\n")
            break

        else:
            print("[!] Invalid option. Please choose from the menu above.")


if __name__ == "__main__":
    main()
