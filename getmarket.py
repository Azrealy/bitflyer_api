import tornado.httpclient
import json
from tornado.escape import json_decode, json_encode
from tornado import gen
import tornado.options

@tornado.gen.coroutine
def json_fetch(http_client):
    response = yield http_client.fetch("http://api.bitflyer.jp/v1/getmarkets", method = 'GET')
    raise gen.Return(response)

@tornado.gen.coroutine
def request():
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_response = yield json_fetch(http_client)
    print(http_responsse.body)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.ioloop.IOLoop.instance().run_sync(request)