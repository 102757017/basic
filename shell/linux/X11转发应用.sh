#!/bin/bash

# 更新软件包列表并安装必要组件
sudo apt update
sudo apt install -y x11-apps xauth
sudo apt-get install -y libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xfixes0 libxcb-xkb1 \
    libxkbcommon-x11-0 libgl1-mesa-dri libgl1-mesa-glx libglu1-mesa

# 备份并配置 SSH 以允许 X11 转发
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo sed -i 's/^X11Forwarding no/X11Forwarding yes/' /etc/ssh/sshd_config
sudo sed -i 's/^#X11Forwarding yes/X11Forwarding yes/' /etc/ssh/sshd_config

# 设置 X11UseLocalhost 为 no
if grep -q '^X11UseLocalhost' /etc/ssh/sshd_config; then
    sudo sed -i 's/^X11UseLocalhost.*/X11UseLocalhost no/' /etc/ssh/sshd_config
else
    echo 'X11UseLocalhost no' | sudo tee -a /etc/ssh/sshd_config
fi

# 重启 SSH 服务
sudo service ssh restart

# 设置 DISPLAY 环境变量（可选，某些场景需要）
export DISPLAY=localhost:10.0

# 安装 uv 并使用清华源安装 isat-sam
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple
uv pip install isat-sam --system

# 运行 isat-sam
isat-sam