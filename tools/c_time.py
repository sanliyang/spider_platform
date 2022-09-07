# -*- coding: utf-8 -*-
# @Time : 2022/5/17 15:42
# @Author : sanliy
# @File : c_time
# @software: PyCharm
import time
import datetime


class CTime:

    @classmethod
    def get_now_timestamp(cls):
        """
        获取当前时间的时间戳
        :return:
        """
        return time.time()

    @classmethod
    def get_before_day_time(cls, days, type):
        """
        获取前几天的时间
        :param days:
        :return:
        """
        if type == "days":
            return datetime.date.today() + datetime.timedelta(days=(-days))
        elif type == "weeks":
            return datetime.date.today() + datetime.timedelta(weeks=(-days))
        else:
            return datetime.date.today()

    @classmethod
    def get_after_day_time(cls, days, type):
        """
        获取后几天的时间
        :param days:
        :return:
        """
        if type == "days":
            return datetime.date.today() + datetime.timedelta(days=days)
        elif type == "weeks":
            return datetime.date.today() + datetime.timedelta(weeks=days)
        else:
            return datetime.date.today()

    @classmethod
    def get_one_time_after_day_time(cls, one_day, days, type):
        """
        获取某一天后几天的时间
        :param days:
        :return:
        """
        if type == "days":
            return one_day + datetime.timedelta(days=days)
        elif type == "weeks":
            return one_day + datetime.timedelta(weeks=days)
        else:
            return one_day

    @classmethod
    def get_one_time_before_day_time(cls, one_day, days, type):
        """
        获取某一天前几天的时间
        :param days:
        :return:
        """
        if type == "days":
            return one_day + datetime.timedelta(days=(-days))
        elif type == "weeks":
            return one_day + datetime.timedelta(weeks=(-days))
        else:
            return one_day

    @classmethod
    def timestamp_2_asctime(cls, timestamp_num):
        """
        将时间戳转换为asctime时间
        :param timestamp_num:
        :return:
        """
        return time.ctime(timestamp_num)

    @classmethod
    def get_localtime(cls):
        """
        获取当地的时间（struct_time）
        :return:
        """
        return time.localtime()

    @classmethod
    def format_timestamp(cls, timestamp_num, delimiter):
        """
        将时间戳转换为 自己想要的格式
        :param timestamp_num:
        :param delimiter:
        :return:
        """
        return time.strftime("%Y{0}%m{0}%d %H:%M:%S".format(delimiter), time.localtime(timestamp_num))

    @classmethod
    def get_year(cls):
        """
        获取当前的年份
        :return:
        """
        return cls.get_date().year

    @classmethod
    def get_month(cls):
        """
        获取当前的月份
        :return:
        """
        return cls.get_date().month

    @classmethod
    def get_day(cls):
        """
        获取当前的天
        :return:
        """
        return cls.get_date().day

    @classmethod
    def get_date(cls):
        """
        获取当前的日期
        :return:
        """
        return datetime.date.today()

    @classmethod
    def format_time(cls, one_time, delimiter):
        """
        格式化时间
        :param one_time:
        :param delimiter:
        :return:
        """
        return one_time.strftime("%Y{0}%m{0}%d %H:%M:%S".format(delimiter))

    @classmethod
    def format_date(cls, one_date, delimiter):
        """
        格式化日期
        :param one_date:
        :param delimiter:
        :return:
        """
        return one_date.strftime("%Y{0}%m{0}%d".format(delimiter))

    @classmethod
    def get_now_time(cls):
        """
        获取当前的时间
        :return:
        """
        return datetime.datetime.now()

    @classmethod
    def sleep(cls, sleep_vs):
        time.sleep(sleep_vs)


if __name__ == '__main__':
    print(CTime.get_now_timestamp())
    print(CTime.timestamp_2_asctime(CTime.get_now_timestamp()))
    print(CTime.get_localtime())
    print(CTime.get_day())
    print(CTime.format_time(CTime.get_now_time(), "/"))
    print(CTime.get_before_day_time(1, type="days"))
    print(CTime.get_now_time())
    print(CTime.get_date())

    print(CTime.format_timestamp(CTime.get_now_timestamp(), "-"))
