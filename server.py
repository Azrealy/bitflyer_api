import tornado.ioloop
import tornado.web
from tornado.escape import json_decode, json_encode

class ExampleHandler(tornado.web.RequestHandler):

    def post(self):
        print(json_decode(self.request.body))
        response = {'id' : '12345'}
        self.write(response)

application = tornado.web.Application([
    (r"/exampleHandler", ExampleHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()