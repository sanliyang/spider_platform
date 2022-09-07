# -*- coding: utf-8 -*-
# @Time : 2022/6/9 14:13
# @Author : sanliy
# @File : c_sqlalchemy
# @software: PyCharm
import psycopg2
from urllib.parse import quote_plus as urlquote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.record_log import recordLog


class cSqlAlchemy:

    def __init__(self):
        self.logger = recordLog()
        cg = CGetConfig(CResource.config_path)

        self.postgresql_host = cg.get_value(CResource.Name_Postgresql, CResource.Name_Host)
        self.postgresql_database = cg.get_value(CResource.Name_Postgresql, CResource.Name_DB_Name)
        self.postgresql_port = cg.get_value(CResource.Name_Postgresql, CResource.Name_Port)
        self.postgresql_user = cg.get_value(CResource.Name_Postgresql, CResource.Name_Name)
        self.postgresql_password = cg.get_value(CResource.Name_Postgresql, CResource.Name_Password)
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.postgresql_user}:{urlquote(self.postgresql_password)}@{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_database}")
        self.cursor = None
        self.session = None

    def create_session(self):
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()

    def close_session(self):
        self.session.close()

    def fetchall(self, sql, *args, **kwargs):
        """
        返回所有记录
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            self.create_session()
            self.cursor = self.session.execute(sql, *args, **kwargs)
            return self.cursor.fetchall()
        except Exception as error:
            self.logger.error("数据库执行fetchall出现错误，具体原因是[{0}]".format(error))
        finally:
            self.close_session()

    def fetchone(self, sql, *args, **kwargs):
        """
        返回一条记录
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        return self.fetchall(sql, *args, **kwargs)[0]

    def one_value(self, sql, *args, **kwargs):
        """
        返回记录中的一个值
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        return self.fetchall(sql, *args, **kwargs)[0][0]

    def execute(self, sql, *args, **kwargs):
        """
        这里执行 除查询以外的所有的sql
        :param sql:
        :param args:
        :param kwargs:
        :return: boolean
        """
        try:
            self.session.execute(sql, *args, **kwargs)
            self.session.commit()
            return True
        except Exception as error:
            self.logger.error("数据库执行execute出现错误，具体原因是[{0}]".format(error))
            return False
        finally:
            self.close_session()


if __name__ == '__main__':
    cs = cSqlAlchemy()
    cs.create_session()
    x = cs.fetchall(
        '''
        select * from ac_order where issubmit= :issubmit
        ''',
        {
            "issubmit": "0"
        }
    )
    print("aaaa{0}".format(x))
