# -*- coding: UTF-8 -*-
import toml
import os

# 定义配置文件名
config_file = "setting.toml"

# --- 1. 模拟初始配置文件内容 (如果文件不存在，先创建它) ---
initial_config = {
    "server": {
        "host": "localhost",
        "port": 8080,
        "enabled": True
    },
    "database": {
        "type": "postgres",
        "host": "db.example.com",
        "port": 5432,
        "username": "admin"
    },
    "log_level": "INFO",
    "features": ["email_notifications", "dashboard_analytics"]
}

print(f"--- 1. 写入初始配置到 '{config_file}' ---")
try:
    with open(config_file, "w", encoding="utf-8") as f:
        toml.dump(initial_config, f)
    print("初始配置已成功写入。")
except Exception as e:
    print(f"写入初始配置失败: {e}")
    exit() # 如果初始写入失败，后续操作无意义








# --- 2. 从 'setting.toml' 读取配置 ---
print(f"\n--- 2. 从 '{config_file}' 读取配置 ---")
config = {} # 初始化一个空字典
try:
    # 推荐的修改：使用文本模式 'r' 并指定编码
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    
    print("成功读取到的配置 (Python 字典格式):")
    print(config)
    port=config['server']['port']
    print(f"当前服务器端口: {port}")
except FileNotFoundError:
    print(f"错误: 文件 '{config_file}' 不存在。")
except Exception as e:
    print(f"读取配置失败: {e}")


# --- 3. 修改 'setting.toml' 配置 ---
# 修改现有值
config['server']['port'] = 8081  # 将端口从 8080 修改为 8081
# 添加新的键值对
config['server']['timeout'] = 60 # 为 server 添加一个新的超时设置



# --- 4. 将修改后的配置写回 'setting.toml' 文件 ---
print(f"\n--- 4. 将修改后的配置写回 '{config_file}' ---")
if config: # 确保有配置可写
    try:
        # 使用 'w' 模式会覆盖文件原有内容
        with open(config_file, "w", encoding="utf-8") as f:
            toml.dump(config, f)
        print("修改后的配置已成功写回。")
    except Exception as e:
        print(f"写回修改后的配置失败: {e}")
else:
    print("没有配置数据可以写回文件。")


