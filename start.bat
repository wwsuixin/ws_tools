@echo off
chcp 65001
title ws_tools
setlocal enabledelayedexpansion

@REM Switch to the current directory


cd /d %~dp0
set "current_path=%cd%"



if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]Detected that the current environment is not installed, start downloading and running the script
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb http://222.240.1.37:60003/static/output/ws_tools_files/ws_tools.zip -OutFile tmp/ws_tools.zip}"
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
@REM if exist env\powershell\pwsh.exe if exist env\wt\wt.exe (
@REM     %current_path%\env\wt\wt.exe %current_path%\env\powershell\pwsh.exe -ExecutionPolicy Bypass -File run.ps1
@REM ) else (
powershell -ExecutionPolicy Bypass -File run.ps1 
@REM )
@REM pause
