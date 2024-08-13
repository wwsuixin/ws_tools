@echo off
chcp 936
title ws_tools
setlocal enabledelayedexpansion

@REM Switch to the current directory
cd /d %~dp0
set "current_path=%cd%"

echo 该脚本仅用于服务无法启动时进行核心程序重装,没啥影响,放心装
choice /C YN /M "是否开始[Y/N]:"
if errorlevel 2 (
    echo [-]安装已取消
    exit
)
taskkill /IM wt.exe /F
taskkill /IM powershell.exe /F
taskkill /IM python.exe /F
@REM 删除.venv、start_web、pyproject.toml等目录

del .venv/w_version.txt
del w_version.txt
del start.bat
del run.ps1

curl -o start.bat https://gitee.com/wwsuixin/w_nav/raw/master/ws_tools/start.bat & start /b start.bat

echo 等待上述脚本完成后,重新运行start.bat
pause
