import streamlit as st
import pandas as pd
import os
import sys

sys.path.append("src")
from src.DataEractor import account_info
from src.extract_transactions import extract_transactions
from src.asset.analyze_transactions import analyze_transactions
from src.asset.visualize import plot_timeline, create_pdf_report

st.set_page_config(page_title="Bank Statement Analyzer", layout="wide")

st.title("Bank Statement Analyzer")
st.write("Upload your HDFC or ICICI bank statement (PDF) to extract account info and transactions.")

# File Upload 
uploaded_file = st.file_uploader("Upload Bank Statement (PDF)", type=["pdf"])

if uploaded_file:
    # Save uploaded file temporarily
    input_path = os.path.join("data", "input", uploaded_file.name)
    os.makedirs("data/input", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    select_type = st.sidebar.radio(
        'Select',
        ['Account Information', 'Transactions Information', 'Flagged Transactions', 'Visualization & Report']
    )

    # Account Information
    if select_type == 'Account Information':
        st.subheader("Account Information")
        account_data = account_info(input_path)
        st.json(account_data)

        account_df = pd.DataFrame([account_data])  # wrap dict in a list
        st.download_button(
            "Download Account Information CSV",
            account_df.to_csv(index=False).encode("utf-8"),
            "account_info.csv",
            "text/csv"
        )

    # Transactions
    elif select_type == 'Transactions Information':
        st.subheader("Transactions")
        df = extract_transactions(input_path)
        st.dataframe(df)

        st.download_button(
            "Download Transactions CSV",
            df.to_csv(index=False).encode("utf-8"),
            "transactions.csv",
            "text/csv"
        )

    # Flagged Transactions
    elif select_type == 'Flagged Transactions':
        st.subheader("Flagged Transactions")
        df = extract_transactions(input_path)
        flagged = analyze_transactions(df)

        for key, flagged_df in flagged.items():
            st.write(f"**{key}: {len(flagged_df)} transactions**")
            st.dataframe(flagged_df)

    # Visualization & Report
    elif select_type == 'Visualization & Report':
        st.subheader("Visualization & Report")
        df = extract_transactions(input_path)
        chart_path = plot_timeline(df)
        st.image(chart_path)

        flagged = analyze_transactions(df)
        report_path = create_pdf_report("Yash Rank", "yashrank48@gmail.com", flagged, chart_path)

        with open(report_path, "rb") as f:
            st.download_button("Download PDF Report", f, file_name="Summary_Report.pdf")
