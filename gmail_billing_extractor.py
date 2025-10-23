import requests
from _access_token import get_access_token
from _subject import get_subject
from urllib.parse import urljoin
import fitz
import pprint
import base64

token = get_access_token()
headers = {"Authorization":f"Bearer {token}"}
subject = get_subject()
params = {"q":f"subject:{subject}"}
url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/'
response = requests.get(url,headers=headers,params=params)
data = response.json()
messages = data.get('messages')

for p in messages:
    message_id = p.get('id')
    subjects = urljoin(url,message_id)
    email_response = requests.get(subjects,headers=headers)
    payload = email_response.json()['payload']['parts']
    for data in payload:
        payload_header = data['headers']
        for file in payload_header:
            if file.get('name') == 'Content-Disposition' and file.get('value').startswith('attachment;'):
                attachment_id = data['body'].get('attachmentId')
                filename = data['filename']
                end_point = f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/attachments/{attachment_id}'
                attachment_response = requests.get(
                    end_point,headers=headers
                )
                attachment_data = attachment_response.json()['data']
                decoded_bytes = base64.urlsafe_b64decode(attachment_data)

                with open(f'pdf_files/{filename}', 'wb') as f:
                    f.write(decoded_bytes)