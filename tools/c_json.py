# -*- coding: utf-8 -*-
# @Time : 2022/5/30 15:17
# @Author : sanliy
# @File : c_json
# @software: PyCharm
import json

import orjson
import jmespath

from tools.c_file import CFile


class CJson:
    def __init__(self):
        self.json_obj = None

    def load(self, mark: any):
        if type(mark) == dict:
            json_str = json.dumps(mark)
        if type(mark) == str:
            if CFile.path_is_exist(mark):
                with open(mark, 'rb') as f:
                    json_str = f.read()
            else:
                json_str = mark
        self.json_obj = orjson.loads(json_str)

    def json_path(self, expr):
        value_list = jmespath.search(expr, self.json_obj)
        if not value_list:
            return None
        return value_list

    def json_path_one(self, expr):
        value = jmespath.search(expr, self.json_obj)
        if not value:
            return None
        if type(value) == str:
            return value
        if type(value) == list:
            return value[0]


if __name__ == '__main__':
    cj = CJson()
    cj.load(
        '''
            {"foo": {"bar": [{"name": "one"}, {"name": "two"}]}}
        ''')
    x = cj.json_path('foo.bar[*].name')
    print(x)

    y = cj.json_path_one('foo.bar[*].name')
    print(y)
