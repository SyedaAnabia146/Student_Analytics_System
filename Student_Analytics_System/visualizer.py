import os

try:
    import matplotlib
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from analytics import subject_wise_average, class_wise_performance, get_top_performers

OUTPUT_DIR = "Charts"


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_subject_averages(enriched):
    avgs = subject_wise_average(enriched)
    subjects = [s.capitalize() for s in avgs]
    values = list(avgs.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(subjects, values, color="#4C72B0", edgecolor="white", width=0.55)

    ax.set_ylim(0, 110)
    ax.set_ylabel("Average Marks (out of 100)")
    ax.set_title("Subject-wise Class Average", fontsize=14, fontweight="bold")
    ax.axhline(50, color="red", linestyle="--", linewidth=0.9, label="Pass line (50)")
    ax.axhline(75, color="green", linestyle="--", linewidth=0.9, label="Top performer line (75)")
    ax.legend(fontsize=9)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val}", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    _ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, "subject_averages.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"   Chart saved → '{path}'")


def plot_class_performance(enriched):
    summary = class_wise_performance(enriched)
    classes = list(summary.keys())
    averages = [summary[c]["average"] for c in classes]

    colors = ["#55A868", "#C44E52", "#4C72B0", "#DD8452"][:len(classes)]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(classes, averages, color=colors, edgecolor="white", width=0.5)

    ax.set_ylim(0, 110)
    ax.set_ylabel("Average Percentage (%)")
    ax.set_title("Class-wise Average Performance", fontsize=14, fontweight="bold")

    for bar, val in zip(bars, averages):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val}%", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    _ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, "class_performance.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"   Chart saved → '{path}'")


def plot_top_performers(enriched):
    top = get_top_performers(enriched)
    if not top:
        print("   No top performers to chart.")
        return

    names = [s["name"].split()[0] for s in top]
    percentages = [s["percentage"] for s in top]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(names, percentages, color="#4C72B0", edgecolor="white")

    ax.set_xlim(0, 115)
    ax.set_xlabel("Percentage (%)")
    ax.set_title("Top Performing Students (>= 75%)", fontsize=14, fontweight="bold")
    ax.axvline(75, color="green", linestyle="--", linewidth=0.9, label="Threshold 75%")
    ax.legend(fontsize=9)
    ax.invert_yaxis()

    for bar, val in zip(bars, percentages):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val}%", va="center", fontsize=9)

    plt.tight_layout()
    _ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, "top_performers.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"   Chart saved → '{path}'")


def _text_bar_chart(enriched):
    avgs = subject_wise_average(enriched)
    print("\n   Subject Averages (text chart):")
    print("   " + "-" * 40)
    for subject, avg in avgs.items():
        filled = int(avg // 2.5)
        bar = "█" * filled + "░" * (40 - filled)
        print(f"   {subject.capitalize():<10} |{bar}| {avg:>5.1f}")
    print()


def run_visualizations(enriched):
    if not enriched:
        print("\n No data available to visualize.")
        return

    if not MATPLOTLIB_AVAILABLE:
        print("\n[Note] matplotlib not found — showing text-based charts instead.\n")
        _text_bar_chart(enriched)
        return

    print("\n Generating and updating system graphs...")
    plot_subject_averages(enriched)
    plot_class_performance(enriched)
    plot_top_performers(enriched)
    print("\n All system charts successfully refreshed inside 'Charts/' directory.")