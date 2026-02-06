@echo off
echo MSVC Portable： https://github.com/Delphier/MSVC

set ROOT=%~dp0

set MSVC_VERSION=14.40.33807
set MSVC_HOST=Hostx64
set MSVC_ARCH=x64
set SDK_VERSION=10.0.26100.0
set SDK_ARCH=x64

set MSVC_ROOT=%ROOT%VC\Tools\MSVC\%MSVC_VERSION%
set SDK_INCLUDE=%ROOT%Windows Kits\10\Include\%SDK_VERSION%
set SDK_LIBS=%ROOT%Windows Kits\10\Lib\%SDK_VERSION%

set VCToolsInstallDir=%MSVC_ROOT%\
set PATH=%MSVC_ROOT%\bin\%MSVC_HOST%\%MSVC_ARCH%;%ROOT%Windows Kits\10\bin\%SDK_VERSION%\%SDK_ARCH%;%ROOT%Windows Kits\10\bin\%SDK_VERSION%\%SDK_ARCH%\ucrt;%PATH%
set INCLUDE=%MSVC_ROOT%\include;%SDK_INCLUDE%\ucrt;%SDK_INCLUDE%\shared;%SDK_INCLUDE%\um;%SDK_INCLUDE%\winrt;%SDK_INCLUDE%\cppwinrt
set LIB=%MSVC_ROOT%\lib\%MSVC_ARCH%;%SDK_LIBS%\ucrt\%SDK_ARCH%;%SDK_LIBS%\um\%SDK_ARCH%

echo 设置Python编译环境变量
echo DISTUTILS_USE_SDK=1跳过自动检测，使用已经设置好的Windows SDK环境
echo set MSSdk=1，旧版Python（如3.8）需要的老式标志，新版随意
set DISTUTILS_USE_SDK=1
set MSSdk=1

echo MSVC及Python环境变量已设置完成

cmd /k echo.