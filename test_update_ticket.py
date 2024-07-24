import json
import requests

def test_update_ticket():
    api_url = 'http://127.0.0.1:1477/update_ticket'
    id = "ffe4e80c-4a08-11ef-a28a-28d0ea7d6477"
    password = "gwizz"
    json = {'password' : 'gwizz', 'id' : id, 'completed' : False, 'url' : 'https://www.youtube.com/watch?v=Wj1FfilAe2Y&t=20s'}
    r = requests.post(url=api_url, json=json)
    return r

r = test_update_ticket()
print(r.status_code,r.reason,r.text)