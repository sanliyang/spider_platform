import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

# 创建执行器  用于支持多进程/多线程
executor = ProcessPoolExecutor(max_workers=5)

# 创建调度器
scheduler = BackgroundScheduler(executors={'default': executor})


def func1():
    print("aaaaaaaaaaaaaaa")


# 添加任务
# date  只执行一次
# scheduler.add_job(func1, "date", run_date='2019-08-29 14:53:40', args=['zs', 30])
# interval 周期执行 参数是时间间隔
# scheduler.add_job(func1, "interval", seconds=10, args=['zs', 30])
# cron 周期执行 参数是时间   每月1号3点会执行一次
# scheduler.add_job(func1, "cron", day=1, hour=3, args=['zs', 30])

# 秒针每次到30时执行一次
scheduler.add_job(func1, "interval", seconds=3)

# 启动调度器
scheduler.start()

while True:
    time.sleep(24 * 60 * 60)