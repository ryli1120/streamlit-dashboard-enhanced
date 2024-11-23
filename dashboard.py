import streamlit as st
import pandas as pd

# Header and Description
st.header("2024 AHI 507 Streamlit Enhanced Example")
st.subheader("Visualizing NCES 2021 School Learning Modalities Data")
st.text("""This dashboard explores the distribution of learning modalities (Hybrid, In Person, Remote) 
in schools across the U.S. during 2021 using NCES data.""")

# Load the dataset
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])  # Convert 'week' to datetime
df['zip_code'] = df['zip_code'].astype(str)  # Ensure ZIP code is treated as a string

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

# Radio Button Visualization
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

# Multiselect Visualization
st.subheader("Compare Multiple Learning Modalities")
selected_modalities = st.multiselect("Select Learning Modalities:",
                                     ['Hybrid', 'In Person', 'Remote'])
if selected_modalities:
    st.bar_chart(plot, x="state", y=selected_modalities)

# Week Filter with Slider
st.subheader("Filter Data by Week Range")

# Convert Timestamp to datetime.date
week_min = df['week_recoded'].min().date()
week_max = df['week_recoded'].max().date()

# Slider for date range
selected_weeks = st.slider("Select a week range:", value=(week_min, week_max))

# Filter data based on slider selection
filtered_df = df[(df['week_recoded'] >= pd.to_datetime(selected_weeks[0])) &
                 (df['week_recoded'] <= pd.to_datetime(selected_weeks[1]))]

st.write(f"Data for selected weeks ({selected_weeks[0]} to {selected_weeks[1]}):")
st.dataframe(filtered_df)

# Additional Data Summary
st.subheader("Summary Statistics")
st.text("Distribution of student counts across learning modalities:")
summary = df.groupby('learning_modality')['student_count'].sum()
st.dataframe(summary)

# Line Chart by Week
st.subheader("Student Count Trends Over Time")
weekly_plot = pd.pivot_table(df, values='student_count', index=['week_recoded'],
                             columns=['learning_modality'], aggfunc="sum")
st.line_chart(weekly_plot)

# Footer
st.text("Created with Streamlit")

