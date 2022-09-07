import requests


from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.record_log import recordLog


class add_shopping_cart:

    def __init__(self):
        self.logger = recordLog()
        self.cg = CGetConfig(CResource.config_path)
        self.logger.info("正在读取配置文件...")
        self.add_shopping_cart_url = self.cg.get_value("tools_website_voucher", "add_shopping_cart_url")
        # self.add_shopping_cart_url = "https://data.cresda.cn/manage/order/shopping/add/normal"

    def add_cart(self, headers, formdata):
        response_add_cart = requests.post(self.add_shopping_cart_url, headers=headers, json=formdata)
        if response_add_cart.status_code == 200:
            self.logger.info("产品加入购物车成功...")
        else:
            self.logger.debug("产品加入购物车失败...")
        return response_add_cart


if __name__ == '__main__':
    add_cart_obj = add_shopping_cart()
    add_cart_response = add_cart_obj.add_cart(headers={}, formdata={})
