# PDF Invoice Extractor

Extracts the invoice number and total amount from PDF invoices and saves the results to a single CSV file.

## Limitation
The regex patterns used to find the invoice number and total are matched to one specific invoice template. Real-world use with different invoice formats would require adjusting these patterns.

## Requirements

pip install pdfplumber


## How to run

python invoice_extractor.py
