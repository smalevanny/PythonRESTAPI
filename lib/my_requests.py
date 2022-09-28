import requests
from lib.logger import Logger

class MyRequests():

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, params, headers, cookies, "GET")

    @staticmethod
    def post(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        url = f"https://playground.learnqa.ru/api{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        match method:
            case "GET":
                response = requests.get(url, params=data, headers=headers, cookies=cookies)
            case "POST":
                response = requests.post(url, data=data, headers=headers, cookies=cookies)
            case "DELETE":
                response = requests.delete(url, data=data, headers=headers, cookies=cookies)
            case "PUT":
                response = requests.put(url, data=data, headers=headers, cookies=cookies)
            case _:
                raise Exception(f"Bad HTTP method '{method}' has been received")

        Logger.add_response(response)

        return response

