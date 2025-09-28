import pandas as pd
import re


# find flag on DD withdrawals above 10,000
def flag_dd_large_withdrawals(df):
    """DD withdrawals above 10,000"""
    return df[
        df['description'].str.contains("DD", case=False, na=False)
        & (df['withdrawal_amount'] > 10000)
    ]
    
# find flag on RTGS deposits above 50,000
def flag_rtgs_large_deposits(df):
    """RTGS deposits above 50,000"""
    return df[
        df['description'].str.contains("RTGS", case=False, na=False)
        & (df['deposit_amount'] > 50000)
    ]

# find flag on Entities: Guddu, Prabhat, Arif, Coal India
def flag_specific_entities(df):
    """Entities: Guddu, Prabhat, Arif, Coal India"""
    entities = ["Guddu", "Prabhat", "Arif", "Coal India"]
    pattern = "|".join(entities)
    return df[df['description'].str.contains(pattern, case=False, na=False)]

# final table 
def analyze_transactions(df):
    """Return dict of flagged transactions"""
    flagged = {
        "DD Large Withdrawals": flag_dd_large_withdrawals(df),
        "RTGS Large Deposits": flag_rtgs_large_deposits(df),
        "Specific Entities": flag_specific_entities(df),
    }
    return flagged
