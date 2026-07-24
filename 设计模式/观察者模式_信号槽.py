# -*- coding: UTF-8 -*-
from blinker import signal
from typing import List, Tuple, Any

"""
观察者模式（发布-订阅）的 Blinker 信号实现
本示例使用 Blinker 信号库替代手写回调列表，实现完全解耦。

关键特性：
- 使用全局信号 status_changed，发布者只负责发射信号，不关心谁订阅。
- 订阅者（UI、Logger）在初始化时自行连接信号。
- signal.send() 返回一个列表：[(receiver, return_value), ...]，
  其中每个元素是接收者函数及其返回值。如果没有任何订阅者，返回空列表 []。
- 我们选择忽略该返回值（即不接收、不处理），符合“不获取返回值”的要求。
"""

# 定义一个全局信号，用于通知网络状态变化
status_changed = signal('status-changed')


class NetworkManager:
    """
    网络管理器（发布者）
    管理连接状态，并在状态变化时发射信号。
    不关心订阅者的返回结果。
    """

    def connect(self) -> None:
        """
        建立网络连接，发射 '已连接' 信号。
        说明：
            - status_changed.send(self, is_connected=True) 会返回一个列表，包含所有订阅者（槽函数）的返回值。
            - 我们选择不接收这个返回值，即忽略它，符合“不获取返回值”的目标。
            - 若需调试，可捕获返回值并打印，但不影响主流程。
        """
        # 发射信号，传入发送者 self 和参数 is_connected
        # 返回值示例：[ (<function UI.update_icon at 0x...>, None), ... ]
        status_changed.send(self, is_connected=True)
        # 此处未使用返回值，直接丢弃

    def disconnect(self) -> None:
        """断开网络连接，发射 '已断开' 信号，同样忽略所有返回结果。"""
        status_changed.send(self, is_connected=False)


class UI:
    """
    用户界面模块（订阅者）更新图标反映连接状态。
    """

    def __init__(self, network: NetworkManager) -> None:
        self.network = network
        # 连接信号，当 status_changed 发射时自动调用 update_icon
        status_changed.connect(self.update_icon)

    def update_icon(self, sender: Any, is_connected: bool) -> None:
        """
        槽函数：根据连接状态更新图标。
        参数：
            sender: 发送者对象（通常是 NetworkManager 实例）
            is_connected: 连接状态布尔值
        返回值：
            None （不返回任何值，所以 send() 返回的列表中此项为 None）
        """
        icon = '🟢' if is_connected else '🔴'
        print(f"更新图标：{icon}")


class Logger:
    """
    日志模块（订阅者）记录网络状态变化。
    """

    def __init__(self, network: NetworkManager) -> None:
        self.network = network
        status_changed.connect(self.log_status)

    def log_status(self, sender: Any, is_connected: bool) -> None:
        """
        槽函数：记录状态日志。
        参数：
            sender: 发送者
            is_connected: 连接状态
        返回值：None
        """
        status = '已连接' if is_connected else '已断开'
        print(f"[Logger] 连接状态：{status}")


if __name__ == "__main__":
    # 创建发布者
    net = NetworkManager()

    # 创建订阅者（构造时自动连接信号）
    ui = UI(net)
    logger = Logger(net)

    print("--- 触发连接事件（忽略返回值） ---")
    net.connect()  # 发射信号，所有槽函数被调用，返回值被丢弃

    print("\n--- 触发断开事件（同样忽略返回值） ---")
    net.disconnect()

    # ---------- 可选演示：查看 send() 实际返回的内容 ----------
    print("\n--- 演示：直接调用信号并查看返回值列表 ---")
    # 直接调用信号，接收其返回的列表
    returns: List[Tuple[Any, Any]] = status_changed.send(None, is_connected=True)
    print(f"send() 返回的列表长度：{len(returns)}")
    for receiver, ret_val in returns:
        print(f"  接收者：{receiver.__name__}，返回值：{ret_val}")
