import psutil


class CMonitor:

    @staticmethod
    def cpu_count():
        """
        查看cpu物理个数
        :return:
        """
        return psutil.cpu_count(logical=False)

    @staticmethod
    def get_cpu_use_percent():
        """
        获取cpu使用率
        :return:
        """
        return str(psutil.cpu_percent(interval=2, percpu=False))

    @staticmethod
    def get_totle_memory():
        """
        获取总内存
        :return:
        """
        return str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)) + "GB"

    @staticmethod
    def get_free_memory():
        """
        获取空闲内存
        :return:
        """
        return str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2)) + "GB"

    @staticmethod
    def user():
        """
        获取用户个数和登录的用户名称
        :return:
        """
        users_count = len(psutil.users())
        user_name = ",".join([u.name for u in psutil.users()])
        all_users = [users_count, user_name]
        return all_users

    @staticmethod
    def network():
        """
        获取网卡的入网流量和出网流量
        :return:
        """
        net = psutil.net_io_counters()
        bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)  # 网卡接收流量
        bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)  # 网卡发送流量
        net_list = [bytes_rcvd, bytes_sent]
        return net_list


if __name__ == '__main__':
    cm = CMonitor()
    print(cm.cpu_count())
    print(cm.get_cpu_use_percent())
    print(cm.get_totle_memory())
    print(cm.get_free_memory())
    print(cm.network())
    print(cm.user())
