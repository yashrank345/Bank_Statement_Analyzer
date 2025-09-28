import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# Timeline plot
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_timeline(df, out_path="data/output/timeline.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df["transaction_date"], df["withdrawal_amount"], label="Withdrawals", color="red", marker="o")
    plt.plot(df["transaction_date"], df["deposit_amount"], label="Deposits", color="green", marker="o")

    plt.xlabel("Date")
    plt.ylabel("Amount (INR)")
    plt.title("Withdrawals vs Deposits Timeline")
    plt.legend()
    plt.grid(True)

   
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%Y"))
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)  
    plt.close()

    return os.path.abspath(out_path)



# PDF Report
def create_pdf_report(name, email, flagged, chart_path, out_path="data/output/Summary_Report.pdf"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc = SimpleDocTemplate(out_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("<b>Bank Statement Analysis Report</b>", styles["Heading1"]))
    story.append(Spacer(1, 12))

    # Author details
    story.append(Paragraph(f"Name: {name}", styles["BodyText"]))
    story.append(Paragraph(f"Email: {email}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    # Methodology
    story.append(Paragraph("<b>Methodology</b>", styles["Heading2"]))
    methodology_text = """
    1. Extracted PDF data using pdfplumber and regex, handling differences in Statement layouts.<br/>
    2. Standardized account details and transactions into structured CSV files.<br/>
    3. Implemented rule-based checks for large withdrawals (DD > RS.10,000), large deposits (RTGS > RS.50,000),
       and entity-specific transactions (Guddu, Prabhat, Arif, Coal India).<br/>
    4. Built a timeline visualization of withdrawals vs deposits.<br/>
    5. Generated this automated summary report.
    """
    story.append(Paragraph(methodology_text, styles["BodyText"]))
    story.append(Spacer(1, 12))

    # Challenges
    story.append(Paragraph("<b>Challenges Faced</b>", styles["Heading2"]))
    challenges_text = """
    - Variability between bank formats .<br/>
    - Multi-line and messy narration fields.<br/>
    - Currency/amount formatting issues with commas and CR/DR.<br/>
    - Ensuring balance consistency while parsing.<br/>
    """
    story.append(Paragraph(challenges_text, styles["BodyText"]))
    story.append(Spacer(1, 12))

    # Flagged Transactions
    story.append(Paragraph("<b>Flagged Transactions Summary</b>", styles["Heading2"]))
    for key, flagged_df in flagged.items():
        story.append(Paragraph(f"{key}: {len(flagged_df)} transactions", styles["BodyText"]))
        story.append(Spacer(1, 6))

    # Visualization
    story.append(Paragraph("<b>Visualization</b>", styles["Heading2"]))
    if chart_path and os.path.exists(chart_path):
        story.append(Spacer(1, 12))
        story.append(Image(chart_path, width=400, height=250))
    else:
        story.append(Paragraph("Timeline chart not available.", styles["BodyText"]))

    
    

    doc.build(story)
    return os.path.abspath(out_path)
