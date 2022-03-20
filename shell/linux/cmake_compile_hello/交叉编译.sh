sudo apt-get upgrade
sudo apt-get install mingw-w64 mingw-w64-tools mingw-w64-i686-dev mingw-w64-x86-64-dev zlib1g-dev libsdl2-dev libjpeg-dev

echo cmake不支持中文路径，该文件需要放到英文路径下运行
echo 切换到当前脚本所在的目录
script_dir=$(cd $(dirname $0) && pwd)
echo "$script_dir"
cd "$script_dir"

# cmake命令生成makefile文件,也可以用cmake-gui生成
# -B 指定编译文件的build目录，会在build目录生成makefile文件
# -S 指定CMakeLists.txt所在的目录
# -G指定generator，可选“Ninja”、“Visual Studio 16 2019”等
cmake . -B "$script_dir"/build_cross -DCMAKE_TOOLCHAIN_FILE="$script_dir"/tool.make -G "Unix Makefiles"

# 切换到makefile文件所在的目录执行编译命令
cd  "$script_dir"/build_cross
make