import os
import threading
import uuid

from apscheduler.events import EVENT_JOBSTORE_ADDED, EVENT_SCHEDULER_STARTED


class base_listener:

    def __init__(self):
        self.base_sch = None
        self.logger = None

    def job_status_listener(self, Event):
        job = self.base_sch.get_job(Event.job_id)
        if not Event.exception:
            self.logger.info(
                "[{0}]--[{1}]正在执行编号为[{2}]的[{3}]类型的任务[{4}],"
                "执行此任务的小型工人名称为[{5}], 任务返回值为[{6}], 进程id为[{7}], 线程id为[{8}]\n".format(
                    Event.scheduled_run_time,
                    job.executor,
                    job.id,
                    job.trigger,
                    job.name,
                    job.func.__name__,
                    Event.retval,
                    os.getpid(),
                    threading.get_ident()
                ))
        else:
            self.logger.error(
                "任务名称=[{0}]|任务执行类型=[{1}]|异常编号=[{2}]|引发的异常=[{3}]|"
                "异常格式化回溯=[{4}]|任务执行时间=[{5}]|进程id=[{6}]|线程id=[{7}]\n".format(
                    job.name,
                    job.trigger,
                    Event.code,
                    Event.exception,
                    Event.traceback,
                    Event.scheduled_run_time,
                    threading.get_ident(),
                    os.getpid()
                )
            )

    def job_list_listener(self, Event):
        if Event.code == EVENT_JOBSTORE_ADDED:
            for job_detail in self.base_sch.get_jobs():
                self.logger.info(
                    "[{0}]正在将编号为[{1}]的[{2}]类型的任务[{3}]加入到调度器中,"
                    "执行此调度的小型工人名称为[{4}]\n".format(
                        job_detail.executor,
                        job_detail.id,
                        job_detail.trigger,
                        job_detail.name,
                        job_detail.func.__name__
                    ))

    def job_start_listener(self, Event):
        if Event.code == EVENT_SCHEDULER_STARTED:
            self.logger.info("调度中心[{0}]已经准备就绪！\n".format(uuid.uuid4().hex))
