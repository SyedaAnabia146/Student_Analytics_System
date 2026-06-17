import csv
import os

SUBJECT_COLS = ["math", "english", "science", "urdu", "computer"]
MAX_MARKS_PER_SUBJECT = 100
TOTAL_MAX = MAX_MARKS_PER_SUBJECT * len(SUBJECT_COLS)


def calculate_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 65:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "Fail"


def enrich_records(records):
    """Attaches total, average, percentage, and grade to each student dict."""
    enriched = []
    for r in records:
        student = dict(r)
        total = sum(student[s] for s in SUBJECT_COLS)
        average = total / len(SUBJECT_COLS)
        percentage = (total / TOTAL_MAX) * 100
        student["total"]      = total
        student["average"]    = round(average, 2)
        student["percentage"] = round(percentage, 2)
        student["grade"]      = calculate_grade(percentage)
        enriched.append(student)
    return enriched


def get_top_performers(enriched, threshold=75.0):
    top = [s for s in enriched if s["percentage"] >= threshold]
    return sorted(top, key=lambda x: x["percentage"], reverse=True)


def get_weak_students(enriched, threshold=50.0):
    weak = [s for s in enriched if s["percentage"] < threshold]
    return sorted(weak, key=lambda x: x["percentage"])


def subject_wise_average(enriched):
    averages = {}
    for subject in SUBJECT_COLS:
        scores = [s[subject] for s in enriched]
        averages[subject] = round(sum(scores) / len(scores), 2) if scores else 0.0
    return averages


def class_wise_performance(enriched):
    class_groups = {}
    for student in enriched:
        cls = student["class"]
        class_groups.setdefault(cls, []).append(student["percentage"])

    summary = {}
    for cls, percentages in sorted(class_groups.items()):
        summary[cls] = {
            "count":   len(percentages),
            "average": round(sum(percentages) / len(percentages), 2),
            "highest": round(max(percentages), 2),
            "lowest":  round(min(percentages), 2),
        }
    return summary


#  Reporting 

def export_summary_report(enriched, filename="student_summary_report.csv"):
    fieldnames = [
        "student_id", "name", "class",
        "math", "english", "science", "urdu", "computer",
        "total", "average", "percentage", "grade"
    ]
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(enriched)
        print(f"\n Report saved → '{filename}'")
    except Exception as e:
        print(f"[Error] Could not write report: {e}")


#  Display helpers

def show_performance_table(enriched):
    print("\n" + "=" * 85)
    print(f"{'ID':<8} {'Name':<20} {'Class':<6} {'Total':>6} {'Avg':>6} {'%':>7} {'Grade':>5}")
    print("-" * 85)
    for s in enriched:
        print(
            f"{s['student_id']:<8} {s['name']:<20} {s['class']:<6} "
            f"{s['total']:>6} {s['average']:>6} {s['percentage']:>6.1f}% {s['grade']:>5}"
        )
    print("=" * 85)


def show_top_performers(enriched):
    top = get_top_performers(enriched)
    print(f"\n Top Performers (percentage ≥ 75%): {len(top)} student(s)")
    if not top:
        print("  None found.")
        return
    print(f"  {'Name':<20} {'Class':<6} {'%':>6} {'Grade':>5}")
    print("  " + "-" * 42)
    for s in top:
        print(f"  {s['name']:<20} {s['class']:<6} {s['percentage']:>5.1f}% {s['grade']:>5}")


def show_weak_students(enriched):
    weak = get_weak_students(enriched)
    print(f"\n Weak Students (percentage < 50%): {len(weak)} student(s)")
    if not weak:
        print("  None found.")
        return
    print(f"  {'Name':<20} {'Class':<6} {'%':>6} {'Grade':>5}")
    print("  " + "-" * 42)
    for s in weak:
        print(f"  {s['name']:<20} {s['class']:<6} {s['percentage']:>5.1f}% {s['grade']:>5}")


def show_subject_averages(enriched):
    avgs = subject_wise_average(enriched)
    print("\n Subject-wise Class Average:")
    print("  " + "-" * 28)
    for subject, avg in avgs.items():
        bar = "█" * int(avg // 5)
        print(f"  {subject.capitalize():<10} {avg:>5.1f}  {bar}")
    print()


def show_class_comparison(enriched):
    summary = class_wise_performance(enriched)
    print("\n Class-wise Performance Summary:")
    print(f"  {'Class':<8} {'Students':>8} {'Avg %':>7} {'Highest':>8} {'Lowest':>7}")
    print("  " + "-" * 44)
    for cls, data in summary.items():
        print(
            f"  {cls:<8} {data['count']:>8} {data['average']:>6.1f}% "
            f"{data['highest']:>7.1f}% {data['lowest']:>6.1f}%"
        )
