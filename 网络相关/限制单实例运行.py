import socket
import sys
import time
import atexit

# 这种方法通过尝试在本地绑定并监听一个特定的、不常用的TCP端口来实现单例。如果绑定成功，说明端口可用，脚本可以运行；如果绑定失败，则说明该端口已被另一个实例占用，当前实例应该退出。
# 建议选择一个高端口号（如 49152-65535），避免与常用服务冲突
SINGLE_INSTANCE_PORT = 54321
SINGLE_INSTANCE_HOST = '127.0.0.1' # 本地回环地址

class SingleInstancePort:
    def __init__(self):
        self.sock = None
        self._acquire_lock()

    def _acquire_lock(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socket.SO_REUSEADDR，因为它允许端口重用，与单例需求冲突
            # 我们希望的是独占端口，而非允许重用。

            self.sock.bind((SINGLE_INSTANCE_HOST, SINGLE_INSTANCE_PORT))
            # 关键步骤：将 socket 置于监听状态，使其独占端口
            # 参数 1 是 backlog 大小，表示在拒绝连接之前可以排队的连接数量。
            # 这里我们不需要接受连接，只是为了独占端口。
            self.sock.listen(1)
            
            print(f"成功绑定并监听端口 {SINGLE_INSTANCE_HOST}:{SINGLE_INSTANCE_PORT}，获取实例锁。")
            # 注册清理函数，确保在脚本退出时关闭socket
            atexit.register(self._release_lock)
        except OSError as e:
            # 端口被占用时会抛出 "Address already in use" 错误
            if "Address already in use" in str(e):
                print(f"错误：端口 {SINGLE_INSTANCE_PORT} 已被占用，可能已有实例在运行。")
                print(f"详细错误：{e}")
                sys.exit(1) # 退出当前实例
            else:
                # 其他 socket 相关的错误
                print(f"错误：无法绑定到端口 {SINGLE_INSTANCE_PORT}：{e}")
                sys.exit(1)

    def _release_lock(self):
        if self.sock:
            print(f"关闭端口 {SINGLE_INSTANCE_PORT}，释放实例锁。")
            self.sock.close()
            self.sock = None

# --- 主逻辑开始 ---
if __name__ == '__main__':
    # 在脚本最开始创建 SingleInstancePort 类的实例
    # 这一步将尝试获取锁，如果失败，则脚本会退出
    singleton_port = SingleInstancePort()

    print("脚本启动成功，正在运行...")
    print("-------------------------")
    print("这里是你的主要程序逻辑。")
    print("例如：")
    for i in range(10): # 延长运行时间，方便测试
        print(f"执行任务 {i+1}...")
        time.sleep(1)
    print("-------------------------")
    print("脚本执行完毕。")

    # 当脚本正常退出时，atexit 注册的 _release_lock 会被调用，关闭 socket。
    # 如果脚本被强制杀死，操作系统也会自动释放端口。
