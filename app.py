import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_lab_reports_no_pii.csv")
    return df

# Function to check password
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Enter password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Enter password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

def main():
    st.title("Lab Reports Analysis")

    df = load_data()

    # Display basic information about the dataset
    st.subheader("Dataset Information")
    st.write(f"Number of records: {len(df)}")
    st.write(f"Number of columns: {len(df.columns)}")

    # Display the first few rows of the dataset
    st.subheader("Sample Data")
    st.dataframe(df.head())

    # Allow users to select columns for analysis
    st.subheader("Column Analysis")
    selected_column = st.selectbox("Select a column to analyze", df.columns)

    # Display basic statistics for the selected column
    st.write(f"Statistics for {selected_column}:")
    st.write(df[selected_column].describe())

    # Create a histogram for numeric columns
    if pd.api.types.is_numeric_dtype(df[selected_column]):
        st.subheader(f"Histogram of {selected_column}")
        fig = px.histogram(df, x=selected_column)
        st.plotly_chart(fig)

    # Create a bar chart for categorical columns
    elif pd.api.types.is_object_dtype(df[selected_column]):
        st.subheader(f"Bar Chart of {selected_column}")
        value_counts = df[selected_column].value_counts()
        fig = px.bar(x=value_counts.index, y=value_counts.values)
        fig.update_layout(xaxis_title=selected_column, yaxis_title="Count")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()