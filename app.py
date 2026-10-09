import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI improvement
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Function to load and cache the dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('students.csv')
        
        # Ensure numerical types
        numeric_cols = ['Attendance', 'Study hours', 'Exam score', 'Previous scores', 'Assignment scores']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing values with median for numerical columns
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
                
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# --- Title and Header ---
st.title("🎓 Student Performance Dashboard")
st.markdown("Analyze student performance data, discover trends, and view individual statistics.")
st.markdown("---")

# --- Sidebar for Filters ---
st.sidebar.header("🔍 Filters")

# Gender filter
gender_options = ["All"] + sorted(list(df['Gender'].dropna().unique()))
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

# Grade filter
grade_options = ["All"] + sorted(list(df['Final performance/grade'].dropna().unique()))
selected_grade = st.sidebar.selectbox("Select Grade", grade_options)

# Attendance filter
min_att, max_att = float(df['Attendance'].min()), float(df['Attendance'].max())
attendance_range = st.sidebar.slider("Attendance Range (%)", min_att, max_att, (min_att, max_att))

# Study hours filter
min_sh, max_sh = float(df['Study hours'].min()), float(df['Study hours'].max())
study_hours_range = st.sidebar.slider("Study Hours Range", min_sh, max_sh, (min_sh, max_sh))

# --- Apply Filters ---
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_grade != "All":
    filtered_df = filtered_df[filtered_df['Final performance/grade'] == selected_grade]

filtered_df = filtered_df[
    (filtered_df['Attendance'] >= attendance_range[0]) & 
    (filtered_df['Attendance'] <= attendance_range[1])
]

filtered_df = filtered_df[
    (filtered_df['Study hours'] >= study_hours_range[0]) & 
    (filtered_df['Study hours'] <= study_hours_range[1])
]

# --- 1. Dashboard Overview (KPIs) ---
st.markdown("### 📊 Overview KPIs")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your criteria.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_students = len(filtered_df)
    avg_exam_score = filtered_df['Exam score'].mean()
    avg_attendance = filtered_df['Attendance'].mean()
    avg_study_hours = filtered_df['Study hours'].mean()
    
    # Calculate pass percentage (assuming >= 60 is Pass, Grades A-D)
    pass_count = len(filtered_df[filtered_df['Exam score'] >= 60])
    pass_percentage = (pass_count / total_students) * 100 if total_students > 0 else 0
    
    with col1:
        st.metric("Total Students", f"{total_students}")
    with col2:
        st.metric("Avg Exam Score", f"{avg_exam_score:.1f}")
    with col3:
        st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    with col4:
        st.metric("Avg Study Hours", f"{avg_study_hours:.1f} hrs")
    with col5:
        st.metric("Pass Percentage", f"{pass_percentage:.1f}%")

    st.markdown("---")

    # --- 2. Performance Analysis Charts ---
    st.markdown("### 📈 Performance Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Average score by gender
        avg_score_gender = filtered_df.groupby('Gender')['Exam score'].mean().reset_index()
        fig_gender = px.bar(
            avg_score_gender, 
            x='Gender', 
            y='Exam score', 
            color='Gender',
            title='Average Exam Score by Gender',
            text_auto='.1f',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_gender.update_layout(xaxis_title="Gender", yaxis_title="Average Score")
        st.plotly_chart(fig_gender, use_container_width=True)
        
    with chart_col2:
        # Score Distribution
        fig_dist = px.histogram(
            filtered_df, 
            x='Exam score', 
            nbins=10,
            title='Exam Score Distribution',
            color_discrete_sequence=['#3498db']
        )
        fig_dist.update_layout(xaxis_title="Exam Score", yaxis_title="Number of Students")
        st.plotly_chart(fig_dist, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        # Study hours vs Exam score
        fig_study = px.scatter(
            filtered_df, 
            x='Study hours', 
            y='Exam score', 
            color='Final performance/grade',
            hover_data=['Student ID'],
            title='Study Hours vs Exam Score'
        )
        st.plotly_chart(fig_study, use_container_width=True)
        
    with chart_col4:
        # Attendance vs Exam score
        fig_att = px.scatter(
            filtered_df, 
            x='Attendance', 
            y='Exam score', 
            color='Final performance/grade',
            hover_data=['Student ID'],
            title='Attendance vs Exam Score'
        )
        st.plotly_chart(fig_att, use_container_width=True)

    # Number of students by grade
    grade_counts = filtered_df['Final performance/grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    # Sorting grades properly (A, B, C, D, F)
    grade_order = ['A', 'B', 'C', 'D', 'F']
    grade_counts['Grade'] = pd.Categorical(grade_counts['Grade'], categories=grade_order, ordered=True)
    grade_counts = grade_counts.sort_values('Grade')
    
    fig_grades = px.bar(
        grade_counts, 
        x='Grade', 
        y='Count', 
        color='Grade',
        title='Number of Students by Grade',
        text_auto=True,
        category_orders={"Grade": grade_order},
        color_discrete_sequence=['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']
    )
    st.plotly_chart(fig_grades, use_container_width=True)

    st.markdown("---")

    # --- 4. Student Search ---
    st.markdown("### 🧑‍🎓 Student Search")
    
    student_ids = df['Student ID'].tolist()
    search_query = st.selectbox("Select or type a Student ID to view details", [""] + student_ids)
    
    if search_query:
        student_data = df[df['Student ID'] == search_query].iloc[0]
        
        st.info(f"**Viewing Details for Student: {student_data['Student ID']}**")
        s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
        
        s_col1.metric("Study Hours", f"{student_data['Study hours']} hrs")
        s_col2.metric("Attendance", f"{student_data['Attendance']}%")
        s_col3.metric("Previous Score", f"{student_data['Previous scores']}")
        s_col4.metric("Exam Score", f"{student_data['Exam score']}")
        s_col5.metric("Grade", f"{student_data['Final performance/grade']}")

    st.markdown("---")
    
    # --- 5. Basic Insights ---
    st.markdown("### 💡 Basic Insights")
    
    highest_score = filtered_df['Exam score'].max()
    lowest_score = filtered_df['Exam score'].min()
    
    correlation_study = filtered_df['Study hours'].corr(filtered_df['Exam score'])
    correlation_text = "strong positive" if pd.notna(correlation_study) and correlation_study > 0.6 else "moderate positive" if pd.notna(correlation_study) and correlation_study > 0.3 else "weak or no"
    
    st.success(f"**1. Average Score:** The average exam score for the selected criteria is **{avg_exam_score:.1f}**.")
    st.success(f"**2. Extremes:** The highest score is **{highest_score}** and the lowest is **{lowest_score}**.")
    st.success(f"**3. Pass Rate:** **{pass_count}** out of {total_students} students passed the exam ({pass_percentage:.1f}%).")
    if pd.notna(correlation_study):
        st.success(f"**4. Study Impact:** There is a **{correlation_text}** relationship (correlation = {correlation_study:.2f}) between study hours and exam performance.")
    else:
        st.success("**4. Study Impact:** Not enough varied data to calculate correlation.")
