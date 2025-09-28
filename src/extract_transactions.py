import re
import pdfplumber as pf
import pandas as pd
from src.asset.HDFCtransactions import HDFC_transactions
from src.asset.ICICtransactions import ICIC_transactions


def extract_transactions(pdf_path):
    # Extract first page text 
    with pf.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text() or ""

    # Extract IFSC from first page 
    match_ifsc = re.search(r"\b([A-Z]{4}0[A-Z0-9]{6})\b", first_page_text, re.IGNORECASE)
    if not match_ifsc:
        print("DEBUG: Could not find IFSC code, first page text:\n", first_page_text)
        raise ValueError("Could not extract IFSC code from statement")

    ifsc = match_ifsc.group(1).upper()
    bank_code = ifsc[:4]

    bank_map = {
        "HDFC": HDFC_transactions,
        "ICIC": ICIC_transactions,
    }

    parser_func = bank_map.get(bank_code)
    if not parser_func:
        raise ValueError(f"Unsupported bank code detected in IFSC: {bank_code}")

    # Extract transactions using the proper parser 
    info = parser_func(pdf_path)

    # Convert into DataFrame (assuming list of dicts)
    df = pd.DataFrame(info)

    # Save output CSV 
    df.to_csv("data/output/transactions.csv", index=False)
    print("[INFO] Transactions extracted -> data/output/transactions.csv")

    return df
