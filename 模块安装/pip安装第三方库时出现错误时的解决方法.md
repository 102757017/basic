# 缺少C++编译器/缺少MinGW编译器的解决方案有以下几种：

## 1.安装对应版本的C++编译器

对于使用VC ++作为默认值的mingw32和packages：

pip install --global-option build_ext --global-option --compiler=mingw32 <package_zip>



对于使用mingw32作为默认值的WinPython上的Visual C ++：
pip install --global-option build_ext --global-option --compiler=msvc <package_zip>



## 2.安装预编译的whl格式模块（依赖的子模块肯能会报同样的错误）

到以下网站下载编译好的模块
https://www.lfd.uci.edu/~gohlke/pythonlibs/
https://pypi.tuna.tsinghua.edu.cn/simple/

先安装wheel模块
pip install wheel

再安装目标模块
pip install XXXXX.whl



## 3.安装exe格式（依赖的子模块不会自动安装，需要手动安装）

