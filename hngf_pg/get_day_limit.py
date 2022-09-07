import requests


from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.record_log import recordLog


class get_day_limit:

    def __init__(self):
        self.logger = recordLog()
        self.cg = CGetConfig(CResource.config_path)
        self.logger.info("正在读取配置文件...")
        self.limit_url = self.cg.get_value("tools_website_voucher", "limit_url")

    def get_limit(self, headers, json):
        response_limit = requests.post(self.limit_url, headers=headers, json=json)
        if response_limit.status_code == 200:
            self.logger.info("产品查询成功...")
        return response_limit