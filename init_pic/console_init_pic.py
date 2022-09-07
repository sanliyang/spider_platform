from tools.c_resource import CResource
from tools.c_time import CTime
from tools.record_log import recordLog


class console_init_pic:
    def __init__(self):
        self.logger = recordLog()
        self.init_pic = CResource.init_pic_path
        self.show_type = CResource.init_show_type
        self.foregroundColor = CResource.init_foregroundColor
        self.backgroundColor = CResource.init_backgroundColor

    def print_pic(self):
        self.logger.info("正在初始化自动化订购系统...")
        CTime.sleep(3)
        file_object = open(self.init_pic)
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        print("\033[{0};{1};{2}m\t\n{3}\033[0m".format(
            self.show_type,
            self.foregroundColor,
            self.backgroundColor,
            all_the_text
        ))


if __name__ == '__main__':
    cip = console_init_pic()
    cip.print_pic()
