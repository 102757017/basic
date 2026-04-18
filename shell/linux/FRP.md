

安装

```
!wget https://github.com/fatedier/frp/releases/download/v0.62.1/frp_0.62.1_linux_amd64.tar.gz
!tar -zxvf frp_0.62.1_linux_amd64.tar.gz
```





设置

```
%cd /kaggle/working/frp_0.62.1_linux_amd64

# 1. 从 Kaggle User Secrets 获取密码（安全）
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
frp_token = user_secrets.get_secret("frp_password")  # 假设你在 Secrets 中存了这个键

# 2. 构建配置内容（使用获取到的密码）
config_content = f"""
serverAddr = "ddns.sunnyho.eu.org"
serverPort = 7000
auth.token = "{frp_token}"

[[proxies]]
name = "rdp"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3389
remotePort = 7001
"""

# 3. 写入文件
with open("frpc.toml", "w") as f:
    f.write(config_content)
```



启动

```
# 给客户端程序添加执行权限（如果还没加）
!chmod +x frpc

# 前台启动测试（推荐先这样测试，方便看日志）
!./frpc -c frpc.toml

'''
import subprocess
import os

process = subprocess.Popen(
    ["./frpc", "-c", "frpc.toml"],
    stdout=open("frpc.log", "w"),
    stderr=subprocess.STDOUT,
    start_new_session=True,   # 脱离终端，类似 nohup
)

print(f"FRP 客户端已启动，PID = {process.pid}")

'''
```

