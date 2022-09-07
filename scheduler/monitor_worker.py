from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED, EVENT_JOBSTORE_ADDED, \
    EVENT_SCHEDULER_STARTED
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from scheduler.base_listener import base_listener
from tools.c_monitor import CMonitor
from tools.c_time import CTime
from tools.record_log import recordLog


class monitor_worker(base_listener):

    def __init__(self):
        super(monitor_worker, self).__init__()
        self.logger = recordLog()
        self.executor = {
            "监视cpu占用率工人": ThreadPoolExecutor(3),
            "监视网络情况工人": ThreadPoolExecutor(3)
        }
        self.monitor_worker_sch = BackgroundScheduler(executors=self.executor, timezone='Asia/Shanghai')
        self.base_sch = self.monitor_worker_sch
        self.monitor_worker_sch._logger = self.logger
        self.cm = CMonitor()

    def get_class_name(self):
        return self.__class__.__name__

    def monitor_cpu_percent_job(self):
        if float(self.cm.get_cpu_use_percent()) < 50:
            self.logger.info(
                "机器工人[{0}], 正在监控机器状况，当前系统cpu的占用率为[{1}]%...\n".format(
                    self.get_class_name(),
                    self.cm.get_cpu_use_percent()
                )
            )
        else:
            self.logger.warning(
                "机器工人[{0}]提醒, 当前系统cpu的占用率为[{1}]%, 已经超过了50%，请谨慎使用！...\n".format(
                    self.get_class_name(),
                    self.cm.get_cpu_use_percent())
            )

    def monitor_net_job(self):
        self.logger.info(
            "机器工人[{0}], 正在监控机器状况，当前系统网络上传速度为[{1}], 下载速度为[{2}]...\n".format(
                self.get_class_name(),
                self.cm.network()[0],
                self.cm.network()[1]
            )
        )


if __name__ == '__main__':
    mw = monitor_worker()
    a = mw.monitor_worker_sch.add_job(
        func=mw.monitor_cpu_percent_job,
        trigger="interval",
        seconds=5,
        executor="监视cpu占用率工人",
        id='monitor_cpu_percent_task',
        name="监视cpu占用率任务"
    )
    b = mw.monitor_worker_sch.add_job(
        func=mw.monitor_net_job,
        trigger="interval",
        seconds=10,
        executor="监视网络情况工人",
        id='monitor_net_job_task',
        name="监视网络情况任务"
    )
    mw.monitor_worker_sch.add_listener(
        mw.job_start_listener,
        EVENT_SCHEDULER_STARTED
    )
    mw.monitor_worker_sch.add_listener(
        mw.job_status_listener,
        EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED
    )
    mw.monitor_worker_sch.add_listener(
        mw.job_list_listener,
        EVENT_JOBSTORE_ADDED
    )
    mw.monitor_worker_sch.start()

    CTime.sleep(100000)
