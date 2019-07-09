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
        # sql1 = "select pid from position_detail"
        result = pool.query_(sql)
        # result_detail = pool.query_(sql1)
        self.result = list()
        # self.result_detail = list()
        for i in result:
            self.result.append(i[0])
        # for i in result_detail:
        #     self.result_detail.append(i[0])

    def process_item(self, item, spider):
        pid = item['pid']
        for i in self.result:
            if pid == i:
                raise DropItem("The position already exists!")
        else:
            self.pid.add(pid)
        # for i in self.result_detail:
        #     if pid == i:
        #         raise DropItem("The detail content already exists!")
        return item


class PositionPipeline(object):
    def __init__(self):
        self.position_name = set()

    def process_item(self, item, spider):
        position_name = item['positionName']
        if position_name:
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
        if salary:
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
        # sql1 = "insert into position_detail( pid, detail_content) value (%s, %s)"
        # data1 = (item['pid'], item['detail_content'])
        pool.insert_(sql, data)
        # pool.insert_(sql1, data1)
        # 提交sql语句
        pool.end()
        return item
        # 纯属python操作mysql知识，不熟悉请恶补


if __name__ == '__main__':
    PidPipeline()
