import re
import pdfplumber as pf
import pandas as pd
import os

def account_ICIC_info(pdf_path, output_dir="data/output"):
    with pf.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages[:1]:
            text = page.extract_text() or ""
            full_text += text + "\n"

    # ACCOUNT NUMBER
    account_number = None
    match_acc = re.search(r"Savings\s+([0-9]{9,18})", full_text, re.IGNORECASE)
    if match_acc:
        account_number = match_acc.group(1)

    # HOLDER NAME
    holder = None
    match_holder = re.search(r"Your Details With Us:\s*\n?(.+)", full_text)
    if match_holder:
        holder = match_holder.group(1).strip()

    # RAW ADDRESS (block between holder and 'Your Base Branch')
    raw_address = ""
    match_address = re.search(
        r"Your Details With Us:.*?\n(.+?)Your Base Branch:",
        full_text,
        re.DOTALL | re.IGNORECASE
    )
    if match_address:
        raw_address = match_address.group(1).strip()
        # Remove holder name if it's at the start of raw address
        if holder and raw_address.startswith(holder):
            raw_address = raw_address[len(holder):].strip()

    # Split into lines
    addr_lines = [line.strip() for line in raw_address.splitlines() if line.strip()]

    street, city, state, pincode = "", "", "", ""

    if addr_lines:
        # Last line usually contains "STATE - COUNTRY - PINCODE"
        last_line = addr_lines[-1]
        state_pin_match = re.search(r"([A-Za-z]+)\s*-\s*India\s*-\s*([0-9]{6})", last_line, re.IGNORECASE)
        if state_pin_match:
            state = state_pin_match.group(1).title()
            pincode = state_pin_match.group(2)

        # City is typically the second-last line
        if len(addr_lines) >= 2:
            city = addr_lines[-2].title()

        # Street = everything except last 2 lines
        if len(addr_lines) > 2:
            street = " ".join(addr_lines[:-2])

    # Build single address (clean)
    address_parts = [street, city, state, pincode]
    address = ", ".join([part for part in address_parts if part])

    # IFSC
    ifsc = None
    match_ifsc = re.search(r"\b([A-Z]{4}0[A-Z0-9]{6})\b", full_text, re.IGNORECASE)
    if match_ifsc:
        ifsc = match_ifsc.group(1).upper()

    # MICR
    micr = None
    match_micr = re.search(r"\b([0-9]{9})\b", full_text)
    if match_micr:
        micr = match_micr.group(1)

    # ACCOUNT TYPE
    account_type = "Savings" if "Savings" in full_text else "Current"

    # BANK NAME
    bank_codes = {
        "ICIC": "ICICI Bank",
        "HDFC": "HDFC Bank",
        "SBIN": "State Bank of India",
        "AXIS": "Axis Bank",
        "PNB": "Punjab National Bank",
    }
    bank_name = ""
    if ifsc:
        prefix = ifsc[:4]
        bank_name = bank_codes.get(prefix, "")

    ICIC_info = {
        "account_number": account_number or "",
        "account_holder_name": holder or "",
        "account_type": account_type,
        "ifsc": ifsc or "",
        "micr": micr or "",
        "bank_name": bank_name or "",
        "address": address
    }

    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame([ICIC_info])
    out_file = os.path.join(output_dir, "account_info.csv")
    df.to_csv(out_file, index=False)
    print(f"[INFO] Account information extracted -> {out_file}")

    return ICIC_info
