# -*- coding: UTF-8 -*-
from typing import Callable, Optional


"""
观察者模式又称为发布-订阅模式，有下面的实现方式
回调函数 vs  Blinker的信号/回调机制：
- 信号/回调机制：发射后无法获取槽函数的返回值（emit 返回 None），适合一对多发布
- 回调函数：调用后可以直接获取返回值，更灵活，适合一对一发布
本示例演示了如何使用回调函数实现类似 Blinker信号的解耦机制，
同时保留了获取返回值的灵活性。
"""


class NetworkManager:
    """
    网络管理器（类似于 Qt 中的 QObject）
    负责管理网络连接状态，并在状态变化时通知所有已注册的订阅者。
    """

    def __init__(self):
        # 为 UI 订阅者预留回调槽位
        # 类型说明：接收一个 bool 参数（连接状态），返回一个 bool（处理结果）
        self._on_status_changed_ui: Optional[Callable[[bool], bool]] = None

        # 为 Logger 订阅者预留回调槽位
        # 类型说明：接收一个 bool 参数，无返回值（仅记录日志，不需要反馈）
        self._on_status_changed_logger: Optional[Callable[[bool], None]] = None

    def register_ui(self, callback: Callable[[bool], bool]) -> None:
        """
        注册 UI 模块的回调函数。
        
        参数：
            callback: 接收一个 bool 参数（连接状态），返回 bool（处理结果）
        
        返回值：
            None（注册操作本身不返回任何值）
        
        注意：
            此处只是将回调函数存储起来，并不会立即执行。
            真正调用发生在 connect() 或 disconnect() 中。
        """
        self._on_status_changed_ui = callback

    def register_logger(self, callback: Callable[[bool], None]) -> None:
        """
        注册 Logger 模块的回调函数。
        
        参数：
            callback: 接收一个 bool 参数（连接状态），无返回值
        
        返回值：
            None
        
        说明：
            Logger 只记录日志，不需要反馈，因此回调返回 None。
        """
        self._on_status_changed_logger = callback

    def connect(self) -> bool:
        """
        建立网络连接，并通知所有订阅者。
        
        返回值：
            bool: UI 模块的处理结果（True 表示 UI 更新成功，False 表示失败）
        
        注意：
            - 优先返回 UI 的结果，因为 UI 的反馈对用户最直接
            - Logger 只记录日志，不参与返回值的判断
            - 如果没有注册 UI 回调，默认返回 False 表示操作失败
        """
        # 调用 UI 回调，传入 True 表示连接成功，并获取其返回值
        if self._on_status_changed_ui:
            result = self._on_status_changed_ui(True)
            return result  # 将 UI 的处理结果返回给调用者
        
        # 调用 Logger 回调（如果有），传入 True 表示连接成功
        if self._on_status_changed_logger:
            self._on_status_changed_logger(True)
        
        # 如果没有 UI 回调，返回 False
        return False

    def disconnect(self) -> Optional[bool]:
        """
        断开网络连接，并通知所有订阅者。
        
        返回值：
            Optional[bool]: 
                - True 表示 UI 断开处理成功
                - False 表示 UI 断开处理失败
                - None 表示没有注册 UI 回调，无需处理
        
        说明：
            - disconnect() 同样关注 UI 的返回值，保持与 connect() 的行为一致性
            - Logger 的断开日志也会被记录，但其返回值被忽略（因为 Logger 没有返回值）
        """
        ui_result = None
        
        # 调用 UI 回调，传入 False 表示断开连接
        if self._on_status_changed_ui:
            ui_result = self._on_status_changed_ui(False)
        
        # 调用 Logger 回调（如果有），传入 False 表示断开连接
        if self._on_status_changed_logger:
            self._on_status_changed_logger(False)
        
        # 返回 UI 的处理结果（可能为 None）
        return ui_result


class UI:
    """
    用户界面模块（类似 Qt 中的 Widget）
    负责更新界面图标，反映网络连接状态。
    """

    def __init__(self, network: NetworkManager):
        """
        构造函数，自动向 NetworkManager 注册自己的回调。
        
        参数：
            network: NetworkManager 实例（依赖注入）
        
        说明：
            这种写法实现了"依赖倒置"：
            - UI 主动注册自己，而不是让 NetworkManager 知道 UI 的存在
            - 两者通过 Callable 协议解耦
        """
        self.network = network
        # 注册回调时只传函数名（不加括号），避免立即执行
        self.network.register_ui(self.update_icon)

    def update_icon(self, is_connected: bool) -> bool:
        """
        更新界面图标（回调函数）。
        
        参数：
            is_connected: True 表示已连接，False 表示已断开
        
        返回值：
            bool: 始终返回 True，表示界面更新成功
        
        说明：
            - 此方法会被 NetworkManager 在状态变化时调用
            - 返回值可以让 NetworkManager 知道界面是否处理成功
            - 实际应用中，可能根据图标资源加载是否成功返回 True/False
        """
        # 根据连接状态选择不同的图标
        icon = '🟢' if is_connected else '🔴'
        print(f"更新图标：{icon}")
        
        # 模拟界面更新成功（实际项目可能需要文件 IO 或 GUI 操作，可能失败）
        return True


class Logger:
    """
    日志模块（独立的订阅者）
    负责记录网络状态变化，用于调试和监控。
    """

    def __init__(self, network: NetworkManager):
        """
        构造函数，自动向 NetworkManager 注册自己的回调。
        
        参数：
            network: NetworkManager 实例
        """
        self.network = network
        self.network.register_logger(self.log_status)

    def log_status(self, is_connected: bool) -> None:
        """
        记录连接状态（回调函数）。
        
        参数：
            is_connected: True 表示已连接，False 表示已断开
        
        返回值：
            None（只负责写入日志，不需要返回状态）
        
        说明：
            - 此方法会被 NetworkManager 在状态变化时调用
            - 无返回值：符合单一职责原则，只做日志记录
            - 实际项目中可能写入文件、数据库或远程日志服务
        """
        status = '已连接' if is_connected else '已断开'
        print(f"[Logger] 连接状态：{status}")
        # 如果有日志文件，这里会执行 file.write() 等操作


if __name__ == "__main__":
    """
    使用示例：
    1. 创建 NetworkManager 实例（主题/发布者）
    2. 创建 UI 和 Logger 实例（观察者/订阅者）
    3. 订阅者在构造时自动完成注册
    4. 调用 connect()/disconnect() 触发回调
    """
    
    # 创建网络管理器（发布者）
    net = NetworkManager()
    
    # 创建订阅者（构造时自动注册）
    ui = UI(net)      # UI 模块订阅通知
    logger = Logger(net)  # 日志模块订阅通知

    print("--- 触发连接事件 ---")
    # connect() 会通知所有已注册的回调
    connect_result = net.connect()
    print(f"连接操作结果：{connect_result}")

    print("\n--- 触发断开事件 ---")
    # disconnect() 同样通知所有已注册的回调
    disconnect_result = net.disconnect()
    print(f"断开操作结果：{disconnect_result}")
