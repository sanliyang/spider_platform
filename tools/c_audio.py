# -*- coding: utf-8 -*-
# @Time : 2022/5/16 16:31
# @Author : sanliy
# @File : c_audio
# @software: PyCharm
import pyttsx3


class CAudio:
    def __init__(self):
        """
        初始化引擎对象
        """
        self.engine = pyttsx3.init()

    def wait_engine(self):
        """
        使引擎进入等待状态
        :return: 无返回值
        """
        self.engine.runAndWait()

    def say(self, msg):
        """
        实现朗读文本
        :param msg: 待朗读的文本
        :return: 无返回值
        """
        self.engine.say(msg)
        self.wait_engine()

    def get_speed(self):
        """
        获取当前设备朗读的速度
        :return: 返回值为当前设备朗读的速度
        """
        return self.engine.getProperty('rate')

    def change_speed(self, change_speed_num: int):
        """
        改变当前设备朗读的速度
        :param change_speed_num: 更改的朗读速度值
        :return: 无返回值
        """
        rate = self.get_speed()
        self.engine.setProperty('rate', rate + change_speed_num)

    def save_audio(self, msg, file_name_with_path):
        """
        保存文本信息为音频文件
        :param msg: 文本信息
        :param file_name_with_path: 音频文件， 路径+名字+后缀名
        :return: 无返回值
        """
        self.engine.save_to_file(msg, file_name_with_path)

    def get_all_voice(self):
        """
        获取当前设备的所有的嗓音对象
        :return: 返回值为嗓音对象列表
        """
        return self.engine.getProperty('voices')

    def get_voice_id(self, voice):
        """
        根据嗓音对象，获取当前嗓音的id，用于改变嗓音
        :param voice: 嗓音对象
        :return: 返回值为嗓音对象的id
        """
        return voice.id

    def change_voice(self, voice_id):
        """
        根据嗓音的id改变当前设备朗读嗓音
        :param voice_id:嗓音的id
        :return: 返回值为当前嗓音的id号
        """
        self.engine.setProperty('voice', voice_id)

    def get_volume(self):
        """
        获取当前设备音量
        :return: 返回值为当前设备的音量
        """
        return self.engine.getProperty('volume')

    def change_volume(self, change_volume_num: float):
        """
        更改朗读音量
        :param change_volume_num: 更改的朗读音量值， 浮点型， 介于 0.0 - 1.0 之间
        :return: 无返回值
        """
        volume = self.get_volume()
        if change_volume_num < 0.0 or change_volume_num > 1.0:
            self.engine.setProperty('volume', volume)
        else:
            self.engine.setProperty('volume', volume - change_volume_num)


if __name__ == '__main__':
    ca = CAudio()
    print(ca.get_all_voice())
