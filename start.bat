@echo off 

setlocal enabledelayedexpansion
title ws_tools

@REM ???????
cd /d %~dp0

@REM ????url
set http_proxy=https://gh.con.sh

:func
if exist .venv\Scripts\python.exe (
    start chrome "http://127.0.0.1:60001"
    cmd /c  ".venv\Scripts\python.exe -m  flask -A start_web  run --host 0.0.0.0 --port 60001"
    exit
) else (
    @REM ?while??????

    if not exist install.ps1 (
        set /p yn=[-]???????????,??????????[y/n]:
        @REM ??????
        if  not "!yn!" == "y" (
            echo [-] ?????
            pause
            exit
        )
        echo [+] ????????
        powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !http_proxy!/https://github.com/wwsuixin/ws_tools/raw/main/install.ps1 -OutFile install.ps1}"

    ) else (
        set /p yn=[+]???????,??????[y/n]:
        if  not "!yn!" == "y" (
            echo [-] ?????
            pause
            exit
        )
        echo [+] ????
        powershell -ExecutionPolicy Bypass -File install.ps1 !http_proxy!

    )
)
goto func

pause