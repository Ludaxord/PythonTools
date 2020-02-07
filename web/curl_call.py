import requests


class CurlCall:

    def curl_call(self, url, payload, headers, display_result=True):
        r = requests.post(url=url, json=payload, headers=headers)
        if display_result:
            print(r.content)
        return r
