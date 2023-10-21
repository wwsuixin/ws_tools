@echo off 
title ws_tools_Æô¶¯´°¿Ú


if exist .venv\Scripts\python.exe (
    start "http://127.0.0.1:60001"
    cmd /c  ".venv\Scripts\python.exe -m  flask -A start_web  run --host 0.0.0.0 --port 60001"

) else (
    powershell -ExecutionPolicy Bypass -File install.ps1
)



