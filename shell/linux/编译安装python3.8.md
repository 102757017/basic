升级系统

```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install bluetooth libbluetooth-dev libreadline-dev libncurses-dev build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev python3 python3-dev python3-venv python3-pip libffi-dev libtiff-dev autoconf libopenjp2-7 python3-pip libglib2.0-dev -y
sudo pip3 install pybluez
```



编译安装sqlite

若不安装sqlite，python3.8的sqlite3库会出现导入错误的情况

```
wget https://www.sqlite.org/2018/sqlite-autoconf-3240000.tar.gz
tar -xvzf sqlite-autoconf-3240000.tar.gz
cd sqlite-autoconf-3240000/
./configure
make -j4
sudo make install
```



安装pyenv

```
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```

修改pi用户的环境变量，在~/.bashrc文件中增加3行内容

export PATH="/home/pi/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

```
sudo sed -i '$a export PATH="/home/pi/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"' ~/.bashrc
```

pyenv命令

```
#显示可以安装的环境
pyenv install --list

#安装python3.8.8
pyenv install -v 3.8.8

#显示系统上可用的环境
pyenv versions

#将3.8.8设置为全局环境，在所有shell窗口中都生效。
pyenv global 3.8.8

#创建一个python3.8.8的虚拟环境，名称是hass，其中的库是隔离的，不影响其它python3.8的环境
pyenv virtualenv 3.8.8 hass

#在当前文件夹将3.8.8设置为本地环境，那么 local 命令和刚才有啥不同呢。如果你执行：ls -al，你就会发现，在目录下，有个隐藏文件 .python-version，你可以看到这个文件里面，只写了一句话 my-env，这样你只要进入本路径，就会自动激活虚拟环境
pyenv local hass

#激活环境
pyenv activate hass

#修改环境变量
export PATH="${PATH}:/home/pi/.pyenv/versions/hass/bin/"
```

编译安装python3.8

altinstall 与 install 的区别在于，altinstall 跳过创建Python链接和手册页链接，它安装后可以与树莓派自带的 Python3.7 共存，不会出现冲突和替换

```
wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz 
tar xzvf Python-3.8.6.tgz
cd Python-3.8.6
./configure --prefix=/home/pi/software/python3.8
sudo make altinstall
sudo apt -y autoremove
cd
sudo rm -r Python-3.8.6
sudo rm Python-3.8.6.tgz
```

这时候执行 python 或者 python3.8 都没法启动它(如果没有指定 –prefix 的话，是安装到系统路径，直接执行 python3.8 即可)

需要编辑 `~/.bashrc` 文件，在最下面添加

```
export $PATH:/home/pi/software/python3.8/bin
```
