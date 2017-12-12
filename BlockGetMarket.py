import requests
import json
from sys import argv
from datetime import datetime

def get_markets(location):
    endpoint = 'http://api.bitflyer.jp/v1/' + location
    response = requests.get(endpoint)
    json_data = json.loads(response.text)
    print(json_data)

if __name__ == "__main__":
    time_before_exec = datetime.now()
    print(argv[1])
    get_markets(argv[1])
    time_after_exec = datetime.now()
    print(time_after_exec - time_before_exec)
    