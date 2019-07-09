# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# class BossItemLoader(ItemLoader):
#     #定义一个默认的全局默认输出处理器，TakeFirst取出数组中第一个，相当于extract_fitst()
#     default_output_processor = TakeFirst()


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    pid = scrapy.Field()                # 职位的ID
    positionName = scrapy.Field()       # 职位的名称
    workYear = scrapy.Field()           # 职位的工作经历要求
    salary = scrapy.Field()             # 职位薪水
    city = scrapy.Field()               # 职位工作的城市
    education = scrapy.Field()          # 职位的学历要求
    companyShortName = scrapy.Field()   # 招聘公司简称
    industryField = scrapy.Field()      # 具体的应用行业
    financeStage = scrapy.Field()       # 融资规模
    companySize = scrapy.Field()        # 公司规模
    updated_at = scrapy.Field()         # 职位的更新时间（设置为爬取当日）
    detail_content = scrapy.Field()     # 职位的详情页中的职位描述信息
