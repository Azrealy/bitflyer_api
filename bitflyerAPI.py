from tornado.httpclient import HTTPRequest
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
    """
    This class can create tornado.client HTTPRequest of user 
    to use the Bitflyer API, which website you can access follow
    https://lightning.bitflyer.jp/docs/playground

    IF you want use the private request, you should initalize the
    key and secret of you account.
    Example:
    bitflyerApi(key=[YOU KEY], secret=[YOU SECRET])
    And you can use this object to take others method to make you 
    HTTPRequst.
    """

    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret
    
    def auth_header(self, request_path, method = "GET", request_body=""):
        """
        This function create the PRIVATE Header for specify user

        Parameter
        -------------
        path , method , body
        
        Return
        -------------
        a authetication of the user Header.
        """
        Auth = Authentication(self.secret, request_path, method, request_body)
        return {
        "ACCESS-KEY": self.key,
        "ACCESS-TIMESTAMP": Auth.access_timestamp,
        "ACCESS-SIGN": Auth.signature(),
        "Content-Type": "application/json"
        }

    def request(self, request_path, method = "GET", param=None):
        """
        THis method can use to create HTTPRequest, which is
        base on you need.

        Parameter:
        --------------
        path, method, param

        Return:
        --------------
        HTTPRequest 
        """
        api_url = "https://api.bitflyer.jp"
        body = ""
        header = None

        if method == "POST":
            body = json.dumps(param)
            print(body)
        else:
            if param:
                body += "?" + urllib.parse.urlencode(param)

        if self.key and self.secret:
            header = self.auth_header(request_path, method, body)

        if method == "GET":
            endpiont = api_url + request_path + body
            return HTTPRequest(endpiont, method = method, headers = header)
        else:
            endpiont = api_url + request_path
            return HTTPRequest(endpiont, method = method, headers = header, 
                               body = body)

    def get_markets(self):
        """
        GET Public HTTPRequest
        show the exchange markets product_code

        Return
        --------------
        HTTPRequest of tornado.httpclient 
        """
        request_path = "/v1/getmarkets"
        return self.request(request_path)

    def get_ticker(self, **param):
        """
        GET Public HTTPRequest
        get the ticker of exchange

        Parameter:
        -------------
        product_code: FX_BTC_JPY

        Return
        --------------
        HTTPRequest of tornado.httpclient
        """
        request_path = "/v1/getticker"
        return self.request(request_path, param = param)

    def get_chats(self, **param):
        """
        GET Public HTTPRequest
        get the a list of message of chat log

        Parameter:
        --------------
        from_date: 2016-02-15

        Return
        --------------
        HTTPRequest of tornado.httpclient
        """
        request_path = "/v1/getchats"
        return self.request(request_path, param = param)

    def get_balance(self, **param):
        """
        GET Public HTTPRequest
        get a list of balances sheet of user

        Parameter:
        --------------
        from_date: 2016-02-15

        Return
        --------------
        HTTPRequest of tornado.httpclient
        """        
        request_path = "/v1/me/getbalance"
        return self.request(request_path, param = param)

    def get_collateral(self, **param):
        """
        GET Public HTTPRequest
        get a list of user collateral statue

        Parameter:
        --------------
        param

        Return
        --------------
        HTTPRequest of tornado.httpclient
        """        
        request_path = "/v1/me/getcollateral"
        return self.request(request_path, param = param)

    def send_order(self, product_code, price, size, minute_to_expire=100000, 
                   child_order_type="LIMIT", side="BUY", time_in_force="GTC"):
        """
        POST a child order based on your parameter.

        Parameter:
        ---------------
        "product_code": product_code,
        "child_order_type": child_order_type,
        "side": side, 
        "price": price, (default)
        "size": size, (default)
        "minute_to_expire": minute_to_expire, (default)
        "time_in_force": time_in_force (default)

        Return:
        ---------------
        HTTPRequest of tornado.httpclient 
        """
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
        """
        GET Private HTTPRequest 

        Parameter:
        -------------
        product_code: "BTC_JPY"
        count: 100
        before: 0
        after: 0
        child_order_state: "ACTIVE"
        child_order_id: "JFX20171111-120000-421212"
        child_order_accepta_:"JFX20171111-120000-421212"
        parent_order_id: ""

        Return:
        --------------
        HTTPRequest of tornado.httpclient
        """
        request_path = "/v1/me/getchildorders"
        return self.request(request_path, param = param)

    def get_board(self, **param):
        """
        GET Public HTTPRequest

        Parameter: (option)
        --------------
        product_code: "FX_BTC_JPY"

        Return: HTTPRequest
        --------------
        HTTPRequest of tornado.httpclient
        """
        request_path = "/v1/getboard"
        return self.request(request_path, param = param)

    def send_parentorder(self):
        """
        GET Public HTTPRequest

        Parameter: (option)
        --------------
        product_code: "FX_BTC_JPY"

        Return: HTTPRequest
        --------------
        HTTPRequest of tornado.httpclient
        """
        param = {
        "order_method": "IFDOCO",
        "minute_to_expire": 10000,
        "time_in_force": "GTC",
        "parameters": [{
            "product_code": "FX_BTC_JPY",
            "condition_type": "LIMIT",
            "side": "BUY",
            "price": 2470000,
            "size": 0.1
        },
        {
            "product_code": "FX_BTC_JPY",
            "condition_type": "LIMIT",
            "side": "SELL",
            "price": 2570000,
            "size": 0.1
        },
        {
            "product_code": "FX_BTC_JPY",
            "condition_type": "STOP_LIMIT",
            "side": "SELL",
            "price": 2400000,
            "trigger_price": 2400001,
            "size": 0.1
        }]
        }        
        request_path = "/v1/me/sendparentorder"
        return self.request(request_path,method = "POST", param = param)