# -*- coding: utf-8 -*-
# @Time : 2022/6/8 10:31
# @Author : sanliy
# @File : get_ip_location
# @software: PyCharm
import IP2Location
import requests

from tools.c_json import CJson


class getIpLocation:

    def __init__(self, ip_address):
        # https://www.ip2location.com/development-libraries/ip2location/python
        # database = IP2Location.IP2Location(os.path.join("data", "IPV6-COUNTRY.BIN"), "SHARED_MEMORY")
        self.database = IP2Location.IP2Location("./IP2LOCATION-LITE-DB5.BIN")
        self.rec = self.database.get_all(ip_address)
        self.detail_msg = None
        self.cj = CJson()

    def get_city_piny(self):
        """
        获取ip所属城市的拼音
        :return:
        """
        return self.rec.city

    def get_country_short_en(self):
        """
        获取ip所在国家的英文简写
        :return:
        """
        return self.rec.country_short

    def get_country_long_en(self):
        """
        获取ip所在国家的英文
        :return:
        """
        return self.rec.country_long

    def get_region_piny(self):
        """
        获取ip所在省的拼音
        :return:
        """
        return self.rec.region

    def get_latitude(self):
        """
        获取ip所在的纬度
        :return:
        """
        return self.rec.latitude

    def get_longitude(self):
        """
        获取ip所在的经度
        :return:
        """
        return self.rec.longitude

    def get_detail_json_msg(self, baidu_ak, lon, lat):
        """
        根据经纬度获取详细的地址信息(使用百度地图的API)
        :param baidu_ak: 百度地图应用的AK
        :param lon: 经度
        :param lat: 纬度
        :return:
        """
        response = requests.get(
            url="https://api.map.baidu.com/reverse_geocoding/v3/?ak={0}&output=json&coordtype=wgs84ll&location={1},{2}".
                format(baidu_ak, lat, lon)
        )
        if response.status_code == 200:
            self.detail_msg = response.text
            self.cj.load(self.detail_msg)
            return response.text
        return None

    def get_detail_location(self):
        """
        根据经纬度获取详细的地址信息
        :return:
        """
        if self.detail_msg is not None:
            detail_location = self.cj.json_path_one("result.formatted_address")
            return detail_location

    def get_business_circle(self):
        """
        根据经纬度获取附近的商业圈
        :return:
        """
        if self.detail_msg is not None:
            business_circle = self.cj.json_path_one("result.business")
            return business_circle


if __name__ == '__main__':
    gip = getIpLocation("117.61.17.9")
    print(gip.get_city_piny())
    print(gip.get_region_piny())
    print(gip.get_country_short_en())
    print(gip.get_country_long_en())
    print(gip.get_longitude())
    print(gip.get_latitude())
    detail_msg = gip.get_detail_json_msg(
        "KuuyE4zrAqlhktHtiwh5OG2HcPGEvinj",
        gip.get_longitude(),
        gip.get_latitude()
    )
    print(detail_msg)
    print(gip.get_detail_location())
