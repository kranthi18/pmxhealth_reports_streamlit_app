import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data from cleaned_lab_data.csv
df = pd.read_csv("cleaned_lab_reports_no_pii_combined_long.csv")

# st.header("Patient and Medical Values Overview")

# Display the number of patients
num_patients = df['patient_id'].nunique()

# Display the number of medical values (excluding patient_id)
num_medical_values = df['medical_attribute_name'].nunique()

# Calculate statistics for the 'age' column
age_stats = {
    'Average Age': df['age'].mean(),
    'Minimum Age': df['age'].min(),
    'Maximum Age': df['age'].max(),
    'Median Age': df['age'].median()
}


# Calculate the number of male and female patients
num_female_patients = df[df['gender'].str.lower() == 'female']['patient_id'].nunique()
num_male_patients = df[df['gender'].str.lower() == 'male']['patient_id'].nunique()


st.subheader("Dashboard Overview")
# Display the statistics as big numbers
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("# Patients", num_patients)

with col2:
    st.metric("# Medical Attributes", num_medical_values)

with col3:
    st.metric("Average Age", f"{age_stats['Average Age']:.2f}")

with col4:
    st.metric("Minimum Age", f"{age_stats['Minimum Age']:.2f}")

with col5:
    st.metric("Maximum Age", f"{age_stats['Maximum Age']:.2f}")

with col6:
    st.metric("Median Age", f"{age_stats['Median Age']:.2f}")

col7, col8 = st.columns(2)

with col7:
    st.metric("Number of Female Patients", num_female_patients)

with col8:
    st.metric("Number of Male Patients", num_male_patients)



# Allow users to select medical attributes for charting
medical_attributes = [col for col in df.columns if col != 'patient_id']
medical_attribute = st.selectbox("Select a medical attribute to visualize", medical_attributes)

# Create a chart based on the selected medical attribute
if medical_attribute in ['age', 'gender', 'collection_date']:
    # Use only unique patient_ids for these attributes
    unique_df = df.drop_duplicates(subset=['patient_id'])
    
    if pd.api.types.is_numeric_dtype(unique_df[medical_attribute]):
        st.subheader(f"Histogram of {medical_attribute}")
        fig = px.histogram(unique_df, x=medical_attribute)
    else:
        st.subheader(f"Bar Chart of {medical_attribute}")
        value_counts = unique_df[medical_attribute].value_counts()
        fig = px.bar(x=value_counts.index, y=value_counts.values)
        fig.update_layout(xaxis_title=medical_attribute, yaxis_title="Count")
    
    st.plotly_chart(fig)
else:
    if pd.api.types.is_numeric_dtype(df[medical_attribute]):
        st.subheader(f"Histogram of {medical_attribute}")
        fig = px.histogram(df, x=medical_attribute)
    elif pd.api.types.is_object_dtype(df[medical_attribute]):
        st.subheader(f"Bar Chart of {medical_attribute}")
        value_counts = df[medical_attribute].value_counts()
        fig = px.bar(x=value_counts.index, y=value_counts.values)
        fig.update_layout(xaxis_title=medical_attribute, yaxis_title="Count")
    
    st.plotly_chart(fig)