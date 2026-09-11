# Data Analyst Assessment — README / Methodology


https://docs.google.com/spreadsheets/d/1SEhyJmbS8igyYIQkLb7x3cauMvPlRY8z/edit?usp=sharing&ouid=116896028053749145608&rtpof=true&sd=true

**Name:** Somya Gupta
**Assessment:** Data Analyst Assessment Test (VirtuBox)

## What's in this folder

| File | What it is |
|---|---|
| `BizAssessment.xlsx` | One Google Sheet with all worksheets: Data, Q1, Q2, Processed Data, Q3, Q4, Q5, Q6, Q7, Q10 |
| `airline_satisfaction_analysis.py` | Python script (Pandas/NumPy/Matplotlib) used to clean the data and run the analysis |
| `Airline_Satisfaction_Presentation.pptx` | 7-slide presentation for management |
| `raw_combined.csv` | Full raw dataset (129,880 rows) — train.csv + test.csv combined |
| `processed_data.csv` | Full cleaned, analysis-ready dataset (129,880 rows) |
| `chart1_class.png`, `chart2_class_travel.png`, `chart3_correlation.png`, etc. | Charts used in the analysis, dashboard, and presentation |

## Dataset

**Airline Passenger Satisfaction Dataset** from Kaggle
https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction

129,880 rows, 24 columns. It came as two files (train.csv and test.csv) with the same structure, so I combined them into one dataset before cleaning.

## Why a sample is shown in the Google Sheet tabs

The "Data" and "Processed Data" tabs in `BizAssessment.xlsx` show the first 5,000 rows only, because Google Sheets gets slow and hard to review with 129,880 rows sitting inside a single tab. The **full** dataset (raw and processed, all 129,880 rows) is included as separate CSV files (`raw_combined.csv`, `processed_data.csv`) in this same folder so nothing is left out — I just didn't want to force the reviewer to scroll through 130k rows in a spreadsheet tab.

## Methodology (short version)

1. **Combine** — merged train.csv and test.csv, dropped the extra index column.
2. **Clean** — removed duplicates (found none), filled 393 missing "Arrival Delay" values with the median, fixed data types, standardized text (e.g. "disloyal Customer" → "Disloyal Customer").
3. **Transform** — added calculated fields: Total Delay, Delay Bucket, Age Group, Average Service Rating, Satisfied Flag (1/0).
4. **Analyze** — grouped satisfaction rate by class, travel type, age group, customer type, and delay length; checked correlation between each of the 14 service ratings and satisfaction.
5. **Report** — picked the 5 clearest business insights, one surprising result, 3 data-quality/limitation notes, and 3 prioritized recommendations. Full detail for each is in the matching worksheet tab (Q4, Q5, Q6, Q7).

## Google Sheets / Looker Studio note

Since this was built and tested locally in Python/Excel first, to finish the submission properly:
1. Upload `BizAssessment.xlsx` to Google Drive and open it with Google Sheets (File → Open with → Google Sheets) — this turns it into the required Google Sheet with all worksheets.
2. Import `processed_data.csv` into Google Looker Studio (or link the Processed Data sheet) to build the dashboard for Q8, using the charts in this folder as a starting reference for what to include (KPI summary, class comparison, service rating breakdown, delay trend, filters for Class/Type of Travel).

## Tools used

Python (Pandas, NumPy, Matplotlib) in Google Colab for cleaning and analysis. Google Sheets for the worksheet-based answers. Google Looker Studio for the dashboard. AI assistance details are in the Q10 worksheet.
