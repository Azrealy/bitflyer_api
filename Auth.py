import time 
import hmac
import hashlib

class Authentication(object):
    
    def __init__(self, secret, request_path, method, request_body):
        self.secret = secret
        self.method = method
        self.request_path = request_path
        self.request_body = request_body
        self.access_timestamp = str(time.time())
    
    def signature(self):
        api_secret = str.encode(self.secret)
        text = str.encode(self.access_timestamp + self.method + self.request_path + self.request_body)
        return hmac.new(api_secret, text, hashlib.sha256).hexdigest()
