import json
import requests

def test_upload_ticket():
    api_url = 'http://127.0.0.1:1477/upload'
    print("To upload a ticket, please enter the following information: ")
    desc = input("Description: ")
    email = input("Email: ")
    
    create_row_data = {'desc' : desc, "email" : email}
    r = requests.post(url=api_url, json=create_row_data)
    return r

r = test_upload_ticket()
print(r.status_code,r.reason,r.text)