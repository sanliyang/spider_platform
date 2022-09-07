# -*- coding: utf-8 -*-
# @Time : 2022/5/23 14:02
# @Author : sanliy
# @File : c_encrypt
# @software: PyCharm
import base64
import hashlib
import rsa

from tools.c_file import CFile


class CEncrypt:

    @classmethod
    def str_2_base64(cls, plaint_text):
        return base64.b64encode(plaint_text.encode("utf-8"))

    @classmethod
    def base64_2_str(cls, cipher_text):
        return base64.b64decode(cipher_text).decode("utf-8")

    @classmethod
    def str_2_md5(cls, plaint_text):
        hash_md5 = hashlib.md5()
        hash_md5.update(plaint_text.encode("utf-8"))
        return hash_md5.hexdigest()

    @classmethod
    def str_2_sha1(cls, plaint_text):
        hash_sha1 = hashlib.sha1()
        hash_sha1.update(plaint_text.encode("utf-8"))
        return hash_sha1.hexdigest()

    def __init__(self):
        """
        生成公钥和私钥
        """
        self.public_rsa_key, self.private_rsa_key = rsa.newkeys(nbits=512)

    def save_rsa(self, public_key_filename, private_key_filename, file_path):
        """
        保存密钥文件
        :param public_key_filename: 公钥文件名
        :param private_key_filename: 私钥文件名
        :param file_path: 保存路径
        :return:
        """
        if not CFile.path_is_exist(file_path):
            CFile.mk_dir(file_path)
        with open(CFile.path_join(file_path, public_key_filename), 'wb') as file_obj:
            file_obj.write(self.public_rsa_key.save_pkcs1())
        with open(CFile.path_join(file_path, private_key_filename), 'wb') as file_obj:
            file_obj.write(self.private_rsa_key.save_pkcs1())

    def read_rsa_public_key(self, public_key_file_name_with_path):
        """
        从文件中读取公钥
        :param public_key_file_name_with_path: 公钥文件地址
        :return:
        """
        with open(public_key_file_name_with_path, 'rb') as file_obj:
            pub = file_obj.read()
            pub_key = rsa.PublicKey.load_pkcs1(pub)
        return pub_key

    def read_rsa_private_key(self, private_key_file_name_with_path):
        """
        从文件中读取私钥
        :param private_key_file_name_with_path: 私钥文件地址
        :return:
        """
        with open(private_key_file_name_with_path, 'rb') as file_obj:
            prt = file_obj.read()
            prt_key = rsa.PrivateKey.load_pkcs1(prt)
        return prt_key

    def encrypt_with_rsa(self, plaint_text, public_rsa_key=None):
        """
        使用公钥加密，如果传入了公钥，则使用传入的公钥进行加密， 如果没有传入公钥，则使用初始化创建实例时的公钥加密
        :param plaint_text: 待机密的明文文本
        :param public_rsa_key: 公钥
        :return:
        """
        if public_rsa_key:
            return rsa.encrypt(plaint_text.encode("utf-8"), public_rsa_key)
        return rsa.encrypt(plaint_text.encode("utf-8"), self.public_rsa_key)

    def decrypt_with_rsa(self, cipher_text, private_rsa_key=None):
        """
        使用私钥解密， 如果传入了私钥， 则使用传入的私钥解密， 如果没有传入私钥， 则使用初始化创建实例时的私钥解密
        :param cipher_text: 待解密的密文
        :param private_rsa_key: 私钥
        :return:
        """
        if private_rsa_key:
            return rsa.decrypt(cipher_text, private_rsa_key)
        return rsa.decrypt(cipher_text, self.private_rsa_key).decode("utf-8")

    def sign(self, message, private_rsa_key, hash_method="SHA-256"):
        """
        使用私钥进行签名， 默认hash算法为："SHA-256"， 也可以使用md5， 或者其他hash算法
        :param message: 要签名的数据
        :param private_rsa_key: 私钥
        :param hash_method: hash算法
        :return:
        """
        sign_result = rsa.sign(message, private_rsa_key, hash_method)
        return sign_result

    def verify(self, message, sign, public_rsa_key):
        """
        验签， 使用公钥验证签名是否正确， 如果正确， 则返回签名算法， 否则返回验证失败
        :param message: 已加密的数据
        :param sign: 已签名的数据
        :param public_rsa_key: 公钥
        :return:
        """
        try:
            verify = rsa.verify(message, sign, public_rsa_key)
            return verify
        except rsa.VerificationError:
            return False


