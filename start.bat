@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM Switch to the current directory
cd /d %~dp0


echo .
echo "                      _              _         "
echo "     __      _____   | |_ ___   ___ | |___     "
echo "     \ \ /\ / / __|  | __/ _ \ / _ \| / __|    "
echo "      \ V  V /\__ \  | || (_) | (_) | \__ \    "
echo "       \_/\_/ |___/___\__\___/ \___/|_|___/    "
echo "                 |_____|   version:20240319    "
echo .

if not exist tmp (
    mkdir tmp
)

@REM if not exist env/github_download/github_download.exe (
@REM     echo [-]Project code exception, please download again: https://github.com/wwsuixin/ws_tools
@REM     pause
@REM     exit
@REM )

if not exist w_version.txt (
    echo [-]Detected that the current environment is not installed, start downloading and running the script
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb http://222.240.1.20:60003/static/output/ws_tools_files/ws_tools.zip -OutFile tmp/ws_tools.zip}"
    @REM start /B  /WAIT env/github_download/github_download.exe -i http://222.240.1.20:60003/static/output/ws_tools_files/ws_tools.zip -o tmp/ws_tools.zip
    powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'tmp\ws_tools.zip' -DestinationPath './' -Force"
)

if not exist w_version.txt (
    echo [-]Network environment abnormal, please check the network......
    pause
    exit
)
if exist tmp\ws_tools.zip (
    del tmp\ws_tools.zip
)
if exist env\powershell\pwsh.exe (
    env\powershell\pwsh.exe -ExecutionPolicy Bypass -File run.ps1
) else (
    powershell -ExecutionPolicy Bypass -File run.ps1 
)
exit
