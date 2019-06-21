from scrapy import cmdline
import datetime
import time


def doSth():
    # 把爬虫程序放在这个类里
    cmdline.execute("scrapy crawl boss_spider".split())

# 一般网站都是1:00点更新数据，所以每天凌晨一点启动
def main():
    while True:
        now = datetime.datetime.now()
        if now.hour % 2 == 0 and now.minute == 0:
            doSth()
        # 每隔60秒检测一次
        print("sleep 60 s")
        time.sleep(60)

doSth()