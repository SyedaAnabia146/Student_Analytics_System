import csv
import os

CSV_FILE = "students.csv"

COLUMNS = ["student_id", "name", "class", "math", "english", "science", "urdu", "computer"]
SUBJECT_COLS = ["math", "english", "science", "urdu", "computer"]


def load_data():
    if not os.path.exists(CSV_FILE):
        print(f"[Warning] '{CSV_FILE}' not found. Starting with an empty dataset.")
        return []

    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = []
            for row in reader:
                try:
                    for col in SUBJECT_COLS:
                        row[col] = int(row[col])
                except ValueError:
                    print(f"[Warning] Skipping malformed record: {row.get('student_id', '?')}")
                    continue
                records.append(row)
        return records
    except Exception as e:
        print(f"[Error] Could not read data file: {e}")
        return []


def save_data(records):
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(records)
    except Exception as e:
        print(f"[Error] Failed to save data: {e}")


def _find_student(records, student_id):
    for i, record in enumerate(records):
        if record["student_id"] == student_id:
            return i
    return -1


def view_all_students(records):
    if not records:
        print("\nNo student records found.")
        return

    print("\n" + "=" * 75)
    print(f"{'ID':<8} {'Name':<20} {'Class':<6} {'Math':>5} {'Eng':>5} {'Sci':>5} {'Urdu':>5} {'Comp':>5}")
    print("-" * 75)
    for r in records:
        print(
            f"{r['student_id']:<8} {r['name']:<20} {r['class']:<6} "
            f"{r['math']:>5} {r['english']:>5} {r['science']:>5} "
            f"{r['urdu']:>5} {r['computer']:>5}"
        )
    print("=" * 75)
    print(f"Total records: {len(records)}\n")


def add_student(records):
    print("\n-- Add New Student --")
    try:
        student_id = input("Student ID (e.g. S011): ").strip().upper()
        if _find_student(records, student_id) != -1:
            print(f"[Error] ID '{student_id}' already exists.")
            return records

        name = input("Full Name: ").strip()
        if not name:
            print("[Error] Name cannot be empty.")
            return records

        class_name = input("Class (e.g. 10A): ").strip().upper()

        marks_dict = {}
        for subject in SUBJECT_COLS:
            while True:
                try:
                    val = int(input(f"{subject.capitalize()} marks (0-100): "))
                    if not 0 <= val <= 100:
                        raise ValueError
                    marks_dict[subject] = val
                    break
                except ValueError:
                    print("  Please enter a whole number between 0 and 100.")

        new_record = {"student_id": student_id, "name": name, "class": class_name, **marks_dict}
        records.append(new_record)
        save_data(records)
        print(f"\n Student '{name}' added successfully.")

    except KeyboardInterrupt:
        print("\n[Cancelled] No changes were made.")

    return records


def update_marks(records):
    print("\n-- Update Student Marks --")
    student_id = input("Enter Student ID to update: ").strip().upper()

    idx = _find_student(records, student_id)
    if idx == -1:
        print(f"[Error] No student found with ID '{student_id}'.")
        return records

    print(f"Updating marks for: {records[idx]['name']}")

    for subject in SUBJECT_COLS:
        current = records[idx][subject]
        raw = input(f"  {subject.capitalize()} (current: {current}, press Enter to skip): ").strip()
        if raw == "":
            continue
        try:
            new_val = int(raw)
            if not 0 <= new_val <= 100:
                raise ValueError
            records[idx][subject] = new_val
        except ValueError:
            print(f"  Invalid input for {subject} — keeping original value.")

    save_data(records)
    print("Marks updated successfully.")
    return records


def delete_student(records):
    print("\n-- Delete Student Record --")
    student_id = input("Enter Student ID to delete: ").strip().upper()

    idx = _find_student(records, student_id)
    if idx == -1:
        print(f"[Error] No student with ID '{student_id}' found.")
        return records

    student_name = records[idx]["name"]
    confirm = input(f"Are you sure you want to delete '{student_name}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return records

    records.pop(idx)
    save_data(records)
    print(f"Record for '{student_name}' has been deleted.")
    return records