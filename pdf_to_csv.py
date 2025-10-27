from pdf_pass import pdf_pass
import pytesseract
from PIL import Image
import pandas as pd
from datetime import datetime
import re
import io
import fitz
import os

year = '2025'
base_dir = os.getcwd()
folder_path = os.path.join(base_dir,'pdf_files',f'{year}')
pdf_password = pdf_pass()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
billing_details = []
for page in os.listdir(folder_path):
    file = os.path.join(folder_path,page)
    print(file)
    doc = fitz.open(file)
    doc.authenticate(pdf_password)
    try:
        page = doc.load_page(4)
    except ValueError:
        page = doc.load_page(2)
    zoom = 3
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes()))
    text = pytesseract.image_to_string(img)
    pattern = r'^[A-Z][a-z]+\s+\d{1,2}'
    list_result = re.split('\n',text)
    for item in list_result:
        if re.findall(pattern,item):
            item_pattern = r'^([A-Za-z]+\s\d{1,2})\s+([A-Za-z]+\s\d{1,2})\s+(.*?)\s+(-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)$'
            match = re.match(item_pattern,item)
            if match:
                transaction_date, post_date, description, amount = match.groups()
                transaction_date = datetime.strptime(transaction_date,'%B %d')
                post_date = datetime.strptime(post_date,'%B %d')
                transaction_date = transaction_date.strftime(f'{year}-%m-%d')
                post_date = post_date.strftime(f'{year}-%m-%d')
                billing_details.append(
                    {
                        'Year':year,
                        'Transaction Date':transaction_date,
                        'Post Date':post_date,
                        'Description':description,
                        'Amount':amount
                    }
                )

df = pd.DataFrame(billing_details)
df.to_csv(f'{year}.csv',index=False)
            