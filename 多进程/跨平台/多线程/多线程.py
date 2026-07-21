# -*- coding: UTF-8 -*-
import threading
import sys
import time  

# ==================== 全局变量定义 ====================
i = 0
# 线程锁：保护共享变量 i，防止多线程同时修改导致数据错乱
lock = threading.Lock()



def child(thread_name):
    with lock:
        # 获取当前线程对象，以便获取更多线程信息
        current_thread = threading.current_thread()
        # 打印详细信息：线程名称、参数、线程ID、是否为守护线程
        print(f"[线程信息] 我是子线程 '{thread_name}'，"
              f"线程ID: {current_thread.ident}，"
              f"守护线程: {current_thread.daemon}",
              flush=True)  # flush=True 立即刷新输出，确保在IDLE中也能正常显示


def change():
    global i  # 声明使用全局变量 i
    # 使用 with 语句获取锁，保护临界区代码
    with lock:
        old_value = i
        i = old_value + 2
        print(f"[变量修改] 线程 {threading.current_thread().name} "
              f"将 i 从 {old_value} 修改为 {i}",
              flush=True)


# ==================== 主程序入口 ====================
def main():

    
    # ---------- 第一部分：演示多线程基本执行 ----------
    print("\n【第一部分】创建并启动两个子线程（无数据竞争）")
    
    # 创建两个线程，分别传入不同的参数 "a" 和 "b"
    # target: 指定线程执行函数
    # args: 传递给目标函数的参数元组
    
    # daemon=True  → 后台服务
    #   特点：不会阻止程序退出
    #   行为：主程序结束时，被强制终止
    #
    # daemon=False → 前台任务
    #   特点：会阻止程序退出
    #   行为：主程序必须等它完成才能退出
    #
    # 程序退出规则：
    #   等待所有 daemon=False 的线程完成
    #   忽略所有 daemon=True 的线程（直接终止）
    t1 = threading.Thread(target=child, args=("a",), name="Thread-A", daemon=True)
    t2 = threading.Thread(target=child, args=("b",), name="Thread-B", daemon=True)
    
    t1.start()
    t2.start()
    
    t1.join() #阻塞当前线程，直到被调用的线程执行完毕才继续执行
    t2.join()
    print("两个子线程已执行完毕")
    
    # ---------- 第二部分：演示共享变量加锁保护 ----------
    print("\n【第二部分】演示多线程修改共享变量（加锁保护）")
    print(f"初始值: i = {i}")
    
    # 创建两个线程，都执行 change 函数
    # 每个线程都会将 i 增加 2，预期最终结果应为 4
    t3 = threading.Thread(target=change, name="Change-Thread-1")
    t4 = threading.Thread(target=change, name="Change-Thread-2")
    
    print(f"已创建修改线程: {t3.name} 和 {t4.name}")
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    


# ==================== 程序执行入口 ====================
if __name__ == "__main__":
    """
    当脚本被直接运行时（而非作为模块导入），执行 main 函数
    这样可以避免在 IDLE 或交互式环境中被意外执行
    """
    main()
