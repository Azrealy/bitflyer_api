import requests
import json
from sys import argv
def get_markets(location):
    endpoint = 'http://api.bitflyer.jp/v1/' + location
    response = requests.get(endpoint)
    json_data = json.loads(response.text)
    print(json_data)

if __name__ == "__main__":
    print(argv[1])
    get_markets(argv[1])
    