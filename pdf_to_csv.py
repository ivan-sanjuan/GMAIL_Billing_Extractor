from pdf_pass import pdf_pass
import pytesseract
from PIL import Image
import re
import io
import fitz
import os

folder_path = '\\Projects\GMAIL_Billing_Extractor\pdf_files'
pdf_password = pdf_pass()
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

for page in os.listdir(folder_path):
    file = os.path.join(folder_path,page)
    doc = fitz.open(file)
    doc.authenticate(pdf_password)
    page3 = doc.load_page(4)
    zoom = 3
    mat = fitz.Matrix(zoom, zoom)
    pix = page3.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes()))
    text = pytesseract.image_to_string(img)
    pattern = r'^[A-Z][a-z]+\s+\d{1,2}'
    list_result = re.split('\n',text)
    for item in list_result:
        if re.findall(pattern,item):
            print(item)