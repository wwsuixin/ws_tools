'''
Author: wwsuixin
Date: 2022-02-08 14:47:33
LastEditors: wwsuixin
LastEditTime: 2022-02-08 15:07:01
Description: file content
'''
import sqlite3


class sqlliteDBtool:
    def __init__(self,db_filepath):
        """
        初始化函数,创建数据库连接
        """
        self.conn = sqlite3.connect(db_filepath)
        self.conn.row_factory = self.dict_factory
        self.cursor = self.conn.cursor()

    @staticmethod
    def dict_factory(cursor, row):
        """
        对sqlite的查询结果转化成python的词典
        :param cursor: 游标
        :param row: 结果集
        :return: 返回词典
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def executeUpdate(self, sql, param):
        """
        数据库的插入、修改函数
        :param sql: 传入的sql语句
        :param param: 传入的参数
        :return: 返回操作数据库状态
        """
        try:
            self.cursor.executemany(sql, param)
            i = self.conn.total_changes
        except Exception as e:
            print("错误类型:", e)
            return e
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return e

    def excuteDelete(self, sql, param):
        """
        操作数据库删除
        :param sql: sql语句
        :param param: 参数
        :return: 返回数据库状态
        """
        try:
            self.cursor.execute(sql, param)
            i = self.conn.total_changes
        except Exception as e:
            print("错误类型:", e)
            return e
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

    def excuteQuery(self, sql, param):
        """
        数据库数据查询
        :param sql: 传入的SQL语句
        :param param: 传入数据
        :return: 返回操作数据库状态
        """
        test = self.cursor.execute(sql, param)
        return test.fetchall()

    def close(self):
        """
        关闭数据库的连接
        :return:
        """
        self.cursor.close()
        self.conn.close()
