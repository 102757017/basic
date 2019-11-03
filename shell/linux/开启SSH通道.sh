# 1.安装ssh
apt-get install openssh-server

# 2.修改配置文件
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
vim /etc/ssh/sshd_config
#=======(修改以下选项内容)=========#
# Port 23（22端口已被占用）        #
# (取消注释)ListenAddress 0.0.0.0 #
# PermitRootLogin yes            #
# （注释）StrictModes yes         #
# PasswordAuthentication yes     #
#================================#


# 3.启动ssh
service ssh start

# 4.如果提示“sshd error: could not load host key”，则用下面的命令重新生成
rm /etc/ssh/ssh*key
dpkg-reconfigure openssh-server
