# -*- coding: utf-8 -*-

import requests
import re
import threading
from lxml import etree
import time


class TestProxy(object):
    def __init__(self):
        self.sFile = r'proxy.txt'
        self.dFile = r'alive.txt'
        self.URL = 'https://www.zhipin.com'
        self.threads = 10
        self.timeout = 3
        self.regex = re.compile(r'zhipin.com')
        self.aliveList = []

        self.run()

    def run(self):
        with open(self.sFile, 'r') as fp:
            lines = fp.readlines()
            line = lines.pop()
            while lines:
                for i in range(self.threads):
                    time.sleep(15)
                    t = threading.Thread(target=self.link_with_proxy, args=(line,))
                    t.start()
                    if lines:
                        line = lines.pop()
                    else:
                        continue
        with open(self.dFile, 'w') as fp:
            for i in range(len(self.aliveList)):
                fp.write(self.aliveList[i])

    def link_with_proxy(self, line):
        server = {'http': line.strip()}
        try:
            response = requests.get('https://www.zhipin.com/c101110100/?query=%E7%88%AC%E8%99%AB%20%E5%AE%9E%E4%B9%A0',
                                    proxies=server, timeout=2)
        except Exception as e:
            print('%s connect failed' % server)
            return
        else:
            try:
                text = response.text
            except:
                print('%s connect failed!' % server)
                return
            if text.find("404 Not Found") != -1:
                print("%s connect is 404" % server)
            # elif text.find(".error-content") != 1:
            #     print("%s connect is 302" % server)
            else:
                print('%s connect success ......' % server)
                self.aliveList.append(line)


if __name__ == '__main__':
    TP = TestProxy()
