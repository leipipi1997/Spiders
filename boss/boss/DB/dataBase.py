import pymysql


def getConnect():
    # 连接数据库
    connect = pymysql.connect(
        host='193.112.231.132',  # 数据库地址
        port=10029,  # 数据库端口
        db='cloud',  # 数据库名
        user='root',  # 数据库用户名
        passwd='lei52095',  # 数据库密码
        charset='utf8',  # 编码方式
        use_unicode=True)
    # connect.connect()
    return connect

def getCursor(connect):
    cursor = connect.cursor()
    return cursor
