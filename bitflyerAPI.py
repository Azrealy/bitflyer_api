import tornado.httpclient
import json
from tornado.escape import json_decode, json_encode
from tornado import gen
import tornado.options
from datetime import datetime
from Auth import Authentication
import urllib
from sys import argv
import requests

class bitflyerApi(object):
    
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    
    def auth_header(self, request_path, method = "GET", request_body=""):
        Auth = Authentication(self.secret, request_path, method, request_body)
        return {
        "ACCESS-KEY": self.key,
        "ACCESS-TIMESTAMP": Auth.access_timestamp,
        "ACCESS-SIGN": Auth.signature(),
        "Content-Type": "application/json"
        }
    def request(self, request_path, method = "GET", param=None):
        api_url = "https://api.bitflyer.jp"
        #if param:
            #body = json.dumps(param)
            #print(body)
        if method == "GET":
            if param:
                body = "?" + urllib.parse.urlencode(param)
                print(request_path)
                header = self.auth_header(request_path, request_body = body)
            else:
                header = self.auth_header(request_path)
        if method == "POST":
            header = self.auth_header(request_path, method, body)
        with requests.Session() as s:
            s.headers.update(header)
            endpoint = api_url + request_path
            if method == "GET":
                response = s.get(endpoint, params=param)
            else:
                response = s.post(endpoint, data = body)
            content = json.loads(response.content.decode("utf-8"))
        print(content)

    def get_markets(self):
        request_path = "/v1/getmarkets"
        return self.request(request_path)

    def send_order(self, product_code, price, size, minute_to_expire=100000, child_order_type="LIMIT", side="BUY", time_in_force="GTC"):
        param = {
            "product_code": product_code,
            "child_order_type": child_order_type,
            "side": side,
            "price": price,
            "size": size,
            "minute_to_expire": minute_to_expire,
            "time_in_force": time_in_force
        }
        request_path = "/v1/me/sendchildorder"
        return self.request(request_path, method = "POST", param = param)
    def get_order(self, **param):
        print(param)
        request_path = "/v1/me/getchildorders"
        return self.request(request_path, param = param)
"""
@tornado.gen.coroutine
def json_fetch(http_client):
    response = yield http_client.fetch("http://api.bitflyer.jp/v1/getmarkets", method = 'GET')
    raise gen.Return(response)

@tornado.gen.coroutine
def request():
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_response = yield json_fetch(http_client)
    print(http_response.body)
"""
if __name__ == "__main__":
    #tornado.options.parse_command_line()     
    time_before_exec = datetime.now()
    instance = bitflyerApi(argv[1], argv[2])
    instance.get_order(product_code="FX_BTC_JPY", child_order_state="ACTIVE")
    #instance.send_order("FX_BTC_JPY", 2500000, 0.1, side = "SELL")
    #tornado.ioloop.IOLoop.instance().run_sync(request)
    time_after_exec = datetime.now()
    print(time_after_exec - time_before_exec)