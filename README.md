# Data Quality Checker

A simple Python tool that scans a CSV file and reports common data quality issues.

## What it checks
- Missing values per column
- Duplicate rows
- Numeric outliers (IQR method)
- An overall quality score out of 100

## Why I built it
In my work with data governance and SDAIA compliance, data quality was a daily concern.
This project automates the first checks I used to do by hand.

## How to run
```bash
pip install -r requirements.txt
python checker.py sample_data.csv
```

## Example output
```
Rows: 11 | Columns: 5
Duplicate rows: 1
Missing values: city (1), age (1), salary (1)
Outliers: age (1)
Quality score: 83.6/100
```

## Built with
Python, Pandas

## Future ideas
- Export the report to Excel/PDF
- Validate formats (emails, phone numbers, dates)
- Simple web interface
