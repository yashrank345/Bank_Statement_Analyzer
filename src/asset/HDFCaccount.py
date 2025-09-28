import re
import pdfplumber as pf
import pandas as pd

def account_HDFC_info(pdf_path):
    with pf.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages[:1]:  
            full_text += page.extract_text() + "\n"

    # Regex helper
    def isValid_Bank_Acc_Number(acc_str):
        """Check if account number is 9–18 digits."""
        regex = r"^[0-9]{9,18}$"
        return bool(re.match(regex, acc_str))

    #  Extract holder name + address block 
    holder, customer_address = "", ""
    match_block = re.search(r"(MR|MRS|MS)\s+[A-Z ]+([\s\S]*?)(?=AccountNo)", full_text, re.IGNORECASE)
    if match_block:
        lines = match_block.group(0).split("\n")

        # Holder = first line
        holder = lines[0].title().strip()

        # Address cleaning        
        addr_lines = []
        for line in lines[1:]:
            clean_line = line.strip()
            if not clean_line:
                continue
            # Remove unwanted labels but keep the left part (the address text)
            clean_line = re.sub(r"State\s*:.*", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"Phoneno.*", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"ODLimit.*", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"Email.*", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"CustID.*", "", clean_line, flags=re.IGNORECASE)
            clean_line = re.sub(r"Currency.*", "", clean_line, flags=re.IGNORECASE)
            if clean_line:
                addr_lines.append(clean_line)

        # Join clean lines into one address string
        address = " ".join(addr_lines)

    # Extract account number 
    account_number = ""
    match_acc = re.search(r"AccountNo\s*[:\-]?\s*(\d+)", full_text, re.IGNORECASE)
    if match_acc:
        acc = match_acc.group(1)
        if isValid_Bank_Acc_Number(acc):
            account_number = acc

    #  Extract IFSC 
    ifsc = ""
    match_ifsc = re.search(r"IFSC[:\-]?\s*([A-Z0-9]+)", full_text)
    if match_ifsc:
        ifsc = match_ifsc.group(1)

    #  Extract MICR 
    micr = ""
    match_micr = re.search(r"MICR[:\-]?\s*(\d+)", full_text)
    if match_micr:
        micr = match_micr.group(1)

    #  Detect Bank Name 
    bank_name = ""
    if ifsc:
        bank_codes = {
            "HDFC": "HDFC Bank",
            "ICIC": "ICICI Bank",
            "SBIN": "State Bank of India",
            "AXIS": "Axis Bank",
            "PNB": "Punjab National Bank"
        }
        bank_name = bank_codes.get(ifsc[:4].upper(), "")

    #  Build dictionary 
    HDFC_info = {
        "account_number": account_number,
        "account_holder_name": holder,
        "account_type": "Savings",
        "ifsc": ifsc,
        "micr": micr,
        "bank_name": bank_name,
        "address": address,
    }

    # Save to CSV
    df = pd.DataFrame([HDFC_info])
    df.to_csv("data/output/account_info.csv", index=False)
    print("[INFO] Account information extracted -> data/output/account_info.csv")

    return HDFC_info
