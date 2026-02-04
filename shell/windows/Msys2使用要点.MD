# MSYS2 开发环境配置指南

## ⚠️ 重要警告
**不要随意执行 `pacman -Syu`**  
这会升级整个仓库到最新版本，导致 Python 及工具链都变成最新版本，可能破坏现有环境。

## 一、工具链安装

### 基础编译工具
```bash
pacman -S --noconfirm \
    mingw-w64-x86_64-cmake \
    mingw-w64-x86_64-make \
    mingw-w64-x86_64-gcc \
    mingw-w64-x86_64-g++ \
    mingw-w64-x86_64-ninja \
    mingw-w64-x86_64-pybind11
```

### GObject 和 GLib 相关
```bash
pacman -S mingw-w64-x86_64-gobject-introspection \
          mingw-w64-x86_64-gobject-introspection-runtime \
          mingw-w64-x86_64-glib2
```

### Aravis 相机库
```bash
pacman -S mingw-w64-x86_64-aravis

# 验证安装
python -c "import gi; gi.require_version('Aravis', '0.8'); from gi.repository import Aravis; print('Aravis version:', Aravis.get_version())"
```

## 二、包管理规范

### Python 包管理原则
1. **MSYS2 自带 Python**：使用 `pacman` 安装
   ```bash
   pacman -S mingw-w64-x86_64-python-包名
   ```

2. **定期更新**：
   ```bash
   # 更新整个系统（包括 Python 包）
   pacman -Syu
   ```

3. **⚠️ 兼容性警告**：
   - 避免混合使用 `pip install` 和 `pacman` 安装 Python 包
   - MSYS2 编译的 whl 包使用 GCC 编译器，**不能用于官方 Windows Python**（使用 MSVC 编译器）

### 旧版本 Python 处理
- 离线安装旧版 Python 到 MSYS2 时
- 对旧版本 Python 使用 `pip` 安装库（而非 `pacman`）

## 三、构建配置

### Setuptools 环境变量
新版本 setuptools 会忽略 MSYS2 的 GCC 配置。需设置：
```bash
# 强制使用标准库的 distutils
export SETUPTOOLS_USE_DISTUTILS=stdlib

# 安装 numpy（示例）
pip install numpy==1.24.4 --no-binary numpy
```

### 编译命令差异
- **编译 whl 文件**：
  ```bash
  cd 项目目录
  python setup.py bdist_wheel --plat-name win_amd64
  ```

- **编译 C++ 项目**：
  ```bash
  # MSYS2 使用 mingw32-make，不是 make
  mingw32-make
  ```



## 四、故障排查

### 常见问题
1. **编译器不匹配**：确保使用 MSYS2 GCC 编译的包仅用于 MSYS2 Python
2. **GLib 版本冲突**：检查 `gi.repository` 导入的版本号
3. **构建失败**：确认 `SETUPTOOLS_USE_DISTUTILS=stdlib` 环境变量已设置

### 验证命令
```bash
# 检查 Python 版本和编译器
python -c "import sys; print(sys.version)"
gcc --version

# 检查包是否正常导入
python -c "import gi; print('GObject Introspection available')"
```