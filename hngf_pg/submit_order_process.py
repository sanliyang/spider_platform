import json
import uuid

from dboperation.c_sqlalchemy import cSqlAlchemy
from hngf_pg.add_shopping_cart import add_shopping_cart
from hngf_pg.get_day_limit import get_day_limit
from hngf_pg.get_voucher import get_voucher
from hngf_pg.query_data import query_data
from hngf_pg.submit_order import submit_order
from tools.c_time import CTime
from tools.record_log import recordLog


class submit_order_process:
    def __init__(self):
        self.logger = recordLog()
        self.csa = cSqlAlchemy()
        self.csa.create_session()

    @staticmethod
    def get_query_json(gv_token_dict, prodid, satelliteSensor, ssSublevel):
        # 获取地区编号
        area = gv_token_dict.get("data").get("register_address")
        # 用户行业编号
        userIndustry = gv_token_dict.get("data").get("industry")
        # 用户类型
        userType = gv_token_dict.get("data").get("usertype")
        # 用户id
        userId = gv_token_dict.get("data").get("userid")

        # 页数
        page = 1
        # 每页显示的个数
        size = len(prodid)
        # 卫星类型
        dwxtype = "gx"
        # 卫星类型
        satelliteType = ["GX"]

        query_json = {
            # 获取产品id
            "prodid": prodid,
            "area": area,
            "userIndustry": userIndustry,
            "userType": userType,
            "userId": userId,
            "page": page,
            "size": size,
            # 星源系列类型
            "satelliteSensor": satelliteSensor,
            "dwxtype": dwxtype,
            "satelliteType": satelliteType,
            # 产品等级
            "ssSublevel": ssSublevel
        }
        return query_json

    @staticmethod
    def get_query_header(gv_token_dict, cookie):
        # 获取检索所需要的headers信息
        add_headers = {
            "Cookie": cookie,
            "authorization": gv_token_dict.get("data").get("token"),
            "prical": gv_token_dict.get("data").get("username")
        }
        return add_headers

    @staticmethod
    def get_add_cart_data(response_query):
        null = None
        false = False
        true = True
        query_text_dict = eval(response_query.text)
        records = query_text_dict.get("result").get("records")
        if records is None:
            return False
        objectids = []
        for record in records:
            objectids.append(record.get("id"))
        if not objectids:
            return False
        formdata = {
            "metaList": records,
            "objectids": objectids
        }
        return formdata

    def get_order_msg(self) -> list:
        order_all_row = self.csa.fetchall(
            '''
            select id, orderdata, ordertitle from ac_order where issubmit = :issubmit
            ''',
            {
                "issubmit": "0"
            }
        )
        order_z_all_row = self.csa.fetchall(
            '''
            select id, orderdata, ordertitle from ac_order_z where issubmit = :issubmit
            ''',
            {
                "issubmit": "0"
            }
        )
        order_z_all_row.extend(order_all_row)
        return order_z_all_row

    def backtract_2_db_order_z(self, productIds, satellite, sensor, productlevels, order_title) -> bool:
        """
        将剩余无法提交的产品号回溯到ac_order_z表中，方便下次进行提交
        :param order_title:
        :param satellite:
        :param sensor:
        :param productlevels:
        :param productIds:
        :return:
        """
        # 构造 orderdata 字段
        orderdata = {
            "productIds": productIds,
            "satellite": satellite,
            "sensor": sensor,
            "productlevels": productlevels
        }
        ac_order_z_id = uuid.uuid4().hex
        ac_order_z_title = order_title

        # 将数据插入到ac_order_z表中
        insert_result = self.csa.execute(
            '''
            insert into ac_order_z (id, ordertitle, orderdata, creatorid, issubmit) 
            values (:id, :ordertitle, :orderdata, :creatorid, :issubmit)
            ''',
            {
                "id": ac_order_z_id,
                "ordertitle": ac_order_z_title,
                "orderdata": json.dumps(orderdata),
                "creatorid": "hngf_auto_system",
                "issubmit": 0
            }
        )
        if insert_result:
            self.logger.info("未提交的订单成功回溯到数据库中...")
        else:
            self.logger.error("未提交的订单回溯数据库中失败，请检查...")
        return insert_result

    def process(self):
        # 1. 登录
        gv = get_voucher()
        gv_cookie_resp = gv.req_login_cookie()
        if gv_cookie_resp.status_code == 200:
            self.logger.info("登录cookie获取成功,正在进行登录用户信息的获取...")
            cookie = gv_cookie_resp.headers.get("Set-Cookie").split(";")[0]
            # 获取登录的token， 以及登录用户的个人信息
            gv_token_resp = gv.req_login_token(cookie)
            null = None
            false = False
            gv_token_dict = eval(gv_token_resp.text)
            add_headers = self.get_query_header(gv_token_dict, cookie)
            base_headers = gv.get_base_headers()
            query_headers = gv.add_header(base_headers, add_headers)
            # 从数据库中读取订单信息
            order_all_row = self.get_order_msg()
            for order_msg in order_all_row:
                order_id = order_msg[0]
                order_product = order_msg[1]
                order_title = order_msg[2]

                order_product_dict = eval(order_product)

                productIds = order_product_dict.get("productIds")
                sensor = order_product_dict.get("sensor")
                satellite = order_product_dict.get("satellite")
                productlevels = order_product_dict.get("productlevels")
                satelliteSensor_one = satellite + "_" + sensor
                ssSublevel_one = satelliteSensor_one + "_" + productlevels
                satelliteSensor = [satelliteSensor_one]
                ssSublevel = [ssSublevel_one]
                # 1.0.1 检索之前，首先判断今日是否有订购的余量
                gdl = get_day_limit()
                limit_json = {
                    "username": gv_token_dict.get("data").get("username")
                }
                response_limit = gdl.get_limit(headers=query_headers, json=limit_json)
                response_limit_dict = eval(response_limit.text)
                day_totle = response_limit_dict.get("daylimit")
                day_use = response_limit_dict.get("onorder")
                day_free = day_totle - day_use
                self.logger.info("[{0}]今日可提交的订单景数为[{1}]".format(
                    gv_token_dict.get("data").get("username"),
                    day_free)
                )
                if day_free <= 0:
                    self.logger.info("今日已经没有提交订单的余量，请明天再进行订单的提交...")
                    break
                if day_free < len(productIds):
                    self.logger.info(
                        "今日剩余的订单余量已经不足以提交订单[{0}], 只能进行部分订单的提交，"
                        "剩余部分将回溯到ac_order_z表中，等待下次进行提交...".format(
                            order_id
                        ))
                    submit_productIds = productIds[:day_free:]
                    productIds_lave = list(set(productIds) - set(submit_productIds))
                    productIds = submit_productIds
                    if len(productIds_lave) > 0:
                        # 这里将不用于提交的产品号回溯到表中
                        backtract_result = self.backtract_2_db_order_z(
                            productIds_lave,
                            satellite,
                            sensor,
                            productlevels,
                            order_title
                        )
                        if not backtract_result:
                            # 如果回溯失败，就结束今日订单提交（或者可以跳过本订单，进入下一个订单的提交）
                            break
                # 1.1检索
                query_product = query_data()
                query_json = self.get_query_json(gv_token_dict, productIds, satelliteSensor, ssSublevel)
                query_response = query_product.get_records(query_headers, query_json)
                if query_response.status_code == 200:
                    self.logger.info("产品检索成功...")
                    # 1.2加入购物车
                    # 拼接加入购物车需要的data
                    # 用户id
                    userId = gv_token_dict.get("data").get("userid")
                    username = gv_token_dict.get("data").get("username")
                    base_data = {
                        "userId": userId,
                        "username": username
                    }
                    add_cart_data = self.get_add_cart_data(query_response)
                    if not add_cart_data:
                        self.logger.warning("没有检索到产品信息，请检查! 开始下个订单的提交任务...")
                        continue
                    cart_formdata = gv.add_header(base_data, add_cart_data)
                    add_cart_obj = add_shopping_cart()
                    add_cart_response = add_cart_obj.add_cart(headers=query_headers, formdata=cart_formdata)
                    if add_cart_response.status_code == 200:
                        self.logger.info("产品加入购物车成功....")
                        # 1.3提交订单
                        submit_order_json = {
                            "english": True,
                            "page": 1,
                            "username": username
                        }
                        so = submit_order()
                        status, response_save_order = so.submit_order_pg(
                            headers=query_headers,
                            count_json=submit_order_json,
                            productIds=productIds,
                            username=username,
                            order_title=order_title
                        )
                        if not status:
                            self.logger.error("[{0}]订单提交失败,请检查重试...".format(order_id))
                            continue
                        self.logger.info("开始更新数据库中[{0}]的订单状态...".format(order_id))
                        csa = cSqlAlchemy()
                        csa.create_session()
                        try:
                            order_id_row = csa.fetchone(
                                '''
                                select id from ac_order where id = :id
                                ''',
                                {
                                    "id": order_id
                                }
                            )
                            update_ac_order_result = csa.execute(
                                '''
                                update ac_order set issubmit = :issubmit where id = :id
                                ''',
                                {
                                    "issubmit": 1,
                                    "id": order_id
                                }
                            )
                            if update_ac_order_result:
                                self.logger.info("订单[{0}]在ac_order表中的订单状态更新成功...".format(order_id))
                            else:
                                self.logger.error("订单[{0}]在ac_order表中的订单状态更新失败，请检查重试...".format(order_id))
                        except:
                            update_ac_order_z_result = csa.execute(
                                '''
                                update ac_order_z set issubmit = :issubmit where id = :id
                                ''',
                                {
                                    "issubmit": 1,
                                    "id": order_id
                                }
                            )
                            if update_ac_order_z_result:
                                self.logger.info("订单[{0}]在ac_order_z表中的订单状态更新成功...".format(order_id))
                            else:
                                self.logger.error("订单[{0}]在ac_order_z表中的订单状态更新失败，请检查重试...".format(order_id))
                        finally:
                            # 在这里进行对数据表 ac_order_submit_data进行回写
                            for productId in productIds:
                                insert_into_ac_order_submit_data_result = csa.execute(
                                    '''
                                    insert into ac_order_submit_data 
                                    (id, satellite, sensor, productid, status, 
                                    isdownload, remark, addtime, updatetime, orderid) 
                                    VALUES 
                                    (:id, :satellite, :sensor, :productid, :status, 
                                    :isdownload, :remark, :addtime, :updatetime, :orderid)
                                    ''',
                                    {
                                        "id": uuid.uuid4().hex,
                                        "satellite": satellite,
                                        "sensor": sensor,
                                        "productid": productId,
                                        "status": 0,
                                        "isdownload": 0,
                                        "remark": "已提交",
                                        "addtime": CTime.get_now_time(),
                                        "updatetime": CTime.get_now_time(),
                                        "orderid": order_id
                                    }
                                )
                                if insert_into_ac_order_submit_data_result:
                                    self.logger.info("产品号[{0}]回写到ac_order_submit_data表中成功！".format(
                                        productId
                                    ))
                                else:
                                    self.logger.error("产品号[{0}]回写到ac_order_submit_data表中失败！".format(
                                        productId
                                    ))
                    else:
                        self.logger.error(
                            "产品加入购物车失败, 响应状态码为[{0}], 响应信息为[{1}], 请检查后重试...".format(
                                add_cart_response.status_code,
                                add_cart_response.text
                            )
                        )
                else:
                    self.logger.error(
                        "产品检索失败，响应状态码为[{0}], 响应信息为[{1}], 订单id为[{2}]请检查后重试...".format(
                            query_response.status_code,
                            query_response.text,
                            order_id
                        )
                    )
            # 2. 退出登录
            response_logout = gv.req_logout()
            if response_logout.status_code == 200:
                self.logger.info("[{0}]成功登出...".format(gv_token_dict.get("data").get("username")))
            else:
                self.logger.error("[{0}]登出失败...".format(gv_token_dict.get("data").get("username")))
        else:
            self.logger.error(
                "登录cookie获取失败,响应状态码为[{0}],响应信息为[{1}],请检查后重试..."
                .format(gv_cookie_resp.status_code, gv_cookie_resp.text)
            )


if __name__ == '__main__':
    sub = submit_order_process()
    sub.process()
