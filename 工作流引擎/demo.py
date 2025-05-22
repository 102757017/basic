# Prefect要求SQLite 版本不能低于 3.9.0
# 导入 Prefect 相关模块
from prefect import task,flow
from prefect import get_client # 对于本地执行并非严格必要，但建议使用
from prefect.filesystems import LocalFileSystem
from prefect.client.schemas.schedules import IntervalSchedule # 用于调度（此处未使用，但了解很好）



#定义任务,括号内的参数可省略
@task(retries=3, retry_delay_seconds=10)
def add_numbers(a, b):
    return a + b

#任务的超时设置,如果任务的执行时间超过 30 秒，Prefect 将自动终止任务，并将其状态标记为失败。
@task(timeout_seconds=30)
def long_running_task():
    import time
    time.sleep(40)  # 模拟一个长时间运行的任务
    return "Task completed!"


#创建流程
@flow
def simple_flow():
    result = add_numbers(2, 3)
    result2 = add_numbers(4, 5)
    print(f"The result is: {result}")





def on_success(flow):
    print(f"Flow '{flow.name}' completed successfully!")
    
def on_failure(flow):
    print(f"Flow '{flow.name}' failed!")

#在这个示例中，定义了两个回调函数 on_success 和 on_failure，分别在流程成功完成和失败时被调用
@flow(on_completion=[on_success, on_failure])
def monitored_flow():
    # 流程中的任务
    pass



if __name__ == "__main__":
    simple_flow()
