import os, json, time, tornado.ioloop, tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPRequest, HTTPError

http_client = AsyncHTTPClient()

@gen.coroutine
def loop():
    response = yield http_client.fetch("https://api.bitflyer.jp/v1/getmarkets", method = 'GET')
    raise gen.Return(response)

@gen.coroutine
def ready():
    while True:
        reslut = yield loop()
        yield gen.sleep(10)
        print(reslut.body)

if __name__ == "__main__":
    aap = tornado.ioloop.IOLoop.current()
    tornado.ioloop.IOLoop.instance().run_sync(ready)