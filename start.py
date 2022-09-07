from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_MISSED, EVENT_JOBSTORE_ADDED, \
    EVENT_SCHEDULER_STARTED

from init_pic.console_init_pic import console_init_pic
from scheduler.monitor_worker import monitor_worker
from scheduler.order_worker import order_worker
from tools.c_resource import CResource
from tools.clear_log import clearLog

cl = clearLog()
cl.clear_log_for_week()

mw = monitor_worker()
cip = console_init_pic()
cip.print_pic()

a = mw.monitor_worker_sch.add_job(
    func=mw.monitor_cpu_percent_job,
    trigger=CResource.cpu_type,
    seconds=int(CResource.cpu_interval_time),
    executor="监视cpu占用率工人",
    id='monitor_cpu_percent_task',
    name="监视cpu占用率任务"
)
b = mw.monitor_worker_sch.add_job(
    func=mw.monitor_net_job,
    trigger=CResource.net_type,
    seconds=int(CResource.net_interval_time),
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

ow = order_worker()

ow.order_worker_sch.add_job(
    func=ow.flow_submit_order_job,
    trigger=CResource.auto_submit_type,
    hours=int(CResource.auto_subumit_interval_time),
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
