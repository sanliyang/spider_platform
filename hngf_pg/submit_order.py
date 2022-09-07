import requests

from tools.c_get_config import CGetConfig
from tools.c_json import CJson
from tools.c_resource import CResource
from tools.c_time import CTime
from tools.record_log import recordLog


class submit_order:

    def __init__(self):
        self.logger = recordLog()
        self.cg = CGetConfig(CResource.config_path)
        self.logger.info("正在读取配置文件...")
        self.submit_url = self.cg.get_value("tools_website_voucher", "submit_url")
        self.save_order_url = self.cg.get_value("tools_website_voucher", "save_order_url")
        self.shop_inner_url = self.cg.get_value("tools_website_voucher", "shop_inner_url")
        self.shopping_url = self.cg.get_value("tools_website_voucher", "shopping_url")

    def get_chart_count(self, headers, json):
        response_chart_count = requests.post(self.shopping_url, headers=headers, json=json)
        caculate_date = CTime.get_date()
        # caculate_date = "2022-06-07"
        chart_count = 0
        if response_chart_count.status_code == 200:
            self.logger.info("正在获取[{0}]购物车中订单数量...".format(caculate_date))
            cj = CJson()
            cj.load(response_chart_count.text)
            pagesinfo = cj.json_path("pageInfo")
            for pageinfo in pagesinfo:
                today_date = pageinfo.get("DFORMAT")
                if str(caculate_date) == today_date:
                    # 获取今天购物车的产品数量
                    chart_count = pageinfo.get("shopNormalPageInfo").get("total")
                    self.logger.info("获取到[{0}]购物车中的订单数量为[{1}]...".format(caculate_date, chart_count))
                    return True, chart_count
            if chart_count == 0:
                return True, chart_count
        else:
            self.logger.error(
                "获取[{0}]购物车中的订单数量失败, 响应状态码为[{1}], 响应信息为[{2}]".format(
                    caculate_date,
                    response_chart_count.status_code,
                    response_chart_count.text
                ))
            return False, chart_count

    def submit_save_order(self, headers, count_json, productIds, username):
        status, shoppingIds = self.get_shop_inner_list(headers, count_json, productIds, username)
        if not status or shoppingIds is []:
            return False
        str_shoppingIds = ",".join(str(shoppingid) for shoppingid in shoppingIds)
        submit_save_order_json = {
            "username": username,
            "shoppingIDs": str_shoppingIds,
            "release": False,
            "sendMail": True
        }
        response_save_order = requests.post(self.save_order_url, headers=headers, json=submit_save_order_json)
        if response_save_order.status_code == 200:
            cj = CJson()
            cj.load(response_save_order.text)
            order_batch = cj.json_path_one("result")
            self.logger.info("批次[{0}]订单保存成功...".format(order_batch))
            return True, [order_batch], str_shoppingIds

        return False

    def get_shop_inner_list(self, headers, count_json, productIds: list, username):
        status, rows = self.get_chart_count(headers, count_json)
        if not status or rows == 0:
            return False
        shop_inner_json = {
            "page": 1,
            "day": str(CTime.get_date()),
            "rows": rows,
            "username": username
        }
        response_shop_inner_list = requests.post(self.shop_inner_url, headers=headers, json=shop_inner_json)
        if response_shop_inner_list.status_code == 200:
            self.logger.info("获取[{0}]购物车中产品详细信息成功...".format(CTime.get_date()))
            cj = CJson()
            cj.load(response_shop_inner_list.text)
            products_info = cj.json_path("pageInfo.list")
            shoppingIds = []
            for product_info in products_info:
                if product_info.get("PRODUCTID") in productIds:
                    shoppingIds.append(product_info.get("shoppingID"))
            return True, shoppingIds
        return False, []

    def submit_order_pg(self, headers, count_json, productIds, username, order_title):
        status, order_batch, str_shoppingIds = self.submit_save_order(
            headers,
            count_json=count_json,
            productIds=productIds,
            username=username
        )
        if not status or order_batch == []:
            return False
        submit_order_json = {
            "remark": order_title,
            "mainids": order_batch,
            "shopids": str_shoppingIds,
            "english": False,
            "agency": False
        }
        response_submit = requests.post(self.submit_url, headers=headers, json=submit_order_json)
        if response_submit.status_code == 200:
            self.logger.info("订单提交成功...")
            return True, response_submit
        else:
            self.logger.info(
                "[{0}]订单在提交的过程中失败, 响应状态码为[{1}], 响应信息为[{2}]".format(
                    productIds,
                    response_submit.status_code,
                    response_submit.text
                ))
            return False
