# -*- coding: utf-8 -*-
# @Time : 2022/5/31 17:03
# @Author : sanliy
# @File : encrypt_pic
# @software: PyCharm
import cv2
import numpy as np

from tools.c_file import CFile


class encrypt_pic:

    def encrypt(self, pic_path, encrypt_img_path, result_path):
        if not CFile.path_is_exist(encrypt_img_path):
            self.random_encrypt_img(encrypt_img_path)
        encrypt_img_obj = cv2.imread(encrypt_img_path)
        img_ndarray = cv2.imread(pic_path)
        result_img = cv2.bitwise_xor(img_ndarray, encrypt_img_obj)
        cv2.imwrite(result_path, result_img)

    def random_encrypt_img(self, encrypt_path):
        encrypt_img = np.random.randint(0, 256, size=(1080, 2560, 3), dtype=np.uint8)
        cv2.imwrite(encrypt_path, encrypt_img)


if __name__ == '__main__':
    ep = encrypt_pic()
    # ep.encrypt("../pic/one.png", "../pic/encrypt.png", "../pic/result.png")
    ep.encrypt("../pic/result.png", "../pic/encrypt.png", "../pic/result1.png")
