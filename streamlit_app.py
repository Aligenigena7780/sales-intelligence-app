import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Intelligence", layout="wide")

st.title("📊 Sales Intelligence Platform")

st.write("Upload your sales report to start analyzing your data.")

uploaded_file = st.file_uploader("Upload a sales file (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Basic Data Information")
    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    numeric_columns = df.select_dtypes(include=["number"]).columns

    if len(numeric_columns) > 0:
        column = st.selectbox("Select a numeric column to visualize", numeric_columns)
        st.subheader("Chart")
        st.bar_chart(df[column])
