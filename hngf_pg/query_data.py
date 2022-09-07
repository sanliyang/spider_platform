import requests


from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.record_log import recordLog


class query_data:

    def __init__(self):
        self.logger = recordLog()
        self.cg = CGetConfig(CResource.config_path)
        self.logger.info("正在读取配置文件...")
        self.records_url = self.cg.get_value("tools_website_voucher", "records_url")
        # self.records_url = "https://data.cresda.cn/manage/meta/api/metadatas/records"

    def get_records(self, headers, json):
        response_recodes = requests.post(self.records_url, headers=headers, json=json)
        if response_recodes.status_code == 200:
            self.logger.info("产品查询成功...")
        return response_recodes
