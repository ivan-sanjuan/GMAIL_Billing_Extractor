import fitz
import os

folder_path = '\Projects\GMAIL_Billing_Extractor\pdf_files'

for file_name in os.listdir(folder_path):
    file = os.path.join(folder_path,file_name)

    doc = fitz.open(file)
    page = doc.load_page(3)            
    text = page.get_text()
    print(text)