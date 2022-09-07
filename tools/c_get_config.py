# -*- coding: utf-8 -*-
# @Time : 2022/5/16 22:59
# @Author : sanliy
# @File : c_get_config
# @software: PyCharm
import configparser

class CGetConfig:

    def __init__(self, config_path):
        self.config_obj = configparser.RawConfigParser()
        self.config_obj.read(config_path, encoding="utf-8")

    def get_all_sections(self):
        return self.config_obj.sections()

    def get_options(self, section):
        return self.config_obj.options(section)

    def get_items(self, section):
        return self.config_obj.items(section)

    def get_value(self, section, option):
        return self.config_obj.get(section, option)


if __name__ == '__main__':
    cg = CGetConfig(CResource.config_path)
    print(cg.get_all_sections())
    print(cg.get_options('tools_log'))
    print(cg.get_items('tools_log'))
    print(cg.get_value('tools_log', 'log.dir.relative.path'))
