import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_lab_reports_no_pii_combined.csv")
    return df

def main():
    st.title("Lab Reports Analysis")

    df = load_data()

    # Create tabs
    tab1, tab2 = st.tabs(["Raw Data", "Charts"])

    with tab1:
        st.header("Raw Data Exploration")
        
        # Display basic information about the dataset
        st.subheader("Dataset Information")
        st.write(f"Number of records: {len(df)}")
        st.write(f"Number of columns: {len(df.columns)}")

        # Display the first few rows of the dataset
        st.subheader("Sample Data")
        st.dataframe(df.head())

        # Allow users to search and filter the data
        st.subheader("Search and Filter")
        search_term = st.text_input("Search for a term in the dataset")
        if search_term:
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]
            st.dataframe(filtered_df)

    with tab2:
        st.header("Charts and Analysis")

        # Allow users to select columns for analysis
        selected_column = st.selectbox("Select a column to analyze", df.columns)

        # Display basic statistics for the selected column
        st.subheader(f"Statistics for {selected_column}")
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