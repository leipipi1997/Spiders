# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem
import time


class BossSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'boss_spider'

    # 设定域名  
    allowed_domains = ['www.zhipin.com']

    # 设置起始页，即入口URL，这里设置的是放在一个数组内，让爬虫每次都爬取这几个城市的数据
    def start_requests(self):
        urls = [
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101010100&industry=&position=',
            # 北京
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101020100&industry=&position=',
            # 上海
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101280100&industry=&position=',
            # 广州
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101280600&industry=&position=',
            # 深圳
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101210100&industry=&position=',
            # 杭州
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101030100&industry=&position=',
            # 天津
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101110100&industry=&position=',
            # 西安
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101190400&industry=&position=',
            # 苏州
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101200100&industry=&position=',
            # 武汉
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101230200&industry=&position=',
            # 厦门
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101250100&industry=&position=',
            # 长沙
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101270100&industry=&position=',
            # 成都
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101180100&industry=&position=',
            # 郑州
            'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101040100&industry=&position=',
            # 重庆

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        boss_item = BossItem()

        # 利用xpath筛选想要爬取的数据
        for box in response.xpath('//div[@class="job-primary"]'):
            boss_item['pid'] = box.xpath('.//a[@data-jobid]/@data-jobid').extract()[0]
            boss_item['positionName'] = box.xpath('.//div[@class="job-title"]/text()').extract()[0]
            boss_item['salary'] = box.xpath('.//span[@class="red"]/text()').extract()[0]
            boss_item['city'] = box.xpath('.//p[1]/text()').extract()[0]
            boss_item['workYear'] = box.xpath('.//p[1]/text()').extract()[1]
            boss_item['education'] = box.xpath('.//p[1]/text()').extract()[2]
            boss_item['companyShortName'] = box.xpath('.//div[@class="info-company"]//a/text()').extract()[0]
            boss_item['industryField'] = box.xpath('.//p[1]//text()').extract()[3]
            if len(box.xpath('.//p[1]/text()').extract()) == 6:
                boss_item['financeStage'] = box.xpath('.//p[1]//text()').extract()[4]
                boss_item['companySize'] = box.xpath('.//p[1]//text()').extract()[5]
            elif len(box.xpath('.//p[1]/text()').extract()) == 5:
                boss_item['financeStage'] = "未知"
                boss_item['companySize'] = box.xpath('.//p[1]//text()').extract()[4]
            boss_item['updated_at'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            time.sleep(30)       # 防止403,所以休息一秒

            # 将Item：boss_item传递给Spider中间件,由它进行数据清洗（去空,去重）等操作
            # 每次yield都将调用SpiderMiddleware
            yield boss_item

            # 分页
        url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()
        if url:
            url = url[0]
            yield scrapy.Request("https://www.zhipin.com" + url, callback=self.parse)
