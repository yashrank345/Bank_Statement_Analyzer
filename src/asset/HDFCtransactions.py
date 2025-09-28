import pdfplumber
import pandas as pd
import re
import os

def HDFC_transactions(pdf_path, output_dir="data/output", output_excel="transactions.csv"):
    transactions = []
    date_pattern = re.compile(r"^\d{2}/\d{2}/\d{2}")

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split("\n")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Case 1: narration continuation (e.g., "S DEBIT")
                if not date_pattern.match(line) and transactions:
                    transactions[-1]["description"] += " " + line
                    continue

                # Case 2: transaction line
                if not date_pattern.match(line):
                    continue

                # Extract numbers (last two should be amount + balance)
                nums = re.findall(r"-?\d+(?:,\d{3})*(?:\.\d+)?", line)
                nums = [n.replace(",", "") for n in nums]

                if len(nums) < 2:
                    continue

                balance = float(nums[-1])
                amount = float(nums[-2])

                parts = line.split()
                date = parts[0]

                # Remove Txn Date + Value Date if present
                possible_value_date = parts[1] if re.match(r"\d{2}/\d{2}/\d{2}", parts[1]) else None

                # Build description
                desc = line
                desc = desc.replace(date, "", 1)
                if possible_value_date:
                    desc = desc.replace(possible_value_date, "", 1)
                desc = desc.replace(nums[-2], "", 1)
                desc = desc.replace(nums[-1], "", 1)

                description = re.sub(r"\s+", " ", desc).strip()

                transactions.append({
                    "transaction_date": date,
                    "description": description,
                    "amount": amount,
                    "balance": balance
                })

    # Convert into DataFrame
    HDFC_df = pd.DataFrame(transactions)

    # Split into withdrawal and deposit
    withdrawal, deposit = [], []
    for i in range(len(HDFC_df)):
        if i == 0:
            if "CRV" in HDFC_df.loc[i, "description"].upper() or "CREDIT" in HDFC_df.loc[i, "description"].upper():
                withdrawal.append(0.0)
                deposit.append(HDFC_df.loc[i, "amount"])
            else:
                withdrawal.append(HDFC_df.loc[i, "amount"])
                deposit.append(0.0)
        else:
            prev_balance = HDFC_df.loc[i - 1, "balance"]
            curr_balance = HDFC_df.loc[i, "balance"]
            amt = HDFC_df.loc[i, "amount"]

            if curr_balance > prev_balance:
                withdrawal.append(0.0)
                deposit.append(amt)
            elif curr_balance < prev_balance:
                withdrawal.append(amt)
                deposit.append(0.0)
            else:
                withdrawal.append(amt)
                deposit.append(amt)

    HDFC_df["withdrawal_amount"] = withdrawal
    HDFC_df["deposit_amount"] = deposit

    HDFC_df = HDFC_df[["transaction_date", "description", "withdrawal_amount", "deposit_amount", "balance"]]
    
    cleaned = []

    for row in HDFC_df['description'].astype(str):
        # collapse spaces
        text = re.sub(r"\s+", " ", row).strip()

        # find reference number (>=7 digits)
        ref = re.search(r"\b\d{7,}\b", text)
        ref_no = ref.group(0) if ref else "000000000000000"

        # find date dd/mm/yy
        date = re.search(r"\b\d{2}/\d{2}/\d{2}\b", text)
        date = date.group(0) if date else ""

        # find all amounts like 12,345.67
        amounts = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", text)

        # keep last 1 or 2 numeric amounts (amount + balance)
        amt_part = " ".join(amounts[-2:]) if amounts else ""

        # remove extracted parts from description
        desc = text
        for part in [ref_no, date] + amounts[-2:]:
            desc = desc.replace(part, "")
        desc = re.sub(r"\s+", " ", desc).strip()

        # rebuild normalized row
        final = " ".join([desc, ref_no, date, amt_part]).strip()
        cleaned.append(final)
        
    HDFC_df['description'] = cleaned
    pattern = r"\d{7,}\s+\d{2}/\d{2}/\d{2}.*$"
    HDFC_df['description'] = HDFC_df['description'].astype(str).str.replace(pattern, "", regex=True).str.strip()
    
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, output_excel)
    HDFC_df.to_csv(out_file, index=False)
    print(f"[INFO] Transactions saved -> {out_file}")

    return HDFC_df
