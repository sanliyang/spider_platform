# -*- coding: utf-8 -*-
# @Time : 2022/5/13 17:54
# @Author : sanliy
# @File : CFile
# @software: PyCharm
import os


class CFile:

    @classmethod
    def path_join(cls, one_path, *other_path):
        return os.path.join(one_path, *other_path)

    @classmethod
    def get_file_main_name(cls, path_with_name):
        name_with_ext = os.path.basename(path_with_name)
        main_name = name_with_ext.split('.')[0]
        return main_name

    @classmethod
    def path_is_exist(cls, path):
        return os.path.exists(path)

    @classmethod
    def get_file_size(cls, path):
        size_byte = os.path.getsize(path)
        if int(size_byte) < int(1024 * 1024):
            return size_byte / float(1024), 'KB'
        else:
            return size_byte / float(1024 * 1024), 'MB'

    @classmethod
    def get_file_add_time(cls, file_name_with_path):
        return os.path.getctime(file_name_with_path)

    @classmethod
    def mk_dir(cls, path):
        if not cls.path_is_exist(path):
            os.mkdir(path)

    @classmethod
    def rm_file(cls, path):
        if cls.path_is_exist(path):
            os.remove(path)


if __name__ == '__main__':
    size, unit = CFile.get_file_size(
        r'C:\Users\sanliy\OneDrive\文档\WXWork\1688851255855661\Cache\File\2022-04\compress_MS'
        r'&PAN.zip')
    print(size, unit)

    print(CFile.get_file_add_time(r'D:\mini_tools\logs\2022-05-12-all.log'))
