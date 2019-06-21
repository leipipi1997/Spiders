from boss.DB import dataBase

def queryData(city, inputSalary, workYear, education):
    connect = dataBase.getConnect()
    cursor = dataBase.getCursor(connect)
    result = list()
    # print("Enter successfully!")
    if workYear == "经验不限" and education == "学历不限" :
        sql = "select * from boss_spider_result " \
              "where city = '" + city +"'"
    elif workYear == "经验不限" and education != "学历不限" :
        sql = "select * from boss_spider_result " \
              "where city = '" + city + "' AND education = '" + education + "'"
    elif workYear != "经验不限" and education == "学历不限" :
        sql = "select * from boss_spider_result " \
              "where city = '" + city + "' AND workYear = '" + workYear + "'"
    else:
        sql = "select * from boss_spider_result " \
              "where city = '"+city+"' AND workYear = '"+workYear+"' AND education = '"+education+"'"

    cursor.execute(sql)
    queryResult = cursor.fetchall()
    connect.close()
    if len(queryResult) != 0:
        for i in queryResult:
            salary = list(i)
            del salary[0]
            salary = salary[2]
            salary = salary.split("-")
            salary[0] = salary[0].replace("K", "000")
            salary[1] = salary[1].replace("K", "000")  # 之前没有格式化薪水数据
            salary[0] = salary[0].replace("k", "000")
            salary[1] = salary[1].replace("k", "000")
            if salary[1].find("薪") != -1:
                exSalary = salary[1].split("·")
                salary[1] = exSalary[0]
                salary.append(exSalary[1].replace("薪", ""))
            salary[1] = salary[1].replace("k", "000")
            lowSalary = int(salary[0])
            highSalary = int(salary[1])

            if inputSalary == "50K+" :

                judgSalary = inputSalary.replace("K", "000")
                judgSalary = judgSalary.replace("+", "")
                judgSalary = int(judgSalary)

                if judgSalary <= lowSalary or judgSalary <= highSalary:
                    finalData = list(i)
                    del finalData[0]
                    result.append(finalData)
            else:
                judgSalary = inputSalary.split("-")
                judgSalary[0] = judgSalary[0].replace("K", "000")
                judgSalary[1] = judgSalary[1].replace("K", "000")
                judgLowSalary = int(judgSalary[0])
                judgHighSalary = int(judgSalary[1])
                # print(judgLowSalary <= lowSalary <= judgHighSalary, judgLowSalary <= highSalary <= judgHighSalary)

                if judgLowSalary <= lowSalary <= judgHighSalary or judgLowSalary <= highSalary <= judgHighSalary:
                    finalData = list(i)
                    del finalData[0]
                    result.append(finalData)
                    # print(finalData)
    elif len(queryResult) == 0:
        resultNone = "No such a job!"
        result.append(resultNone)

    # print(result)
    return result

if __name__ == '__main__':
    queryData("北京", "0-3K", "经验不限", "学历不限")