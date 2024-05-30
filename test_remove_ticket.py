import json
import requests

def test_remove_ticket():
    api_url = 'http://127.0.0.1:1477/remove_ticket'
    print("To remove a ticket, please enter the following information: ")
    email = input("Email: ")
    password = input("Password: ")
    json = {'email' : email, "password" : password}
    r = requests.post(url=api_url, json=json)
    return r

r = test_remove_ticket()
print(r.status_code,r.reason,r.text)