# -*- coding: utf-8 -*-
# @Time : 2022/6/8 23:23
# @Author : sanliy
# @File : get_phone_location
# @software: PyCharm
from phone import Phone

from tools.c_json import CJson


class get_phone_locaion:

    def __init__(self, phone):
        self.phone = phone
        self.phone_tools = Phone()
        self.phone_msg = None
        self.cj = CJson()

    def get_phone_json_msg(self):
        self.phone_msg = self.phone_tools.find(self.phone)
        self.cj.load(self.phone_msg)
        return self.phone_msg

    def get_phone_province(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("province")

    def get_phone_city(self):
        self.get_phone_json_msg()
        return self.cj.json_path_one("city") if self.phone_msg is not None else None

    def get_phone_zip_code(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("zip_code")

    def get_phone_area_code(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("area_code")

    def get_phone_type(self):
        self.get_phone_json_msg()
        return None if self.phone_msg is None else self.cj.json_path_one("phone_type")


if __name__ == '__main__':
    gpl = get_phone_locaion("13509874850")
    phone_location = gpl.get_phone_json_msg()
    print(phone_location)

    print(gpl.get_phone_province())
    print(gpl.get_phone_city())
    print(gpl.get_phone_zip_code())
    print(gpl.get_phone_area_code())
    print(gpl.get_phone_type())

