# -*- coding: utf-8 -*-
# @Time : 2022/5/30 23:21
# @Author : sanliy
# @File : daily_read_weather
# @software: PyCharm
from tools.c_audio import CAudio
from tools.c_json import CJson
from tools.c_time import CTime
from tools.record_log import recordLog
from model.get_weather import get_weather
from model.windows_msg import windowsNote


class daily_read_weather:

    def __init__(self, url, user, passwd):
        self.url = url
        self.user = user
        self.passwd = passwd
        self.log = recordLog()

    def get_and_read_weather_msg(self, city, read_type):
        gw = get_weather(self.url, self.user, self.passwd)
        city_msg = gw.get_weather(city)
        if city_msg is None:
            self.log.info("{0}天气信息获取失败！".format(city))
            return None
        self.log.info("正在解析{0}的天气情况...".format(city))
        cj = CJson()
        cj.load(city_msg)
        data_list = cj.json_path("data")
        self.log.info(data_list)
        self.log.info(type(data_list))
        for data in data_list:
            self.log.info(data)
            print("====================")
            cj_data = CJson()
            cj_data.load(data)
            city_date = cj_data.json_path_one("date")
            city_weather = cj_data.json_path_one("wea")
            city_tem_day = cj_data.json_path_one("tem_day")
            city_tem_night = cj_data.json_path_one("tem_night")
            city_wind = cj_data.json_path_one("win")
            city_wind_speed = cj_data.json_path_one("win_speed").replace("<", "小于").replace(">", "大于")
            msg = "{0}{1}的天气{2}, 白天温度为{3}, 夜晚温度为{4}, 风向为{5}, 风速为{6}".format(
                city,
                city_date,
                city_weather,
                city_tem_day,
                city_tem_night,
                city_wind,
                city_wind_speed
            )
            self.log.info(msg)
            if read_type == "daily" and city_date == str(CTime.get_date()):
                self.read_weather(msg, city, city_date)
                wn = windowsNote('{0}{1}天气情况'.format(city, city_date), msg, icon_path=None, duration=10)
                wn.send_to_windows()
                break
            if read_type == "next" and city_date == CTime.get_after_day_time(1, "days"):
                self.read_weather(msg, city, city_date)
                break
            if read_type == "week":
                self.read_weather(msg, city, city_date)

    def read_weather(self, msg, city, date):
        self.log.info("正在朗读{0}{1}的天气情况...".format(city, date))
        ca = CAudio()
        ca.change_speed(-40)
        ca.say(msg)


if __name__ == '__main__':
    da = daily_read_weather(
        "https://v0.yiketianqi.com/free/week",
        "99562963",
        "qo7DXwM4"
    )
    da.get_and_read_weather_msg("北京", "daily")
