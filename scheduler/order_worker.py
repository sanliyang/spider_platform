from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED, EVENT_JOBSTORE_ADDED, \
    EVENT_SCHEDULER_STARTED
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from hngf_pg.submit_order_process import submit_order_process
from scheduler.base_listener import base_listener
from tools.record_log import recordLog


class order_worker(base_listener):

    def __init__(self):
        super(order_worker, self).__init__()
        self.logger = recordLog()
        self.executor = {
            "订单提交流程工人": ThreadPoolExecutor(3)
        }
        self.order_worker_sch = BlockingScheduler(executors=self.executor, timezone='Asia/Shanghai')
        self.base_sch = self.order_worker_sch
        self.order_worker_sch._logger = self.logger

    def get_class_name(self):
        return self.__class__.__name__

    def flow_submit_order_job(self):
        self.logger.info("自动化提交订单任务已经启动...")
        sub = submit_order_process()
        sub.process()


if __name__ == '__main__':
    ow = order_worker()
    ow.order_worker_sch.add_job(
        func=ow.flow_submit_order_job,
        trigger="interval",
        seconds=120,
        executor="订单提交流程工人",
        id='flow_submit_order_task',
        name="订单提交流程任务"
    )
    ow.order_worker_sch.add_listener(
        ow.job_status_listener,
        EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_EXECUTED
    )
    ow.order_worker_sch.add_listener(
        ow.job_list_listener,
        EVENT_JOBSTORE_ADDED
    )
    ow.order_worker_sch.add_listener(
        ow.job_start_listener,
        EVENT_SCHEDULER_STARTED
    )
    ow.order_worker_sch.start()
