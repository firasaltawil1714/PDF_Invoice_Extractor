import csv
import re
from pathlib import Path
import pdfplumber


class InvoiceExtractor:
    def __init__(self, invoices_folder, output_csv):
        self.invoices_folder = invoices_folder
        self.output_csv = output_csv
        self.all_data = []

    def get_pdf_files(self):
        return list(self.invoices_folder.glob("*.pdf"))

    def extract_text(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
        return text

    def parse_invoice_data(self, text, filename):
        parsed_data = {"filename": filename, "invoice_number": None, "total": None}
        invoice_match = re.search(r"Invoice #(\d+)", text)
        if invoice_match:
            parsed_data["invoice_number"] = invoice_match.group(1)
        total_match = re.search(r"Total USD \$([\d.]+)", text)
        if total_match:
            parsed_data["total"] = total_match.group(1)
        return parsed_data

    def process_all(self):
        pdf_files = self.get_pdf_files()
        all_data = []
        for pdf_path in pdf_files:
            text = self.extract_text(pdf_path)
            data = self.parse_invoice_data(text, pdf_path.name)
            all_data.append(data)
        self.all_data = all_data

    def save(self):
        if not self.all_data:
            print("No data to save.")
            return
        fieldnames = self.all_data[0].keys()
        with open(self.output_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.all_data)

    def run(self):
        if not self.invoices_folder.exists():
            print("Invoices folder does not exist.")
            return
        pdf_files = self.get_pdf_files()
        if not pdf_files:
            print("No PDF files found.")
            return
        self.process_all()
        self.save()
        print(f"Saved {len(self.all_data)} record(s) to {self.output_csv.name}")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    extractor = InvoiceExtractor(invoices_folder=script_dir / "invoices", output_csv=script_dir / "extracted_data.csv")
    extractor.run()
