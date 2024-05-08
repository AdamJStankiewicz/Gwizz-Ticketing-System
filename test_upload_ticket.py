import json
import requests

api_url = 'http://127.0.0.1:1477/upload'
create_row_data = {'desc' : "This is a test description that was set in a python file.", "email" : "test0@gmail.com"}
r = requests.post(url=api_url, json=create_row_data)

create_row_data = {'desc' : "This is a test description that was set in a python file.", "email" : "test1@gmail.com"}
r = requests.post(url=api_url, json=create_row_data)

create_row_data = {'desc' : "This is a test description that was set in a python file.", "email" : "test2@gmail.com"}
r = requests.post(url=api_url, json=create_row_data)

print(r.status_code,r.reason,r.text)