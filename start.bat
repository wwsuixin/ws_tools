@echo off 
cd /d %~dp0
setlocal enabledelayedexpansion
if not exist tmp (
    mkdir tmp
)

if not exist env\python311\python311.exe (
    echo python311��������������,��ʼ����python311.zip
    if not exist tmp\python311.zip (
        curl -L https://git.xfj0.cn/https://github.com/test7911/deployment/releases/download/env/python311.zip -o tmp\python311.zip
        
        if %errorlevel% neq 0 (
            echo �����쳣��������������
            del tmp\python311.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\python311.zip (
        echo ��ѹpython311.zip
        env\bandizip\Bandizip.x64.exe x -target:auto -o:env tmp\python311.zip
        del tmp\python311.zip
    )
)

if not exist env\PowerShell\pwsh.exe (
    echo PowerShell��������������,��ʼ����PowerShell.zip
    if not exist tmp\PowerShell.zip (
        curl -L https://git.xfj0.cn/https://github.com/test7911/deployment/releases/download/env/PowerShell.zip -o tmp\PowerShell.zip
        if %errorlevel% neq 0 (
            echo �����쳣��������������
            del tmp\PowerShell.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\PowerShell.zip (
        echo ��ѹPowerShell.zip
        env\bandizip\Bandizip.x64.exe x -target:auto -o:env tmp\PowerShell.zip
        del tmp\PowerShell.zip
    )
)
if not exist env\java1.8\java.exe (
    echo java1.8��������������,��ʼ����java1.8.zip
    if not exist tmp\java1.8.zip (
        curl -L https://git.xfj0.cn/https://github.com/test7911/deployment/releases/download/202310201038/jre1.8.zip -o tmp\java1.8.zip
        if %errorlevel% neq 0 (
            echo �����쳣��������������
            del tmp\java1.8.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\java1.8.zip (
        echo ��ѹjava1.8.zip
        env\bandizip\Bandizip.x64.exe x -target:auto -o:env tmp\java1.8.zip
        del tmp\java1.8.zip
    )
)

if not exist env\java17\java.exe (
    echo java17��������������,��ʼ����java17.zip
    if not exist tmp\java17.zip (
        curl -L https://git.xfj0.cn/https://github.com/test7911/deployment/releases/download/202310201038/jre17.zip -o tmp\java17.zip
        if %errorlevel% neq 0 (
            echo �����쳣��������������
            del tmp\java17.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\java17.zip (
        echo ��ѹjava17.zip
        env\bandizip\Bandizip.x64.exe x -target:auto -o:env tmp\java17.zip
        del tmp\java17.zip
    )
)

if not exist .venv\Scripts\python.exe (
    set /p install_python=�Ƿ��ʼ������[y/n]
    if "%install_python%"=="y" (
        echo ��װ����
        env\Python311\python311.exe -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
        env\Python311\python311.exe -m pip install pdm 
        env\Python311\python311.exe -m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/
        env\Python311\python311.exe -m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/
        env\Python311\python311.exe -m pdm install
    ) else (
        echo ����װ����
        pause
        exit /b 1
    )
)else (
    start http://127.0.0.1:60001
    .venv\Scripts\python.exe -m  flask -A start_web  run --host 0.0.0.0 --port 60001
)

pause
