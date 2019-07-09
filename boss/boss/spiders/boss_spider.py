# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem
import time
import random


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
        # 利用xpath筛选想要爬取的数据
        for box in response.xpath('//div[@class="job-primary"]'):
            boss_item = BossItem()
            boss_item['pid'] = box.xpath('.//a[@data-jobid]/@data-jobid').extract()[0]
            # position_detail_url = box.xpath('.//a[@data-jobid]/@href').extract()[0]
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
            # 将Item：boss_item传递给Spider中间件,由它进行数据清洗（去空,去重）等操作
            # 每次yield都将调用SpiderMiddleware
            # position_detail_url = response.urljoin(position_detail_url)
            # yield scrapy.Request(position_detail_url, meta={'boss_item': boss_item},
            #                      callback=self.detail_parse, priority=10)
            yield boss_item
        time.sleep(random.randint(30, 55))

        # 分页
        url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()
        if len(url) != 0 and url[0] != 'javascript:;':
            url = response.urljoin(url[0])
            yield scrapy.Request(url, callback=self.parse)

    def detail_parse(self, response):
        boss_item = response.meta['boss_item']
        boss_item['detail_content'] = response.xpath('string(//div[@class="detail-content"]//div[@class="job-sec"]//'
                                                     'h3[contains(text(),"职位描述")]/../'
                                                     'div[@class="text"])').extract()[0].strip()
        yield boss_item
