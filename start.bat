@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM Switch to the current directory
cd /d %~dp0

@REM Set proxy URL
set github_proxy=
echo ---------------------------------------------------
echo 1: https://gh.con.sh/ (recommend)
echo 2: https://gh.ddlc.top/
echo 3: https://dl.ghpig.top/
echo 4: https://slink.ltd/
echo 5: https://git.xfj0.cn/
echo 6: https://gh.h233.eu.org/
echo 7: https://ghps.cc/
echo 8: https://gh-proxy.com/
echo 9: https://hub.gitmirror.com/
set /p user_input=Please enter a number from 1 to 9(default 1): 
if "%user_input%"=="" set user_input=1

if %user_input%==1 set github_proxy=https://gh.con.sh/
if %user_input%==2 set github_proxy=https://gh.ddlc.top/
if %user_input%==3 set github_proxy=https://dl.ghpig.top/
if %user_input%==4 set github_proxy=https://slink.ltd/
if %user_input%==5 set github_proxy=https://git.xfj0.cn/
if %user_input%==6 set github_proxy=https://gh.h233.eu.org/
if %user_input%==7 set github_proxy=https://ghps.cc/
if %user_input%==8 set github_proxy=https://gh-proxy.com/
if %user_input%==9 set github_proxy=https://hub.gitmirror.com/


echo The agent you have chosen is !github_proxy!

echo ---------------------------------------------------



if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]Detected that the current environment is not installed, start downloading and running the script
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !github_proxy!https://github.com/wwsuixin/ws_tools/releases/download/main/ws_tools.zip -OutFile tmp/ws_tools.zip}"
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
    env\powershell\pwsh.exe -ExecutionPolicy Bypass -File run.ps1 !github_proxy!
) else (
    powershell -ExecutionPolicy Bypass -File run.ps1 !github_proxy!
)
exit
