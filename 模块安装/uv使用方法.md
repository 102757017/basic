# uv 包管理指南

## 全局/脚本模式

传统 `pip` 风格的工作流，适用于快速测试和脚本开发：

```bash
# 创建虚拟环境（在当前目录生成 .venv 文件夹）
uv venv --python 3.11

# 激活虚拟环境
# Windows (Command Prompt)
.venv\Scripts\activate.bat
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 查看当前项目关联的环境
uv venv --list

# 删除虚拟环境（直接删除 .venv 文件夹）
rm -rf .venv           # macOS / Linux
rmdir /s .venv        # Windows
```

---

## 项目模式

在项目根目录通过 `pyproject.toml` 声明依赖，实现自动化环境管理。

### 初始化项目

#### **1. `uv init --app` - 应用程序项目**

```
uv init --app
```

用于创建**可执行的应用程序/脚本项目**。

> ⚠️ **警告**：`uv init --app` **会静默覆盖**已存在的 `main.py` 文件，**务必在空目录中执行**！

**生成的结构：**
```
myapp/
├── pyproject.toml    # 依赖声明
├── uv.lock          # 精确锁文件（跨平台）
├── README.md        # 说明文档
├── .gitignore       # Git 忽略文件
└── main.py          # ⭐ 程序入口文件
```

**依赖管理：**

```bash
#Windows 下，硬链接无法跨卷（跨磁盘分区）创建，要使用硬链接需要将缓存目录设置到与项目相同的磁盘分区
#也可以直接设置 UV_LINK_MODE=copy 环境变量，强制 uv 使用复制模式
set UV_CACHE_DIR=E:\uv-cache

# 添加依赖（自动更新 pyproject.toml + uv.lock）
uv add requests

#这个命令会自动在 pyproject.toml 中生成正确的 [[tool.uv.index]] 和 [tool.uv.sources] 配置。
uv add paddlepaddle==3.0.0.dev20250426 --index paddle-nightly=https://www.paddlepaddle.org.cn/packages/nightly/cpu/

#反向显示依赖树
uv tree --invert --package opencv-python-headless

# 删除依赖（自动更新 pyproject.toml + uv.lock）
uv remove requests

# 将 requirements.txt 的依赖添加到项目
uv add -r requirements.txt

# 添加开发依赖，这些包只在写代码、测试时用，线上运行不需要
uv add --dev pytest ruff

# 删除开发依赖
uv remove --dev pytest
```

**运行项目：**
```bash
# 在虚拟环境中执行命令（自动管理环境）
uv run python main.py

# 运行测试
uv run pytest

# 进入虚拟环境交互式 Shell
uv shell
```

**环境同步：**
```bash
# 根据 pyproject.toml/uv.lock 同步虚拟环境，clone的项目可以用它来恢复环境
uv sync
```

### `pyproject.toml`手动修改后的工作流

```
# 1. 手动编辑 pyproject.toml

uv sync    # uv sync 会自动检查 pyproject.toml 变化，相当于 uv lock + uv sync
```



### 导出requirements.txt

```
# 从当前项目导出（使用 uv.lock）
uv export > requirements.txt

# 导出生产依赖（不含开发依赖）
uv export --no-dev > requirements.txt
```

### 核心文件说明

| 文件             | 用途                                     | 是否手动编辑     |
| ---------------- | ---------------------------------------- | ---------------- |
| `pyproject.toml` | 声明**直接依赖**的版本范围               | ✅ 是             |
| `uv.lock`        | 锁定**所有依赖**的精确版本（含传递依赖） | ❌ 否（自动生成） |
| `.venv/`         | 虚拟环境目录（自动创建）                 | ❌ 否             |

---

### 项目模式最佳实践

```bash
# 1. 新项目：始终在新目录中初始化
mkdir my-project && cd my-project
uv init --app

# 2. 添加依赖
uv add fastapi uvicorn

# 3. 日常开发（无需手动激活环境）
uv run python main.py

# 4. 提交锁文件到版本控制
git add pyproject.toml uv.lock
git commit -m "Initial project setup"

# 5. 团队协作/部署：一键同步
git clone <repo>
cd <repo>
uv sync  # 自动创建环境 + 安装所有依赖
```

---



### 两种模式对比

| 特性         | 项目模式                     | 全局/脚本模式            |
| ------------ | ---------------------------- | ------------------------ |
| **配置文件** | `pyproject.toml` + `uv.lock` | 无                       |
| **依赖声明** | 声明式（永久记录）           | 命令式（临时）           |
| **环境管理** | 自动创建/同步                | 手动 `uv venv`           |
| **依赖安装** | `uv add`                     | `uv pip install`         |
| **依赖删除** | `uv remove`                  | `uv pip uninstall`       |
| **适用场景** | **正式项目、团队协作**       | **快速测试、一次性脚本** |



## 配置文件

```
[tool.uv]
# 核心：强制 uv 忽略所有包对 opencv-python-headless 的需求
exclude-dependencies = ["opencv-python-headless"]


# 将 PyPI 设为第一个索引，并作为默认索引，explicit = true：表示这个索引只用于pyproject.toml 中明确标记的包
[[tool.uv.index]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
explicit = false

# 将 paddle-nightly 设为第二个索引
[[tool.uv.index]]
name = "paddle-nightly"
url = "https://www.paddlepaddle.org.cn/packages/nightly/cpu/"

# 指定 paddlepaddle 的来源
[tool.uv.sources]
paddlepaddle = { index = "paddle-nightly" }
# paddlex 不需要指定来源，它将从默认的 PyPI 索引获取

[tool.uv]
# 设置全局索引策略，允许跨索引查找最佳匹配
index-strategy = "unsafe-best-match"
# 允许使用预编译的 wheel
compile-bytecode = true
# 指定当前平台为 Windows AMD64
required-environments = [
    "sys_platform == 'win32' and platform_machine == 'AMD64'"
]
```



# 让双击 `.py` 文件自动激活项目虚拟环境启动 IDLE

```
@echo off
setlocal enabledelayedexpansion

:: 获取双击的文件完整路径（可能含空格）
set "PYFILE=%~1"
if "%PYFILE%"=="" (
    echo 请将.py文件拖拽到此脚本上
    pause
    exit /b
)

:: 获取文件所在目录
set "WORKDIR=%~dp1"
:: 去掉末尾反斜杠
if "%WORKDIR:~-1%"=="\" set "WORKDIR=%WORKDIR:~0,-1%"

:: 切换到该目录（虚拟环境相对路径基于此目录）
pushd "%WORKDIR%"

:: 检测虚拟环境：优先 .venv，其次 venv
set "VENV_DIR="
if exist ".venv\Scripts\python.exe" (
    set "VENV_DIR=.venv"
) else if exist "venv\Scripts\python.exe" (
    set "VENV_DIR=venv"
)

if defined VENV_DIR (
    :: 激活虚拟环境（设置 PATH、VIRTUAL_ENV 等环境变量）
    echo 使用虚拟环境: %VENV_DIR%
    call "%VENV_DIR%\Scripts\activate.bat"

    :: 启动 IDLE（此时 python 已指向虚拟环境的解释器）
    python -m idlelib.idle "%PYFILE%"
) else (
    :: 未找到虚拟环境，使用系统默认 Python
    echo 未找到虚拟环境，使用全局 Python
    python -m idlelib.idle "%PYFILE%"
)

popd
```

