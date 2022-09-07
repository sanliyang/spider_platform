# -*- coding: utf-8 -*-
# @Time : 2022/5/12 15:56
# @Author : sanliy
# @File : format_conversion
# @software: PyCharm
import os.path

from pydub import AudioSegment
from tools.record_log import recordLog
from tools.c_file import CFile


class audio_option:
    def __init__(self, audio_path, target_path, ext):
        self.log = recordLog()
        self.audio_path = audio_path
        self.ext = ext
        self.target_path = target_path
        self.audio_obj = self.load_obj()

    def load_obj(self):
        if CFile.path_is_exist(self.audio_path):
            self.log.info("正在加载[{0}]的音频对象...".format(self.audio_path))
            return AudioSegment.from_file(self.audio_path)
        else:
            self.log.info("文件[{0}]不存在，请检查...".format(self.audio_path))
            return None

    def conversion(self):
        main_name = CFile.get_file_main_name(self.audio_path)
        name_with_path = os.path.join(self.target_path, main_name)
        if self.audio_obj is not None:
            self.log.info("正在对[{0}]文件进行格式转换， 正在转换为[{1}]...".format(self.audio_path, self.ext))
            self.audio_obj.export(r'{0}.{1}'.format(name_with_path, self.ext), format=str(self.ext))
        else:
            self.log.info("文件对象为空，无法进行格式转换，请检查[{0}]音频对象是否加载成功...".format(self.audio_path))


if __name__ == '__main__':
    ao = audio_option(r'C:\Users\sanliy\Music\VipSongsDownload\梦的光点.mflac', r'C:\Users\sanliy\Music', 'flac')
    ao.conversion()
