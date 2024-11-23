import streamlit as st
import pandas as pd

# Header and Description
st.header("2024 AHI 507 Streamlit Example")
st.subheader("Visualizing NCES 2021 School Learning Modalities Data")
st.text("""This dashboard explores the distribution of learning modalities (Hybrid, In Person, Remote) 
in schools across the U.S. during 2021 using NCES data.""")

# Load the dataset
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])  # convert week to datetime
df['zip_code'] = df['zip_code'].astype(str)  # change zipcode type to string

# Metrics
st.subheader("Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1])
col2.metric("Rows", len(df))
col3.metric("Unique Districts/Schools", df['district_name'].nunique())

# Display the first rows of data
st.dataframe(df)

# Pivot table for visualizations
plot = pd.pivot_table(df, values='student_count', index=['state'],
                      columns=['learning_modality'], aggfunc="sum")
plot = plot.reset_index()

#Radio button visualization
st.subheader("Learning Modalities by State")
status = st.radio("Select Learning Modality", ('Hybrid', 'In Person', 'Remote'))
if status == 'Hybrid':
    st.dataframe(df[df['learning_modality'] == 'Hybrid'])
    st.bar_chart(plot, x="state", y="Hybrid")
elif status == 'In Person':
    st.dataframe(df[df['learning_modality'] == 'In Person'])
    st.bar_chart(plot, x="state", y="In Person")
else:
    st.dataframe(df[df['learning_modality'] == 'Remote'])
    st.bar_chart(plot, x="state", y="Remote")

#Multiselect visualization
st.subheader("Compare Multiple Learning Modalities")
selected_modalities = st.multiselect("Select Learning Modalities:",
                                     ['Hybrid', 'In Person', 'Remote'])
if selected_modalities:
    st.bar_chart(plot, x="state", y=selected_modalities)

#Create slider for filtering student count
min_students = int(df['student_count'].min())
max_students = int(df['student_count'].max())

student_limit = st.slider(
    "Select the maximum number of students:",
    min_value=min_students,
    max_value=max_students,
    value=max_students // 2  # Default to half the maximum student count
)

#filter the dataset
filtered_df = df[df['student_count'] <= student_limit]

#Additional Data Summary
st.subheader("Summary Statistics")
st.text("Distribution of student counts across learning modalities:")
summary = df.groupby('learning_modality')['student_count'].sum()
st.dataframe(summary)

#Line Chart by Week
st.subheader("Student Count Trends Over Time")
weekly_plot = pd.pivot_table(df, values='student_count', index=['week_recoded'],
                             columns=['learning_modality'], aggfunc="sum")
st.line_chart(weekly_plot)

