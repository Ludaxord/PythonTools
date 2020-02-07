#!/usr/bin/env python3
import json

from utils.arg_class import ArgClass
from web.curl_call import CurlCall
from utils.parser import Parser, StoreDictKeyPair


class FirebaseMessagingCall(ArgClass):

    def __load_config(self):
        with open(f'{self.get_current_dir_path()}/config.json') as json_file:
            data = json.load(json_file)
            return data

    def __get_server_key(self):
        data = self.__load_config()
        return data["server_key"]

    def __args(self):
        return Parser(
            args=[{"command": "--to", "type": str,
                   "help": "Firebase device token"},
                  {"command": "--data", "action": StoreDictKeyPair,
                   "help": "key value pair of data in notification, add keys like: title, body, url"},
                  {"command": "--headers", "action": StoreDictKeyPair,
                   "help": "headers send with request to firebase, this value is optional"},
                  {"command": "--title", "type": str,
                   "help": "title of notification"},
                  {"command": "--body", "type": str,
                   "help": "body of notification"},
                  {"command": "--url", "type": str,
                   "help": "url to open send with notification"}
                  ]).get_args()

    def __get_headers(self, arguments):
        server_key = self.__get_server_key()
        header = arguments.headers
        if header is None:
            header = {
                'Authorization': f'key={server_key}',
                'Content-Type': 'application/json'
            }
        return header

    def __get_notification(self, arguments):
        notification = {}
        title = arguments.title
        body = arguments.body
        notification["title"] = title
        notification["body"] = body
        return notification

    def __get_data(self, arguments):
        data = {}
        title = arguments.title
        body = arguments.body
        url = arguments.url
        data["title"] = title
        data["body"] = body
        data["url"] = url
        return data

    def get_args(self):
        arguments = self.__args()
        payload = {}
        headers = self.__get_headers(arguments)
        to = arguments.to
        data = arguments.data
        url = arguments.url
        payload["to"] = to
        if data is not None:
            payload["data"] = data
        if data is None and url is None:
            notification = self.__get_notification(arguments)
            payload["notification"] = notification
        elif data is None and url is not None:
            data = self.__get_data(arguments)
            payload["data"] = data
        return headers, payload


firebase = FirebaseMessagingCall()

headers, payload = firebase.get_args()

print(f"headers => {headers}")
print(f"payload => {payload}")

URL = 'https://fcm.googleapis.com/fcm/send'

curl = CurlCall()

req = curl.curl_call(URL, payload, headers)
