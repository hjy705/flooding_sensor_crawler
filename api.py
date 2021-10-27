import requests, json
from datetime import datetime

def request_token():
    payload = 'grant_type=client_credentials'
    headers = {
        'Authorization': 'Basic cG0rRHEzUGxmaEdQUS8xRk9LL1lkbStpT295TE9MRkVqMFZ1aHB6Tng1QT06UnFuL3BQVno1SWFySFJCcTAyY090Q0pFbVFtNVIyVzMrRUUxTFB1cFI3VT0=',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", "https://iot.wra.gov.tw/Oauth2/token", headers=headers, data=payload).json()
    container = {
        "token": response["access_token"],
        "now_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = container["token"]
    with open('token.json','w', encoding = 'utf-8') as outfile:
        json.dump(container , outfile , ensure_ascii=False , indent=4)
    return result

def request_data(token):
    headers = {
        'Authorization': 'Bearer' + ' ' + token,
    }
    response = requests.request(
        "GET", "https://iot.wra.gov.tw/uswg/stations?countyCode=65000", headers=headers).json()
    return response