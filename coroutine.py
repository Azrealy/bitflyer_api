import os, json, time, tornado.ioloop, tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPRequest, HTTPError
from bitflyerAPI import bitflyerApi
from tornado.escape import json_decode, json_encode
import urllib

http_client = AsyncHTTPClient()
api = bitflyerApi()

@gen.coroutine
def make_order(prices):
    request = api.send_order(product_code = "FX_BTC_JPY", price = prices, size = 0.1)
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def research():
    request = api.get_board(product_code = "FX_BTC_JPY")
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def ready():
    while True:
        response = yield research()
        board = json.loads(response.body)
        print("The mid price is " + str(board["mid_price"]))
        list_bids = board["bids"]
        list_asks = board["asks"]
        sum_bids = 0
        sum_asks = 0
        list_size_bids = []
        list_size_asks = []
        for bids in list_bids[:100]:
            #sum_bids += bids["size"]*bids["price"]
            list_size_bids.append(bids["size"])
        for asks in list_asks[:100]:
            list_size_asks.append(asks["size"])

        print("the max size of bids" + str(list_bids[list_size_bids.index(max(list_size_bids))]))
        print("the max size of asks" + str(list_asks[list_size_asks.index(max(list_size_asks))]))

        max_size_of_price = list_bids[list_size_bids.index(max(list_size_bids))]
        if max_size_of_price["size"] >= 100:
            response_make_order = yield make_order(max_size_of_price["price"])
            if response_make_order.body:
                print(json.loads(response_make_order.body))
                break 
        yield gen.sleep(120)

@gen.coroutine
def chats():
    request = api.get_chats(from_date= "2017-12-16T17:16:37.483")
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def search_chats():
    response = yield chats()
    response_json = json.loads(response.body)
    for s in response_json:
        if s["nickname"] == "G-DRAGON":
            print(s["message"])

@gen.coroutine
def balance():
    request = api.get_balance()
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def get_balance():
    response = yield balance()
    print(json.loads(response.body))

@gen.coroutine
def collateral():
    request = api.get_collateral()
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def get_collateral():
    response = yield collateral()
    print(json.loads(response.body))

@gen.coroutine
def parentorder():
    request = api.send_parentorder()
    response = yield http_client.fetch(request)
    raise gen.Return(response)

@gen.coroutine
def send_parentorder():
    response = yield parentorder()
    print(json.loads(response.body))    

if __name__ == "__main__":
    aap = tornado.ioloop.IOLoop.current()
    tornado.ioloop.IOLoop.instance().run_sync(ready)