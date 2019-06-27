# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from boss.DB import DBPool

pool = DBPool.MySqlPool()


class PidPipeline(object):
    def __init__(self):
        self.pid = set()
        sql = "select pid from boss_spider_result"
        result = pool.query_(sql)
        self.result = list()
        for i in result:
            self.result.append(i[0])

    def process_item(self, item, spider):
        pid = item['pid']
        for i in self.result:
            if pid == i:
                raise DropItem("The position already exists!")
        else:
            self.pid.add(pid)

        return item


class PositionPipeline(object):
    def __init__(self):
        self.position_name = set()

    def process_item(self, item, spider):
        position_name = item['positionName']
        if position_name.find("大数据") == -1:
            raise DropItem("The position name doesn't include big data for words!")
        elif position_name.find("大数据"):
            self.position_name.add(position_name)
        return item


class CityPipeline(object):
    def process_item(self, item, spider):           # 城市格式化
        item['city'] = item['city'].split()[0]

        return item


class SalaryPipeline(object):
    def process_item(self, item, spider):           # 薪水格式化
        salary = item['salary']
        # print(item['salary'])
        salary = salary.split("-")
        if salary[0].find('K') != -1:
            salary[0] = salary[0].replace("K", "k")
        elif salary[0].find('K') == -1:
            salary[0] = salary[0] + "k"
        elif salary[1].find('K') != -1:
            salary[1] = salary[1].replace("K", "k")
        salary = salary[0] + "-" + salary[1]
        item['salary'] = salary
        return item


class BossPipeline(object):
    def process_item(self, item, spider):
        sql = "insert into boss_spider_result( pid, positionName, workYear, salary, city ,education, " \
              "companyShortName, industryField, financeStage, companySize, updated_at) " \
                  "value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (item['pid'], item['positionName'], item['workYear'], item['salary'], item['city'], item['education'],
                item['companyShortName'], item['industryField'], item['financeStage'], item['companySize'],
                item['updated_at'])
        pool.insert_(sql, data)
        # 提交sql语句
        pool.end()

        return item
        # 纯属python操作mysql知识，不熟悉请恶补


if __name__ == '__main__':
    PidPipeline()
