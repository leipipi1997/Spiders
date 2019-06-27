from boss.DB import DBPool


def query_data(city, input_salary, work_year, education):
    pool = DBPool.MySqlPool()
    result = list()
    # print("Enter successfully!")
    if work_year == "经验不限" and education == "学历不限":
        sql = "select * from boss_spider_result " \
              "where city = '" + city +"'"
    elif work_year == "经验不限" and education != "学历不限":
        sql = "select * from boss_spider_result " \
              "where city = '" + city + "' AND education = '" + education + "'"
    elif work_year != "经验不限" and education == "学历不限":
        sql = "select * from boss_spider_result " \
              "where city = '" + city + "' AND workYear = '" + work_year + "'"
    else:
        sql = "select * from boss_spider_result " \
              "where city = '"+city+"' AND workYear = '"+work_year+"' AND education = '"+education+"'"

    query_result = pool.query_(sql)

    if len(query_result) != 0:
        for i in query_result:
            salary = list(i)
            del salary[0]
            salary = salary[2]
            salary = salary.split("-")
            salary[0] = salary[0].replace("K", "000")
            salary[1] = salary[1].replace("K", "000")  # 之前没有格式化薪水数据
            salary[0] = salary[0].replace("k", "000")
            salary[1] = salary[1].replace("k", "000")
            if salary[1].find("薪") != -1:
                ex_salary = salary[1].split("·")
                salary[1] = ex_salary[0]
                salary.append(ex_salary[1].replace("薪", ""))
            salary[1] = salary[1].replace("k", "000")
            low_salary = int(salary[0])
            high_salary = int(salary[1])

            if input_salary == "50K+":
                judge_salary = input_salary.replace("K", "000")
                judge_salary = judge_salary.replace("+", "")
                judge_salary = int(judge_salary)

                if judge_salary <= low_salary or judge_salary <= high_salary:
                    final_data = list(i)
                    del final_data[0]
                    result.append(final_data)
            else:
                judge_salary = input_salary.split("-")
                judge_salary[0] = judge_salary[0].replace("K", "000")
                judge_salary[1] = judge_salary[1].replace("K", "000")
                judge_low_salary = int(judge_salary[0])
                judge_high_salary = int(judge_salary[1])

                if judge_low_salary <= low_salary <= judge_high_salary \
                        or judge_low_salary <= high_salary <= judge_high_salary:
                    final_data = list(i)
                    del final_data[0]
                    result.append(final_data)

    if len(query_result) == 0 or len(result) == 0:
        result_none = "No such a job!"
        result.append(result_none)

    return result


if __name__ == '__main__':
    query_data("北京", "0-3K", "3-5年", "本科")
