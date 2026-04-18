

```
# Get signing keys to verify the new packages, otherwise they will not install
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138

# Add the Buster backport repository to apt sources.list
echo 'deb http://httpredir.debian.org/debian buster-backports main contrib non-free' | sudo tee -a /etc/apt/sources.list.d/debian-backports.list

sudo apt update ; sudo apt install libseccomp2 -t buster-backports
```



"registry-mirrors": [
    "https://cfdkj78k.mirror.aliyuncs.com",
    "https://hub-mirror.c.163.com/",
    "https://reg-mirror.qiniu.com"
  ],



#### 拉取镜像

```
#搜索docker hub上的镜像 
docker search ubuntu

#下载ubuntu官方最新镜像，相当于：docker pull ubuntu:latest
docker pull ubuntu
```



#### 列出本地images

```
docker images
```



#### 单个镜像删除,可以指定IMAGE ID

```
docker rmi ubuntu
```





### 根据Dockerfile构建 Docker 镜像

-t参数用于指定镜像名称和版本号

在Docker中，“/”符号用来表示镜像的命名空间和仓库名称。斜杠前面的部分称为命名空间，通常代表镜像的组织或创建者，而斜杠后面的部分则是仓库的名称或类型。

如果Dockerfile位于当前工作目录，则需要在构建命令末尾加一个"."，以告诉Docker引擎在当前目录中查找Dockerfile，并在其中进行构建。

```
docker build -t raspbian/py:1.0.0 .
```



为了加快 Dockerfile 的构建速度，你可以在构建过程中逐层构建并测试新的镜像层。这样可以让你的构建过程更具可控性，确保每一步都正确无误。

一种方法是，先只构建基础镜像层，然后逐层添加软件包和依赖库。每次添加新的软件包或依赖库后，使用 `docker build` 命令重新构建 Dockerfile，以确保每一步都成功运行。如果有错误或缺失的软件包，Dockerfile 的构建将失败，并提供错误信息。

待所有镜像层都构建成功后，你可以将它们合并到单个镜像层中，以进一步减少镜像层数，并优化镜像构建效率。你可以使用 `RUN` 指令来一次添加多个软件包或依赖库，每个镜像层中添加的软件包和依赖库都需要测试和确认无误。

当你在Dockerfile中安装Python包时，每次修改Dockerfile时都需要重新构建Docker镜像并重新运行pip安装同样的包，这确实会非常耗费时间。为了解决这个问题，可以考虑使用Docker的构建缓存。这样一来，Docker在构建过程中会缓存之前的构建步骤并对它们进行复用，从而避免了重复安装包的过程。

具体来说，你可以使用--cache-from和--target参数指定之前已经构建过的镜像作为缓存源，并将最后构建完成的Docker镜像标记为对应的版本。这样，下次构建Docker镜像时，Docker会根据缓存源对之前的步骤进行复用，只重新运行修改过的步骤，从而大大缩短构建时间。

例子：

```
# 假设之前已经构建过名为 "my-image" 的镜像：
docker build -t raspbian/py:1.0.0 .

# 使用之前的镜像作为缓存源，重新构建
docker build --cache-from raspbian/py:1.0.0 -t raspbian/py:1.0.1 .

# 标记最终构建完成的镜像版本
docker tag py:2.0 py:latest
```

需要注意的是，如果Dockerfile中的步骤有任何更改，之前的缓存源将不再适用，Docker将会重新进行构建并重新安装Python包。





#### 使用Docker 镜像创建并运行一个容器：

- **-d:** 后台运行容器，并返回容器ID；
- **-i:** 以交互模式运行容器，通常与 -t 同时使用；
- **-t:** 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
- **-p:** 指定端口映射，格式为：**主机(宿主)端口:容器端口**
- **--name="nginx-lb":** 为容器指定一个名称；
- **--dns 8.8.8.8:** 指定容器使用的DNS服务器，默认和宿主一致；
- **-h "mars":** 指定容器的hostname；
- **-e username="ritchie":** 设置环境变量；
- **--env-file=[]:** 从指定文件读入环境变量；
- **--net="bridge":** 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；
- **--expose=[]:** 开放一个端口或一组端口；
- **--volume , -v:** 绑定一个卷，如果不使用数据卷(Volume)，容器内运行期间产生的数据在容器关闭后，又回到你启动容器时的原始镜像状态.
- --rm:告诉 Docker 在容器停止后自动删除该容器
- -w:用于设置容器的工作目录
- --entrypoint ：替换docker镜像的入口
- --log-driver=syslog：docker中的日志只能在docker log命令来查看，无法通过2>&1重定向，这个驱动程序允许你将 Docker 容器的日志发送到一个或多个目标，从而重定向日志。

这里的容器暴露了两个端口

6080：是web版的vnc，可以在浏览器上直接访问桌面环境,http://127.0.0.1:6080

5900：是使用客户端工具连接的端口

VNC_PASSWORD:远程桌面登录的密码

-v E:/Linux:/mnt/sda1:将 E:\Linux 挂载到 /mnt/sda1 上

:cached 添加缓存，否则读写共享volume的速度极慢

```
docker run -p 6080:80 -p 5900:5900 -e VNC_PASSWORD=password -v E:/Linux:/mnt/sda1 dorowu/ubuntu-desktop-lxde-vnc

docker run -i -t -v E:/Linux:/mnt/sda1:cached ubuntu /bin/bash
docker run -i -t -v E:/Linux:/mnt/sda1:cached f6c402ac9ef0 /bin/bash
docker run -i -t --rm -v /home/pi/etf:/etf -w /etf --name="py" raspbian/py:1.0.0 main.py

docker run -i -t --rm \
  -v /home/pi/pythonapp:/home/pi/pythonapp \
  -w /home/pi/pythonapp/kezhuanzhai \
  --name="py" \
  raspbian/py:1.0.0 \
  kzz.py

#忽略dockerfile内的entrypoint,直接进入bash
docker run -i -t --rm \
  --entrypoint /bin/bash \
  -v /home/pi/pythonapp:/home/pi/pythonapp \
  -w /home/pi/pythonapp/kezhuanzhai \
  --name="py" \
  raspbian/py:1.0.0
```

**注意：在crontab中执行该脚本不能使用交互模式，否则会导致计划任务执行失败，需要删除-t**



#### 列出所有在运行的容器信息。

```
docker ps
```

对于已退出的容器，可以使用如下命令进行查看

```
docker ps -a
```



### 启动一个已经创建过的容器

`docker start` 命令用于启动已经停止的容器。在命令行中，你只需要输入以下命令：

启动 Docker 容器时，可以使用 `--workdir` 或 `-w` 参数来指定容器内的工作目录

```
docker start -w /path/to/workdir <container-name>
```

其中，OPTIONS 包括一些可选参数，例如 `-a` 表示启动容器并附加到容器的标准输出、错误输出，以便实时查看容器的运行情况；`-i` 表示启动容器并进入交互模式。

CONTAINER 是需要启动的容器的名称或 ID。例如，运行以下命令将启动名为 "my_container" 的容器：

```
docker start my_container
```

如果你想启动并附加到容器的标准输出、错误输出，可以使用以下命令：

```
docker start -a my_container
```

如果你想进一步交互式地操作容器，可以使用以下命令：

```
docker start -i my_container
```

这将启动容器并进入交互模式，让你能够与容器进行交互操作。





#### 打开运行的容器

9df70f9a0714 是容器 ID。

```
docker exec -it 5638926aa1bc /bin/bash
```

如果容器内已经定义了CMD ["python", "main.py"]，那么在运行容器时，容器会自动执行这个命令，启动Python应用程序。如果你需要进入容器并执行其他命令，可以使用docker exec命令。在终端中输入以下命令：

```
docker exec -it <container-name> /bin/bash
```

这个命令会打开一个新的交互式终端，你可以在里面执行其他命令。其中，<container-name>是指定容器的名称或ID，/bin/bash是执行的命令。你也可以使用其他的命令，只要容器内有该命令即可。例如，如果你需要在容器内执行ls命令，可以使用以下命令：

```
docker exec -it <container-name> ls
```

这个命令会在容器内执行ls命令并返回结果。注意，使用docker exec命令时，容器必须处于运行状态。





#### 查看docker中的输出

```
docker logs -f 5638926aa1bc
```





#### 删除一个或多个容器

```
docker rm -f db01
```



#### 一条命令实现停用并删除所有容器

```
docker stop $(docker ps -q) & docker rm $(docker ps -aq)
```













