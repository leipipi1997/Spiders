from boss.DB import DBPool

pool = DBPool.MySqlPool()

sql = "SELECT * from boss_spider_result"

result = pool.query_(sql)
return_list = list()

for i in result:
    row = list(i)
    salary = row[3]
    if salary.find("天") != -1:
        return_list.append(row)

print(return_list)
