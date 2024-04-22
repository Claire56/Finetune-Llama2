
import os
import json
import re
from PyPDF2 import PdfReader

def list_pdf_files(folder_path):
    """
    List all PDF files in the specified folder.
    """
    return [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

def extract_text_from_pdf(pdf_file_path):
    """
    Extract text from a PDF file.
    """
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()
    return extracted_text

def extract_information(text, patterns):
    """
    Extract relevant information from the extracted text using provided patterns.
    """
    extracted_info = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_info[key] = match.group(1)
        else:
            extracted_info[key] = "No match found"

    return extracted_info

def create_questions_answers(extracted_text, extracted_info):
    """
    Create questions and answers based on extracted information.
    """
    name = extracted_info.get("name", "No match found")
    account_number = extracted_info.get("account_number", "No match found")
    statement_date = extracted_info.get("statement_date", "No match found")
    due_date = extracted_info.get("due_date", "No match found")
    amount_due = extracted_info.get("amount_due", "No match found")
    insurance_pay = extracted_info.get("insurance_pay", "No match found")
    total_charges = extracted_info.get("total_charges", "No match found")
    date_of_service = extracted_info.get("date_of_service", "No match found")

    questions_answers = [
        {
            "instruction": f"What is {name}'s account number?",
            "context": extracted_text,
            "response": f"{account_number}"
        },
        {
            "instruction": f"What is {name}'s statement date?",
            "context": extracted_text,
            "response": f"{statement_date}"
        },
        {
            "instruction": f"What is {name}'s due date?",
            "context": extracted_text,
            "response": f"{due_date}"
        },
        {
            "instruction": f"When was {name}'s statement created?",
            "context": extracted_text,
            "response": f"{statement_date}"
        },
        {
            "instruction": f"When is {name}'s balance due supposed to be fully paid?",
            "context": extracted_text,
            "response": f"{due_date}"
        },
        {
            "instruction": f"How much does {name} owe?",
            "context": extracted_text,
            "response": f"{amount_due}"
        },
        {
            "instruction": f"How much money is {name} expected to pay by {due_date}?",
            "context": extracted_text,
            "response": f"{amount_due}"
        },
        {
            "instruction": f"How much were {name}'s total charges?",
            "context": extracted_text,
            "response": f"{total_charges}"
        },
        {
            "instruction": f"How much money did {name}'s insurance pay?",
            "context": extracted_text,
            "response": f"{insurance_pay}"
        },
        {
            "instruction": f"When did {name} receive services?",
            "context": extracted_text,
            "response": f"{date_of_service}"
        }
    ]
    return questions_answers

def main(pdfs_folder_path, patterns):
    # Define regex patterns for information extraction
    # Process PDF files
    for pdf_file in list_pdf_files(pdfs_folder_path):
        pdf_file_path = os.path.join(pdfs_folder_path, pdf_file)
        extracted_text = extract_text_from_pdf(pdf_file_path)
        extracted_info = extract_information(extracted_text, patterns)
        questions_answers = create_questions_answers(extracted_text, extracted_info)

        with open('questions_answers.jsonl', 'a') as file:
            for qa in questions_answers:
                file.write(json.dumps(qa) + '\n')

        print("JSONL file created successfully.")

patterns1 = {
        "name": r"Patient Name: (\w+), (\w+)",
        "account_number": r"Account Number:\s*(\d+)",
        "statement_date": r"Statement Date:\s+(\d{1,2}/\d{1,2}/\d{4})",
        "due_date": r"Due Date:\s*(\d{2}/\d{2}/\d{4})",
        "amount_due": r"Amount Due:\s+(\$\d+\.\d+)",
        "insurance_pay": r"Total Insurance Pay/Adj: \$(-?\d+\.\d{2})",
        "total_charges": r"Total Charges:\s*\$([\d,]+(\.\d{2})?)",
        "date_of_service": r"Date of Service:\s*(\d{2}/\d{2}/\d{4})"
    }

if __name__ == "__main__":
    main('pdfs', patterns1)
    main('pdfs/engle', patterns1)
