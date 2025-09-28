#  Bank Statement Analyzer  

This project is a **Bank Statement Analysis Tool** built with **Streamlit**, designed to extract, clean, analyze, and visualize transactions from **HDFC** and **ICICI** bank statements (PDF format).  

---

##  Overview  
It provides:  
- Automated **account information extraction** (Account Number, Holder Name, IFSC, MICR, Address).  
- Standardized **transaction extraction** into CSV (date, description, withdrawal, deposit, balance).  
- **Flagged transaction detection** using rule-based conditions.  
- **Visualization** of withdrawals vs deposits.  
- Automated **PDF Report generation** summarizing findings.  

---

##  Features  
Extracts account details from PDF statements (**HDFC & ICICI**).  
Parses transactions into structured **CSV**.  
Detects suspicious/flagged transactions:  
   - Demand Draft (DD) withdrawals > ₹10,000  
   - RTGS deposits > ₹50,000  
   - Transactions with entities like *Guddu, Prabhat, Arif, Coal India*  
Interactive **Streamlit dashboard** for exploration.  
Timeline chart of **withdrawals vs deposits**.  
Generates a professional **PDF summary report**. 

---

## Input Statement

```bash 

https://drive.google.com/drive/folders/1MpnGyA6EzGLn6L4095IKBU4d7KrkyFsH?usp=sharing

```

---

##  Project Structure  

```bash 
Bank_Statement_Analyzer/
│── data/
│   ├── input/                   # Place input PDF statements here
│   ├── output/                  # Extracted CSVs & reports saved here
│
│── src/
│   ├── asset/
│   │   ├── analyze_transactions.py   # Rule-based transaction flagging
│   │   ├── HDFCaccount.py            # Extract HDFC account info
│   │   ├── HDFCtransactions.py       # Extract HDFC transactions
│   │   ├── ICICaccount.py            # Extract ICICI account info
│   │   ├── ICICtransactions.py       # Extract ICICI transactions
│   │   ├── visualize.py              # Timeline plotting & PDF report
│   │
│   ├── DataEractor.py          # Chooses correct account parser
│   ├── extract_transactions.py # Chooses correct transaction parser
│
│── app.py                      # Streamlit app entry point
│── requirements.txt            # Dependencies
│── README.md                   # Documentation

```
---

## Installation  

Clone the repository and install dependencies:  

```bash
git clone https://github.com/yashrank345/Bank_Statement_Analyzer.git
cd Bank_Statement_Analyzer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
---
## Usage

Run Streamlit app:

```bash
streamlit run app.py

```
---

### Workflow

Upload HDFC/ICICI bank statement (PDF).
Select from sidebar:

  - Account Information → Extract account holder details.

  - Transactions Information → Extract and view transaction history.

  - Flagged Transactions → View suspicious transactions.

  - Visualization & Report → Generate timeline chart + PDF summary report.

  - Download CSVs or PDF report from the app.

 - Demand Draft (DD) withdrawals > ₹10,000  

---

## Tech Stack

Python

Streamlit – Web app framework

pdfplumber – PDF text extraction

pandas / numpy – Data handling

matplotlib – Visualization

reportlab – PDF report generation


