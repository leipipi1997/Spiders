from boss.DB.dataBase import *
import pymysql

connect = getConnect()
cursor = getCursor(connect)

sql = "select pid, salary from boss_spider_result"
cursor.execute(sql)
result = cursor.fetchall()

resultList = list()
for i in result:
    a = list(i)
    resultList.append(a)
    returnList = list()

for i in resultList:
    salary =  i[1]
    salary = salary.split("-")
    if salary[0].find('K') != -1 :
        salary[0] = salary[0].replace("K", "k")
        salary = salary[0] +"-"+ salary[1]
        i[1] = salary
        returnList.append(i)

count = 1
for i in returnList:
    sql = "UPDATE boss_spider_result SET salary = '"+ i[1] +"' WHERE pid = '"+ i[0] +"'"
    cursor.execute(sql)
    connect.commit()
    print(count)
    count += 1

print(len(returnList))

connect.close()