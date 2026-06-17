# Student Analytics Hub

An executive-level visual intelligence platform built with Python and Streamlit to monitor, manage, and analyze student academic performance. This application provides a central data matrix, section-wise performance tracking, and live-rendered analytical visualizations designed for institutional monitoring.

---

## ⚡ Key Features

*   **Central Registry Ledger:** A real-time, interactive data grid view displaying all authenticated student database records securely.
*   **Section Analytics Matrix:** Live distribution mapping and cohort performance statistics calculated automatically across active sections.
*   **Executive Visual Gallery:** Dynamically rendered analytical charts (Subject Index, Cohort Performance, and Academic Merit) using Matplotlib.
*   **Administrative Mutation Desk:** A secure system control panel allowing administrators to register new profiles, perform database overwrites, and purge entry records.
*   **System Diagnostics Logs:** Integrated database health monitoring that tracks file integrity and visualization sync status.

---

## 🛠️ Technology Stack

*   **Core Logic:** Python 3
*   **User Interface:** Streamlit (Custom Premium Jet-Black Executive Theme)
*   **Data Processing:** Pandas DataFrames & Custom Analytical Algorithms
*   **Data Visualization:** Matplotlib Data Rendering Engine

---

## 📦 System Architecture & Files

*   `app.py` - Main dashboard deployment file containing layout configurations and theme styling.
*   `analytics.py` - Math and analytics processing engine for grades, averages, and ranking matrices.
*   `data_manager.py` - Core storage module handling data persistence, CSV loading, and saving routines.
*   `visualizer.py` - Custom rendering module for executive graphs and charts.
*   `main.py` - Core engine script for background workflows.
*   `students.csv` & `student_summary_report.csv` - Central database and reporting storage sheets.
*   `requirements.txt` - Dependency layout configuration file.

---

## 🚀 Installation & Setup Guide

Follow these exact steps to run the application on your local machine:

### 1. Install Project Dependencies
Open your project terminal and install all the required Python libraries using the package manager:
```bash
pip install streamlit pandas matplotlib
