# uv 包管理指南

## 安装

```
curl -fsSL https://pixi.sh/install.sh | sh
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```



## 全局/脚本模式

传统 `pip` 风格的工作流，适用于快速测试和脚本开发：

```bash
# 创建虚拟环境（在当前目录生成 .venv 文件夹）
pixi init

# 创建虚拟环境（在myworkspace目录生成 .venv 文件夹）
pixi init myworkspace

# 激活虚拟环境
pixi shell

# 查看当前项目关联的环境
pixi info

# 删除虚拟环境（直接删除 .venv 文件夹）
rm -rf .venv           # macOS / Linux

pixi clean  #另一种方法
```

---

## 项目模式

在项目根目录通过 `pyproject.toml` 声明依赖，实现自动化环境管理。

### 初始化项目

#### **1. `pix init --myworkspace` - 应用程序项目**

```
pix init --myworkspace
```

```
myworkspace
├── .gitattributes
├── .gitignore
└── pixi.toml
```



```
#使用nano配置镜像源
pixi config edit

#列出 Pixi 的全局配置
pixi config list

#这个详细的 Info 命令会显示 Pixi 在启动时加载了哪些配置文件，帮助判断全局配置是否生效
pixi info -vvv
```



**依赖管理：**

```bash
#Windows 下，硬链接无法跨卷（跨磁盘分区）创建，要使用硬链接需要将缓存目录设置到与项目相同的磁盘分区
#也可以直接设置 UV_LINK_MODE=copy 环境变量，强制 uv 使用复制模式
set UV_CACHE_DIR=E:\uv-cache

# 添加依赖（自动更新 pixi.toml + pixi.lock）
pixi add ros-jazzy-desktop -vvv

#使用pypi源安装，默认使用uv进行管理
pixi add --pypi numpy 

#安装特定平台的依赖["win-64", "linux-64", "osx-64", "osx-arm64"]
pixi add --platform linux-64 tree

#把依赖分组，等同与uv里面的group
pixi add --feature numpy

#反向显示依赖树
pixi tree --invert opencv-python-headless

# 删除依赖（自动更新 pyproject.toml + uv.lock）
pixi remove requests

# 全局工具模式,安装在独立环境中，但是可以全局进行访问
pixi global install cowpy
pixi global list
pixi global update <tool>
pixi global uninstall <tool>
```

**运行项目：**
```bash
# 在虚拟环境中执行命令（自动管理环境）
pixi run python main.py

# 进入虚拟环境交互式 Shell
pixi shell
```

**环境同步：**
```bash
# 根据 pixi.toml/pixi.lock 同步虚拟环境，clone的项目可以用它来恢复环境
pixi install
```

### `pixi.toml`手动修改后的工作流

```
# 1. 手动编辑 pixi.toml

pixi sync    # uv sync 会自动检查 pyproject.toml 变化，相当于 uv lock + uv sync
```



### 项目模式最佳实践

```bash
# 1. 新项目：始终在新目录中初始化
mkdir my-project && cd my-project
pixi init

# 2. 添加依赖
pixi add fastapi uvicorn

# 3. 日常开发（无需手动激活环境）
pixi run python main.py

```

---





## pixi.toml 项目配置文件

```
[workspace]
Pixi 有一个内置的规则，默认将 https://conda.anaconda.org/ 作为主机地址拼接出最终url，
下面的channels对应https://conda.anaconda.org/robostack-jazzy与https://conda.anaconda.org/conda-forge
channels = ["robostack-jazzy", "conda-forge"]


#Pixi 采用“先 conda 后 PyPI”的两阶段解析，自动映射可能不正确（例如 conda 包 foo 实际上对应 PyPI 包 bar），这时就必须手动映射
[conda-pypi-map]
"conda包名" = "pypi包名"   # 自定义映射
```





## config.toml 全局配置文件

```
# [concurrency]
# downloads = 12

[pypi-config]
extra-index-urls = [
  "http://mirrors.baidubce.com/pypi/simple/",
  "https://pypi.tuna.tsinghua.edu.cn/simple",
  "https://pypi.org/simple",
]
index-url = "https://mirrors.aliyun.com/pypi/simple"
# can be "subprocess" or "disabled"
# keyring-provider = "subprocess"

[mirrors]
"https://conda.anaconda.org/bioconda" = [
  "https://mirrors.nju.edu.cn/anaconda/cloud/bioconda",
  "https://mirrors.ustc.edu.cn/anaconda/cloud/bioconda",
]
"https://conda.anaconda.org/conda-forge" = [
  "https://mirrors.nju.edu.cn/anaconda/cloud/conda-forge",
  "https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge",
]
"https://conda.anaconda.org/pytorch" = [
  "https://mirrors.nju.edu.cn/anaconda/cloud/pytorch/",
  "https://mirrors.ustc.edu.cn/anaconda/cloud/pytorch",
]
"https://repo.anaconda.com/pkgs/main" = [
  "https://mirrors.nju.edu.cn/anaconda/pkgs/main",
  "https://mirrors.ustc.edu.cn/anaconda/pkgs/main",
]
"https://repo.anaconda.com/pkgs/msys2" = [
  "https://mirrors.nju.edu.cn/anaconda/pkgs/msys2",
  "https://mirrors.ustc.edu.cn/anaconda/pkgs/msys2",
]
"https://repo.anaconda.com/pkgs/r" = [
  "https://mirrors.nju.edu.cn/anaconda/pkgs/r",
  "https://mirrors.ustc.edu.cn/anaconda/pkgs/r",
]
```



## conda镜像源测试脚本

```
%%bash
#!/bin/bash
# ============================================
# Conda 镜像源可用性测试脚本（可靠版）
# 特点：
#   - 严格检测 HTTP 状态码（必须 200）
#   - 多路径测试，防止误判
#   - 自动筛选真正可用的最快源
#   - 输出详细测试结果
# ============================================

# 检查必要命令
for cmd in curl bc awk sort; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ 缺少命令: $cmd，请先安装（例如 apt install curl bc gawk）"
        exit 1
    fi
done

# 镜像源列表 (名称|base_url)
mirror_sources=(
    "清华大学|https://mirrors.tuna.tsinghua.edu.cn/anaconda"
    "中科大|https://mirrors.ustc.edu.cn/anaconda"
    "阿里云|https://mirrors.aliyun.com/anaconda"
    "北京外国语大学|https://mirrors.bfsu.edu.cn/anaconda"
    "上海交通大学|https://mirrors.sjtug.sjtu.edu.cn/anaconda"
    "南京大学|https://mirrors.nju.edu.cn/anaconda"
)

# 测试路径（标准 Conda 索引文件，若镜像站支持应当返回 200）
paths=(
    "pkgs/main/linux-64/repodata.json"
    "cloud/conda-forge/linux-64/repodata.json"
    "cloud/bioconda/linux-64/repodata.json"
)

# 测试单个镜像源
test_mirror() {
    local name="$1"
    local base_url="$2"
    local total_time=0
    local success=0
    local -a success_times=()

    echo -n "▶ 测试 $name ... "

    for path in "${paths[@]}"; do
        local url="${base_url}/${path}"
        # 获取 HTTP 状态码和总耗时
        local output
        output=$(curl -o /dev/null -s -w '%{http_code} %{time_total}' \
            --connect-timeout 3 --max-time 5 "$url" 2>/dev/null)
        local http_code="${output%% *}"
        local time="${output##* }"

        # 只有状态码为 200 才算成功
        if [[ "$http_code" == "200" ]]; then
            if [[ "$time" =~ ^[0-9.]+$ ]] && (( $(echo "$time > 0" | bc -l) )); then
                total_time=$(echo "$total_time + $time" | bc -l)
                ((success++))
                success_times+=("$time")
            fi
        fi
    done

    if [ $success -gt 0 ]; then
        local avg=$(echo "scale=3; $total_time / $success" | bc -l)
        echo "✅ 可用 ($success/${#paths[@]}) | 平均耗时 ${avg}s"
        # 返回结果行（用于排序）
        echo "${avg}|${name}|${base_url}|${success}"
    else
        echo "❌ 不可用 (所有路径返回非200或超时)"
        echo "inf|${name}|${base_url}|0"
    fi
}

# 主流程
echo "========================================"
echo "  Conda 镜像源测速（可靠版）"
echo "  测试平台: Linux-64"
echo "  超时设置: 每个请求最多 5 秒"
echo "  状态码要求: HTTP 200"
echo "  开始时间: $(date)"
echo "========================================"
echo ""

declare -a results=()

for mirror in "${mirror_sources[@]}"; do
    IFS='|' read -r name base_url <<< "$mirror"
    result_line=$(test_mirror "$name" "$base_url" | tail -1)
    results+=("$result_line")
    sleep 0.2   # 避免并发过多
done

echo ""
echo "========================================"
echo "           测速结果汇总"
echo "========================================"

declare -a good=()
for res in "${results[@]}"; do
    IFS='|' read -r avg name base_url success <<< "$res"
    if [[ "$avg" != "inf" ]]; then
        good+=("$res")
        printf "  %-16s 成功路径: %d/%d, 平均耗时: %s 秒\n" "$name" "$success" "${#paths[@]}" "$avg"
    else
        printf "  %-16s 不可用\n" "$name"
    fi
done

# 推荐最快的可用源
if [ ${#good[@]} -gt 0 ]; then
    # 按平均耗时升序排序
    IFS=$'\n' sorted=($(sort -n <<<"${good[*]}"))
    best="${sorted[0]}"
    IFS='|' read -r best_avg best_name best_url best_success <<< "$best"
    echo ""
    echo "================== 🏆 推荐结果 =================="
    echo "最快镜像源: $best_name"
    echo "Base URL  : $best_url"
    echo "成功路径  : $best_success/${#paths[@]}"
    echo "平均耗时  : ${best_avg} 秒"
    echo "================================================"
    echo ""
    echo "🎯 使用以下命令配置 Conda："
    cat <<EOF

# 清除原有频道
conda config --remove-key channels

# 添加推荐的镜像源频道
conda config --add channels ${best_url}/pkgs/main
conda config --add channels ${best_url}/pkgs/r
conda config --add channels ${best_url}/pkgs/msys2
conda config --add channels ${best_url}/cloud/conda-forge
conda config --add channels ${best_url}/cloud/bioconda

# (可选) 完全禁用 defaults 频道
conda config --remove channels defaults

# 显示频道地址（便于确认）
conda config --set show_channel_urls yes

EOF
else
    echo ""
    echo "❌ 所有镜像源均测试失败！"
    echo ""
    echo "可能原因及解决方法："
    echo "1. 网络不通 -> ping 8.8.8.8"
    echo "2. DNS 问题 -> nslookup mirrors.tuna.tsinghua.edu.cn"
    echo "3. 防火墙限制 -> 检查出站 HTTPS (443) 端口"
    echo ""
    echo "💡 临时方案：直接使用官方源（速度可能很慢）"
    echo "   conda config --add channels conda-forge"
    echo "   conda config --add channels bioconda"
fi
```

