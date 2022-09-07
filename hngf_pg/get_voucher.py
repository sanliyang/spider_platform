import requests


from tools.c_encrypt import CEncrypt
from tools.c_get_config import CGetConfig
from tools.c_resource import CResource
from tools.record_log import recordLog


class get_voucher:

    def __init__(self):
        self.logger = recordLog()
        self.cg = CGetConfig(CResource.config_path)
        self.logger.info("正在读取配置文件...")
        self.login_url_cookie = self.cg.get_value("tools_website_voucher", "login_url_cookie")
        self.login_url_token = self.cg.get_value("tools_website_voucher", "login_url_token")
        self.logout_url = self.cg.get_value("tools_website_voucher", "logout_url")
        self.username = self.cg.get_value("tools_website_voucher", "username")

        password_en_str = self.cg.get_value("tools_website_voucher", "password")
        password_en_byte = eval(password_en_str)

        sign_str = self.cg.get_value("tools_website_voucher", "sign_str")
        sign_byte = eval(sign_str)

        r = CEncrypt()
        self.logger.info("正在对用户密码进行解密...")
        public_rsa_key = r.read_rsa_public_key(CResource.public_path)
        private_rsa_key = r.read_rsa_private_key(CResource.private_path)
        sign_end = r.verify(password_en_byte, sign_byte, public_rsa_key)

        if sign_end:
            end_byte = r.decrypt_with_rsa(password_en_byte, private_rsa_key)
            self.password = bytes.decode(end_byte)
            self.logger.info("用户密码解密成功...")
        else:
            self.logger.error("用户密码解密失败...")
            self.password = None

    def get_base_headers(self):
        headers = {
            "User-Agent": self.cg.get_value("tools_requests", "User-Agent")
        }
        return headers

    def req_login_cookie(self):
        """
        登录网站， 获取cookie
        :return: response对象
        """
        data = {
            "username": self.username,
            "password": self.password
        }

        base_headers = self.get_base_headers()
        response = requests.post(self.login_url_cookie, data=data, headers=base_headers)
        if response.status_code == 200:
            self.logger.info("[{}]用户登录获取cookie成功...".format(self.username))
            return response
        else:
            self.logger.error("[{}]用户登录获取cookie失败...".format(self.username))

    def req_login_token(self, cookie):
        """
        登录网站获取token和cookie
        :param cookie: 登录网站获取cookie的cookie
        :return: response对象
        """
        data = {
            "username": self.username,
            "password": self.password
        }
        base_header = self.get_base_headers()
        add_header = {
            "Cookie": cookie
        }
        header = self.add_header(base_header, add_header)
        response = requests.post(self.login_url_token, data=data, headers=header)
        if response.status_code == 200:
            self.logger.info("[{}]用户登录获取token和cookie成功...".format(self.username))
            return response
        else:
            self.logger.error("[{}]用户登录获取token和cookie失败...".format(self.username))

    @staticmethod
    def add_header(base_header, add_header):
        """
        两个dict合并
        :param base_header: 最基础的header， 里面只有user-agent
        :param add_header: 在基础的header之上进行增加需要的参数
        :return: 合并后的header
        """
        new_header = {}
        new_header = base_header.copy()
        new_header.update(add_header)
        return new_header

    def req_logout(self):
        """
        登出网站
        :return: response对象
        """
        add_headers = {
            "username": self.username,
            "prical": self.username
        }
        base_header = self.get_base_headers()
        headers = self.add_header(base_header, add_headers)
        resp_logout = requests.get(self.logout_url, headers=headers)
        if resp_logout.status_code == 200:
            self.logger.info("[{}]用户登出成功...".format(self.username))
            return resp_logout
        else:
            self.logger.error("[{}]用户登出失败...".format(self.username))


if __name__ == '__main__':
    gv = get_voucher()
    x = gv.req_login_cookie()
    print(x.status_code)
    print(x.text)
    print(x.headers.items())
    print(x.headers.get("Set-Cookie"))
    cookie = x.headers.get("Set-Cookie").split(";")[0]
    print("======================================")
    z = gv.req_login_token(cookie)
    print(z.status_code)
    print(z.text)
    print("======================================")
    y = gv.req_logout()
    print(y.status_code)
    print(y.text)
