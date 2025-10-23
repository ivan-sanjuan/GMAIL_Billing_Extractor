from pdf_pass import pdf_pass
import fitz
import os

folder_path = '\\Projects\GMAIL_Billing_Extractor\pdf_files'
pdf_password = pdf_pass()
for file_name in os.listdir(folder_path):
    file = os.path.join(folder_path,file_name)

    doc = fitz.open(file)
    doc.authenticate(pdf_password)
    page = doc.load_page(3)            
    text = page.get_text('ocr')
    # if not text.strip():
    #     text = page.get_text('ocr')
    print(text)