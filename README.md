# 🎓 Student Performance Dashboard

An interactive dashboard built with Python and Streamlit to analyze student performance data. It provides insightful statistics, dynamic charts, and detailed views of student metrics based on a sample dataset.

## ✨ Features

- **Dashboard Overview**: View key performance indicators (KPIs) like total students, average exam scores, average attendance, and pass percentage.
- **Performance Analysis Charts**: Analyze exam scores by gender, study hours, and attendance through interactive visual charts.
- **Dynamic Filters**: Filter the dashboard by gender, grade, attendance range, and study hours.
- **Student Search**: Find individual students using their Student ID to view their detailed academic metrics.
- **Basic Insights**: Auto-generated text insights based on the selected dataset and filters.

## 📊 Dataset

The dataset is a sample CSV (`students.csv`) containing the following columns:
- `Student ID`: Unique identifier for each student.
- `Gender`: Male / Female.
- `Age`: Age of the student.
- `Study hours`: Number of hours studied per week.
- `Attendance`: Attendance percentage.
- `Previous scores`: Scores from previous assessments.
- `Assignment scores`: Scores from recent assignments.
- `Exam score`: The final exam score.
- `Final performance/grade`: The letter grade assigned (A, B, C, D, F).

## 🛠 Technologies Used

- **[Python](https://www.python.org/)** - Core programming language.
- **[Pandas](https://pandas.pydata.org/)** - Data analysis and manipulation.
- **[Streamlit](https://streamlit.io/)** - Dashboard web application framework.
- **[Plotly](https://plotly.com/python/)** - Interactive data visualization.

## 📸 Dashboard Screenshots

*(Add screenshots of your working dashboard here)*

## 🚀 Installation

1. **Clone or Download the Repository:**
   Download the project files into a folder named `student-performance-dashboard`.

2. **Navigate to the Directory:**
   ```bash
   cd student-performance-dashboard
   ```

3. **Install Dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ How to Run

After installing the requirements, run the following command in your terminal:

```bash
streamlit run app.py
```
This will open the dashboard automatically in your default web browser (usually at `http://localhost:8501`).

## 📈 Example Analysis

Using the built-in dataset, you can see how **Study Hours** and **Attendance** directly influence the **Exam Score**. The dashboard's interactive scatter plots clearly show an upward trend: students with higher study hours and better attendance tend to score higher grades (A and B).

## 🔮 Future Improvements

- Integrate a real database (e.g., SQLite or PostgreSQL).
- Add user authentication for teachers vs. students.
- Incorporate Machine Learning to predict future exam scores based on study hours and attendance.
- Export filtered data to PDF/CSV directly from the dashboard.
