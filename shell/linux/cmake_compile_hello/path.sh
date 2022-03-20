echo 当前工作路径：$(pwd)
echo 当前脚步所在的目录:$(cd $(dirname $0) && pwd)
dir=$(cd $(dirname $0) && pwd)
echo 当前脚本所在目录的子目录："$dir"/child