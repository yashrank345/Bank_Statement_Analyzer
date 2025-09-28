import pdfplumber as pf
import pandas as pd
import re
import os

def safe_float(value):
    """Convert string to float safely, return 0.0 if invalid."""
    try:
        if value is None:
            return 0.0
        value = str(value).replace(",", "").replace("Cr", "").replace("Dr", "").strip()
        value = re.sub(r"[^0-9.\-]", "", value)  # keep only digits, dot, minus
        if value in ("", ".", "-", "--"):
            return 0.0
        return float(value)
    except:
        return 0.0

def ICIC_transactions(pdf_path, output_dir="data/output", output_excel="transactions.csv"):
    transactions = []
    with pf.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            # Skip header row
            for row in table[1:]:
                if len(row) < 6:
                    continue

                date = str(row[0]).strip()
                desc = str(row[1]).strip()
                withdrawal = safe_float(row[3])
                deposit = safe_float(row[4])
                balance = safe_float(row[-1])  # always last column (handles Cr/Dr)

                # Clean date
                date = re.sub(r"[^0-9/\-]", "", date)

                transactions.append({
                    "transaction_date": date,
                    "description": desc,
                    "withdrawal_amount": withdrawal,
                    "deposit_amount": deposit,
                    "balance": balance
                })

    ICIC_df = pd.DataFrame(transactions)

    # Keep only rows with valid date format
    ICIC_df = ICIC_df[ICIC_df["transaction_date"].str.match(r"\d{2}[-/]\d{2}[-/]\d{4}", na=False)]
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, output_excel)
    ICIC_df.to_csv(out_file, index=False)
    print(f"[INFO] Transactions saved -> {out_file}")

    return ICIC_df
