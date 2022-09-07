# -*- coding: utf-8 -*-
# @Time : 2022/4/25 11:06
# @Author : sanliy
# @File : windows_msg
# @software: PyCharm
from win10toast import ToastNotifier
from tools.record_log import recordLog


class windowsNote:

    def __init__(self, title, content, icon_path, duration):
        self.log = recordLog()
        self.toaster = ToastNotifier()
        self.title = title
        self.content = content
        self.icon_path = icon_path
        self.duration = duration   # 通知存在的时间长短

    def send_to_windows(self):
        self.log.info("正在向windows电脑发送通知信息...")
        self.toaster.show_toast(self.title, self.content, self.icon_path, self.duration)


if __name__ == '__main__':
    wn = windowsNote('标题', '这里是内容', icon_path=None, duration=10)
    wn.send_to_windows()
