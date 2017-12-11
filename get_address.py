import requests
import json
from sys import argv
import time
import hmac
import hashlib


def get_address(location, key, secret):
    method = "GET"
    body = ""
    access_timestamp = str(time.time())
    api_secret = str.encode(secret)
    text = str.encode(access_timestamp + method + location + body)
    access_sign = hmac.new(api_secret,
                          text,
                          hashlib.sha256).hexdigest()
    auth_header = {
        "ACCESS-KEY": key,
        "ACCESS-TIMESTAMP": access_timestamp,
        "ACCESS-SIGN": access_sign,
        "Content-Type": "application/json"
    }
    with requests.Session() as s:
        s.headers.update(auth_header)
        endpoint = 'https://api.bitflyer.jp' + location
        response = s.get(endpoint)
        json_data = json.loads(response.text)
    print(json_data)

if __name__ == "__main__":
    print(argv[1])
    print(argv[2])
    print(argv[3])
    get_address(argv[1], argv[2], argv[3])    