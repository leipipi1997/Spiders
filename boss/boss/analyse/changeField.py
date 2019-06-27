def change_field(result):
    data_set = list()
    for i in result:
        data_detail = list(i)

        # 删除不需要的数据项，这里注意，每删除一次列表就会更新一次，所以从末尾开始删除比较好
        # del data_detail[10], data_detail[9], data_detail[8], data_detail[7], data_detail[6], data_detail[1], \
        # data_detail[0]
        # 数据处理，经验要求、起薪、城市、学历要转换为相应的字段
        if len(i) > 0:
            if data_detail[0] == "经验不限":
                data_detail[0] = "EX1"
            elif data_detail[0] == "应届生":
                data_detail[0] = "EX2"
            elif data_detail[0] == "1年以内":
                data_detail[0] = "EX3"
            elif data_detail[0] == "1-3年":
                data_detail[0] = "EX4"
            elif data_detail[0] == "3-5年":
                data_detail[0] = "EX5"
            elif data_detail[0] == "5-10年":
                data_detail[0] = "EX6"
            elif data_detail[0] == "10年以上":
                data_detail[0] = "EX7"

            if len(i) > 1:
                salary = data_detail[1].split("-")
                salary[0] = salary[0].replace("K", "000")
                salary[1] = salary[1].replace("K", "000")  # 之前没有格式化薪水数据
                salary[0] = salary[0].replace("k", "000")
                salary[1] = salary[1].replace("k", "000")
                if salary[1].find("薪") != -1:
                    ex_salary = salary[1].split("·")
                    salary[1] = ex_salary[0]
                    salary.append(ex_salary[1].replace("薪", ""))  # 额外的薪水
                low_salary = int(salary[0])
                high_salary = int(salary[1])
                if len(salary) == 3:
                    avg_salary = round((low_salary + high_salary) / 2 * int(salary[2]) / 12, 1)
                else:
                    avg_salary = (low_salary + high_salary) / 2

                if 0 <= avg_salary <= 3000:
                    data_detail[1] = "S1"
                elif 3000 < avg_salary <= 5000:
                    data_detail[1] = "S2"
                elif 5000 < avg_salary <= 10000:
                    data_detail[1] = "S3"
                elif 10000 < avg_salary <= 20000:
                    data_detail[1] = "S4"
                elif 20000 < avg_salary <= 50000:
                    data_detail[1] = "S5"
                elif avg_salary > 50000:
                    data_detail[1] = "S6"
                    # print(avg_salary)

                if len(i) > 2:
                    if data_detail[2] == "北京":
                        data_detail[2] = "C1"
                    elif data_detail[2] == "上海":
                        data_detail[2] = "C2"
                    elif data_detail[2] == "广州":
                        data_detail[2] = "C3"
                    elif data_detail[2] == "深圳":
                        data_detail[2] = "C4"
                    elif data_detail[2] == "杭州":
                        data_detail[2] = "C5"
                    elif data_detail[2] == "天津":
                        data_detail[2] = "C6"
                    elif data_detail[2] == "西安":
                        data_detail[2] = "C7"
                    elif data_detail[2] == "苏州":
                        data_detail[2] = "C8"
                    elif data_detail[2] == "武汉":
                        data_detail[2] = "C9"
                    elif data_detail[2] == "厦门":
                        data_detail[2] = "C10"
                    elif data_detail[2] == "长沙":
                        data_detail[2] = "C11"
                    elif data_detail[2] == "成都":
                        data_detail[2] = "C12"
                    elif data_detail[2] == "郑州":
                        data_detail[2] = "C13"
                    elif data_detail[2] == "重庆":
                        data_detail[2] = "C14"

                    if len(i) >= 4:
                        if data_detail[3] == "学历不限":
                            data_detail[3] = "ED1"
                        elif data_detail[3] == "高中":
                            data_detail[3] = "ED2"
                        elif data_detail[3] == "大专":
                            data_detail[3] = "ED3"
                        elif data_detail[3] == "本科":
                            data_detail[3] = "ED4"
                        elif data_detail[3] == "硕士":
                            data_detail[3] = "ED5"
                        elif data_detail[3] == "博士":
                            data_detail[3] = "ED6"

        data_set.append(data_detail)

    return data_set
