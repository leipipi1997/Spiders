import pymysql
import traceback
from DBUtils.PooledDB import PooledDB
from boss import mysql_settings


class MySqlPool(object):

    config = {
        'host': mysql_settings.MYSQL_HOST,
        'port': mysql_settings.MYSQL_PORT,
        'database': mysql_settings.MYSQL_DATABASE,
        'user': mysql_settings.MYSQL_USER,
        'password': mysql_settings.MYSQL_PASSWORD,
        'charset': mysql_settings.MYSQL_CHARSET,
    }
    _pool = None

    def __init__(self):
        self._conn = MySqlPool.get_conn()
        self._cursor = self._conn.cursor()

    @staticmethod
    # 单例模式
    def get_conn():
        if MySqlPool._pool is None:
            global _pool
            _pool = PooledDB(creator=pymysql, mincached=1, maxcached=10, host=MySqlPool.config['host'],
                             port=MySqlPool.config['port'], database=MySqlPool.config['database'],
                             user=MySqlPool.config['user'], password=MySqlPool.config['password'],
                             charset=MySqlPool.config['charset'])
        return _pool.connection()

    def query_(self, sql):
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            return result
        except Exception as e:
            traceback.print_exc(e)

    def insert_(self, sql, data):
        try:
            self._cursor.execute(sql, data)
        except Exception as e:
            traceback.print_exc(e)
            self.end("rollback")

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option='commit'):
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self):
        self._cursor.close()
        self._conn.close()


if __name__ == '__main__':
    MySqlPool()
