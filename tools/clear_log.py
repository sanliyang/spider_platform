# #!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time :2021/8/24 11:10 上午
# @Author : liby
# @File: clear_log.py
# @Software : PyCharm
from tools.c_file import CFile
from tools.c_resource import CResource
from tools.c_time import CTime
from tools.record_log import recordLog


class clearLog:

    def __init__(self):
        self.log = recordLog()

    def clear_log_for_week(self):
        """
        清除一周前的log日志
        :return:
        """
        self.log.info("当前程序运行的时间是{0}".format(CTime.get_now_time()))
        # 一周前的日期为: a_week_date
        clear_date = CTime.get_before_day_time(int(CResource.log_clear_time), CResource.log_clear_time_type)
        # 拼接出一周前的日志名称, 然后判断该文件在logs文件夹下是否存在, 如果存在就删除, 如果不存在就继续监控
        all_name = f"{str(clear_date)}.log"
        # 获取日志的全路径
        all_name_with_path = CFile.path_join(CResource.project_logs_root_path, all_name)
        self.log.info("正在检查[{0}]是否有日志产生， 如果有就清除....".format(clear_date))
        # 判断七天前是否有日志存在, 如果有就删除
        if CFile.path_is_exist(all_name_with_path):
            self.log.info("检查到[{0}]有日志产生， 正在删除日志...".format(clear_date))
            CFile.rm_file(all_name_with_path)
        else:
            self.log.info("检查到[{0}]没有日志产生....".format(clear_date))


if __name__ == '__main__':
    cl = clearLog()
    cl.clear_log_for_week()
