# -*- coding: utf-8 -*-
# @Time : 2022/5/30 14:42
# @Author : sanliy
# @File : get_weather
# @software: PyCharm
import requests

from base.c_audio import CAudio
from base.c_json import CJson
from base.record_log import recordLog


class get_weather:
    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.log = recordLog()

    def get_weather(self, city):
        self.log.info("正在获取{0}的天气信息...".format(city))
        response = requests.get(url=self.url, params={
            "appid": self.user,
            "appsecret": self.passwd,
            "city": city,
            "unescape": 1
        })
        if response.status_code == 200:
            self.log.info("{0}天气信息获取成功!".format(city))
            return response.text
        self.log.error("{0}天气获取失败！响应状态为{1}, 响应信息{2}".format(city, response.status_code, response.text))
        return None


if __name__ == '__main__':
    gw = get_weather(
        "https://v0.yiketianqi.com/free/week",
        "99562963",
        "qo7DXwM4"
    )
    city_weather = gw.get_weather("北京")
    print(city_weather)
    cj = CJson()
    cj.load(city_weather)
    city = cj.json_path("city")
    print(city)
    data_list = cj.json_path("data")
    for data in data_list[0]:
        print(data)
