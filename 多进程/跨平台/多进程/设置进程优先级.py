# -*- coding: UTF-8 -*-
import psutil
import os

# 创建windows下的反向映射字典
NICE_TO_CONST = {
    psutil.IDLE_PRIORITY_CLASS: 'IDLE',
    psutil.BELOW_NORMAL_PRIORITY_CLASS: 'BELOW_NORMAL',
    psutil.NORMAL_PRIORITY_CLASS: 'NORMAL',
    psutil.ABOVE_NORMAL_PRIORITY_CLASS: 'ABOVE_NORMAL',
    psutil.HIGH_PRIORITY_CLASS: 'HIGH',
    psutil.REALTIME_PRIORITY_CLASS: 'REALTIME',
}


proc = psutil.Process()
nice_val = proc.nice()
const_name = NICE_TO_CONST.get(nice_val, 'UNKNOWN')
print(f"PID: {proc.pid}")
print(f"进程名: {proc.name()}")
print(f"内存占用: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
print(f"Nice 值: {nice_val}, 对应常量: psutil.{const_name}_PRIORITY_CLASS")








print("修改进程优先级")
try:
    proc.nice(psutil.HIGH_PRIORITY_CLASS)
except psutil.AccessDenied:
    print("权限不足，无法修改 nice 值")
except ValueError as e:
    print(f"nice 值超出范围: {e}")

nice_val = proc.nice()
const_name = NICE_TO_CONST.get(nice_val, 'UNKNOWN')
print(f"Nice 值: {nice_val}, 对应常量: psutil.{const_name}_PRIORITY_CLASS")
