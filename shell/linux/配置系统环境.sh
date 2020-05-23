#查看cpu架构
cat /proc/cpuinfo
#查看内核版本
cat /proc/version

#修改root用户密码
sudo passwd root

#修改host
sudo chmod 777 /etc/hosts
#echo "91.189.88.162 security.ubuntu.com" >> /etc/hosts

#修改DNS服务器为114
sudo chmod 777 /etc/resolv.conf
echo "nameserver 114.114.114.114" > /etc/resolv.conf

#修改DNS服务器为dnsmasq解析，dnsmasq默认监听本机的53端口
sudo chmod 777 /etc/resolv.conf
echo "nameserver 127.0.0.1" > /etc/resolv.conf
#dnsmasq先去解析host文件，再去解析/etc/dnsmasq.d/下的* .conf文件，并且这些文件的优先级要高于dnsmasq.conf，我们自定义的resolv.dnsmasq.conf中的DNS也被称为上游DNS，这是最后去查询解析的；

#测试dnsmasq.conf语法是否有错误
dnsmasq --test

#重载dnsmasq配置文件
service dnsmasq reload

#查看DNS解析情况
nslookup www.baidu.com


#更新软件源list，大坑：必须将卡巴关闭，否则会被拦截
sudo apt-get update

#把本地已安装的软件，与刚下载的软件列表里对应软件进行对比，如果发现已安装的软件版本太低，就会提示你更新
sudo apt-get upgrade

#修改apt软件源为国内源，将/etc/apt/sources.list替换为以下内容
#注意trusty要替换为当前系统的Codename，用lsb_release -a命令可以查看当前系统的Codename
'''
#阿里云
deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
'''
