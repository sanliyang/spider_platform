# #!/usr/bin/python3
# -*- coding:utf-8 -*-
# @time :2021/8/23 7:18 下午
# @Author : liby
# @File: record_log.py
# @Software : PyCharm
import logging
import colorlog

from logging.handlers import RotatingFileHandler
from tools.c_file import CFile
from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.c_time import CTime


config_obj = CGetConfig(CResource.config_path)

log_path = CFile.path_join(CResource.project_root_path, config_obj.get_value('tools_log', 'log.dir.relative.path'))

CFile.mk_dir(path=log_path)  # 若不存在logs文件夹，则自动创建

log_colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'cyan',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    # 终端输出格式
    'color_format': '%(log_color)s%(asctime)s - %(name)s - %(filename)s - [line:%(lineno)d] - [%(funcName)s]- %('
                    'levelname)s - [日志信息]: %(message)s',
    # 日志输出格式
    'log_format': '%(asctime)s - %(name)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - [%(funcName)s] - ['
                    '日志信息]: %(message)s '
}


class recordLog:
    """
    先创建日志记录器（logging.getLogger），然后再设置日志级别（logger.setLevel），
    接着再创建日志文件，也就是日志保存的地方（logging.FileHandler），然后再设置日志格式（logging.Formatter），
    最后再将日志处理程序记录到记录器（addHandler）
    """

    def __init__(self):
        self.__now_time = CTime.get_date()  # 当前日期格式化
        self.__all_log_path = CFile.path_join(log_path, f"{str(self.__now_time)}.log")
        self.__logger = logging.getLogger()  # 创建日志记录器
        self.__logger.setLevel(logging.DEBUG)  # 设置默认日志记录器记录级别

    @staticmethod
    def __init_logger_handler(log_all_path):
        """
        创建日志记录器handler，用于收集日志
        :param log_all_path: 日志文件路径
        :return: 日志记录器
        """
        return RotatingFileHandler(filename=log_all_path, maxBytes=30 * 1024 * 1024, backupCount=3, encoding='utf-8')

    @staticmethod
    def __init_console_handle():
        """创建终端日志记录器handler，用于输出到控制台"""
        return colorlog.StreamHandler()

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        """
        设置handler级别并添加到logger收集器
        :param logger_handler: 日志记录器
        :param level: 日志记录器级别
        """
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    def __set_color_handle(self, console_handle):
        """
        设置handler级别并添加到终端logger收集器
        :param console_handle: 终端日志记录器
        """
        console_handle.setLevel(logging.DEBUG)
        self.__logger.addHandler(console_handle)

    @staticmethod
    def __set_color_formatter(console_handle, color_config):
        """
        设置输出格式-控制台
        :param console_handle: 终端日志记录器
        :param color_config: 控制台打印颜色配置信息
        :return:
        """
        formatter = colorlog.ColoredFormatter(default_formats["color_format"], log_colors=color_config)
        console_handle.setFormatter(formatter)

    @staticmethod
    def __set_log_formatter(file_handler):
        """
        设置日志输出格式-日志文件
        :param file_handler: 日志记录器
        """
        formatter = logging.Formatter(default_formats["log_format"], datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        """
        关闭handler
        :param file_handler: 日志记录器
        """
        file_handler.close()

    def __console(self, level, message, *args, **kwargs):
        """构造日志收集器"""
        all_logger_handler = self.__init_logger_handler(self.__all_log_path)  # 创建日志文件
        console_handle = self.__init_console_handle()

        self.__set_log_formatter(all_logger_handler)  # 设置日志格式
        self.__set_color_formatter(console_handle, log_colors_config)

        self.__set_log_handler(all_logger_handler)  # 设置handler级别并添加到logger收集器
        self.__set_color_handle(console_handle)

        if level == 'info':
            self.__logger.info(message, *args, **kwargs)
        elif level == 'debug':
            self.__logger.debug(message, *args, **kwargs)
        elif level == 'warning':
            self.__logger.warning(message, *args, **kwargs)
        elif level == 'error':
            self.__logger.error(message, *args, **kwargs)
        elif level == 'critical':
            self.__logger.critical(message, *args, **kwargs)

        self.__logger.removeHandler(all_logger_handler)  # 避免日志输出重复问题
        self.__logger.removeHandler(console_handle)

        self.__close_handler(all_logger_handler)  # 关闭handler

    def debug(self, message, *args, **kwargs):
        # 这里使用堆栈信息进行回溯，找到调用
        kwargs['stacklevel'] = 3
        self.__console('debug', message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        kwargs['stacklevel'] = 3
        self.__console('info', message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        kwargs['stacklevel'] = 3
        self.__console('warning', message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        kwargs['stacklevel'] = 3
        self.__console('error', message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        kwargs['stacklevel'] = 3
        self.__console('critical', message, *args, **kwargs)


if __name__ == '__main__':
    log = recordLog()
    log.info("这是日志信息")
    log.debug("这是debug信息")
    log.warning("这是警告信息")
    log.error("这是错误日志信息")
    log.critical("这是严重级别信息")
