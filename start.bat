@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM 切换到当前目录
cd /d %~dp0

@REM 设置代理url
set http_proxy=https://gh.h233.eu.org/
if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]检测到当前环境还未安装, 开始下载运行脚本
    choice /C YN /M "询问是否开始安装Y继续，回N退出:"
    if errorlevel 2 (
        echo [-]安装已取消
        exit
    )
    echo [-]开始下载运行脚本
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !http_proxy!/https://github.com/wwsuixin/ws_tools/releases/download/main/ws_tools.zip -OutFile tmp/ws_tools.zip}"
    @REM 解压ws_tools.zip到指定文件夹
   @REM 覆盖解压ws_tools.zip到指定文件夹
   powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'tmp\ws_tools.zip' -DestinationPath './' -Force"
)

if not exist w_version.txt (
    echo [-]网络环境异常,请检查网络......
    pause
    exit
)
@REM 删除tmp/ws_tools.zip
if exist tmp\ws_tools.zip (
    del tmp\ws_tools.zip
)

powershell -ExecutionPolicy Bypass -File run.ps1 !http_proxy!