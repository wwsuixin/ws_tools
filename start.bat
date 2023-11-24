@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM Switch to the current directory
cd /d %~dp0

@REM Set proxy URL
set http_proxy=https://gh.con.sh
@REM set http_proxy=https://download.nuaa.cf
@REM set http_proxy=https://download.njuu.cf
@REM set http_proxy=https://dl-slb.ghpig.top
@REM set http_proxy=https://mirror.ghproxy.com
@REM set http_proxy=https://gh-proxy.com
@REM set http_proxy=https://ghproxy.net

if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]Detected that the current environment is not installed, start downloading and running the script
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !http_proxy!/https://github.com/wwsuixin/ws_tools/releases/download/main/ws_tools.zip -OutFile tmp/ws_tools.zip}"
    powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'tmp\ws_tools.zip' -DestinationPath './' -Force"
)

if not exist w_version.txt (
    echo [-]Network environment abnormal, please check the network......
    echo [!]Please manually modify the ninth line of the script, replacing http_proxy with another proxy URL
    pause
    exit
)
if exist tmp\ws_tools.zip (
    del tmp\ws_tools.zip
)
if exist env\powershell\pwsh.exe (
    env\powershell\pwsh.exe -ExecutionPolicy Bypass -File run.ps1 !http_proxy!
) else (
    powershell -ExecutionPolicy Bypass -File run.ps1 !http_proxy!
)
exit
