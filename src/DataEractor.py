import re
from src.asset.ICICaccount import account_ICIC_info
from src.asset.HDFCaccount import account_HDFC_info
import pdfplumber as pf
import pandas as pd

def account_info(pdf_path):
    # Extract first page text 
    with pf.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text() or ""

    # Extract IFSC from first page 
    match_ifsc = re.search(r"\b([A-Z]{4}0[A-Z0-9]{6})\b", first_page_text, re.IGNORECASE)
    if not match_ifsc:
        print("DEBUG: Could not find IFSC code, first page text:\n")
        
    ifsc = match_ifsc.group(1).upper()
    bank_code = ifsc[:4]

   
    bank_map = {
        "HDFC": account_HDFC_info,
        "ICIC": account_ICIC_info,
        
    }

    parser_func = bank_map.get(bank_code)
    if not parser_func:
        raise ValueError(f"Unsupported bank code detected in IFSC: {bank_code}")

    #  Extract account info using the proper parser 
    info = parser_func(pdf_path)

    #  Save output CSV 
    df = pd.DataFrame([info])
    df.to_csv("data/output/account_info.csv", index=False)
    print("[INFO] Account information extracted -> data/output/account_info.csv")

    return info
