
# AI-Assisted Campaign Experimentation Analyzer

## Overview

This Streamlit application automates campaign A/B testing analysis.

The app:

- Uploads campaign CSV data
- Calculates funnel metrics
- Performs statistical significance testing
- Compares Test vs Control
- Calculates Lift %
- Identifies winning creatives
- Generates experiment insights

---

# Required Columns

Your CSV file should contain:

| Column |
|---|
| send_d |
| send_week |
| Channel |
| emailname |
| tc_flag |
| app_create_date |
| FICO_Band |
| segment |
| sub_segment |
| snd |
| opn |
| unsub |
| clk |
| app |
| offer |
| listings |
| Issued |
| listing_amount |
| Issued_amount |

---

# Metrics Calculated

| Metric | Formula |
|---|---|
| Open Rate | opn/snd |
| Click Rate | clk/snd |
| Unsub Rate | unsub/snd |
| App Rate | app/clk |
| Response Rate | app/snd |
| Offer Rate | offer/app |
| Take Rate | listings/offer |
| $LPM | listing_amount/snd |
| ALS | listing_amount/listings |
| #LPM | listings/snd |

---

# Statistical Testing

- Two-Proportion Z-Test
- 90% Confidence Level

---

# Installation

## Install Required Libraries

```bash
pip install streamlit pandas numpy scipy statsmodels openpyxl
```

---

# Run Application

Open terminal in project folder.

Run:

```bash
streamlit run app.py
```

---

# Example Folder Structure

```bash
AI_AB_TEST/
│
├── app.py
├── Email_Campaign_Data_Sample_v2.csv
└── README.md
```

---

# Output Features

The application provides:

- Raw Uploaded Data
- Calculated Funnel Metrics
- Lift %
- Statistical Significance
- Winning Metrics
- Downloadable Results

---

# Future GPT Integration

Future versions can integrate ChatGPT APIs for:

- Subject line recommendations
- Audience size recommendations
- Automated experiment summaries
- Predictive campaign insights
- Stakeholder readouts

---

# Author

Suyash Kashyap
