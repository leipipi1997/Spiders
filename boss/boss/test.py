from scrapy import cmdline
import datetime
import time


def do_sth():
    # 把爬虫程序放在这个类里
    cmdline.execute("scrapy crawl boss_spider".split())

# 一般网站都是1:00点更新数据，所以每天凌晨一点启动


def main():
    while True:
        now = datetime.datetime.now()
        if now.hour % 2 == 0 and now.minute == 0:
            do_sth()
        # 每隔60秒检测一次
        # 两小时一次的爬取太频繁了，后期学会如何在封IP后能够识别验证码再采用2小时的
        print("sleep 60 s")
        time.sleep(60)


do_sth()
