# -*- coding: utf-8 -*-

import requests


class TestAliveIP(object):

    def __init__(self, ip=''):
        self.ip = ip
        with open('alive.txt', 'r') as fp:
            self.AllIP = fp.readlines()
        self.process_request()

    def process_request(self):
        print(len(self.AllIP))
        for i in range(len(self.AllIP)):
            this_ip = self.AllIP[i].strip()
            server = {'https': this_ip}
            response = requests.get('https://www.zhipin.com/c101110100/?query=%E7%88%AC%E8%99%AB%20%E5%AE%9E%E4%B9%A0', proxies=server, timeout=5)
            print(response.content)


if __name__ == "__main__":
    t = TestAliveIP()
