import os, json, time, tornado.ioloop, tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPRequest, HTTPError
from bitflyerAPI import bitflyerApi

http_client = AsyncHTTPClient()

@gen.coroutine
def loop():
    param = {
            "product_code": "FX_BTC_JPY",
            "child_order_type": "LIMIT",
            "side": "BUY",
            "price": 1800000,
            "size": 0.1,
            "minute_to_expire": 100000,
            "time_in_force": "GTC"
        }
    data = json.dumps(param)
    api = bitflyerApi(key="", secret="")
    head = api.auth_header("/v1/me/sendchildorder","POST",data)
    request = HTTPRequest("https://api.bitflyer.jp/v1/me/sendchildorder", 'POST', head, body=data)
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def research():
    request = HTTPRequest("https://api.bitflyer.jp/v1/ticker?product_code=FX_BTC_JPY", "GET")
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def ready():
    while True:
        response = yield research()
        research_json = json.loads(response.body)
        price_one_second_before = research_json["ltp"]
        #response = yield loop()
        yield gen.sleep(1)
        response = yield research()
        research_json = json.loads(response.body)
        price_one_second_after = research_json["ltp"]
        
        print((price_one_second_before-price_one_second_after)*100000/price_one_second_before)
        if price > 2220001:
            response = yield loop()
            print(response.body)
            break
if __name__ == "__main__":
    aap = tornado.ioloop.IOLoop.current()
    tornado.ioloop.IOLoop.instance().run_sync(ready)