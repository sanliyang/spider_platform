# -*- coding: utf-8 -*-
# @Time : 2022/5/17 15:01
# @Author : sanliy
# @File : c_resource
# @software: PyCharm
import os
import sys

from tools.c_file import CFile
from tools.c_get_config import CGetConfig


class CResource:

    # 有关logs和项目路径的信息获取
    Name_Base = "base"
    Name_Logs = "logs"
    project_root_path = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    project_base_root_path = CFile.path_join(project_root_path, Name_Base)
    config_path = CFile.path_join(project_root_path, 'cnf', 'config.ini')
    private_path = CFile.path_join(project_root_path, 'cnf', 'private.txt')
    public_path = CFile.path_join(project_root_path, 'cnf', 'public.txt')
    config_dir = CFile.path_join(project_root_path, 'cnf')
    project_logs_root_path = CFile.path_join(project_root_path, Name_Logs)

    cg = CGetConfig(config_path)
    init_pic_dir = cg.get_value('tools_init', 'init_pic_dir')
    init_pic_name = cg.get_value('tools_init', 'init_pic_name')
    init_pic_path = CFile.path_join(project_root_path, init_pic_dir, init_pic_name)
    init_show_type = cg.get_value('tools_init', 'init_show_type')
    init_foregroundColor = cg.get_value('tools_init', 'init_foregroundColor')
    init_backgroundColor = cg.get_value('tools_init', 'init_backgroundColor')

    # 日志清除时间配置
    log_clear_time_type = cg.get_value('logs_clear_time', 'log_time_type')
    log_clear_time = cg.get_value('logs_clear_time', 'log_time')

    # schduler 配置
    net_type = cg.get_value('scheduler_cnf', 'net_type')
    cpu_type = cg.get_value('scheduler_cnf', 'cpu_type')

    net_interval_time = cg.get_value('scheduler_cnf', 'net_interval_time')
    cpu_interval_time = cg.get_value('scheduler_cnf', 'cpu_interval_time')
    auto_submit_type = cg.get_value('scheduler_cnf', 'auto_submit_type')

    auto_subumit_interval_time = cg.get_value('scheduler_cnf', 'auto_subumit_interval_time')

    Name_Postgresql = "tools_postgresql"

    Name_Host = "host"
    Name_Name = "name"
    Name_Password = "password"
    Name_Port = "port"
    Name_DB_Name = "db_name"


if __name__ == '__main__':
    print(CResource.project_root_path)
    print(CResource.project_base_root_path)
    print(CResource.config_path)
    print(CResource.project_logs_root_path)
