@echo off
cd /d %~dp0
setlocal enabledelayedexpansion
if not exist tmp (
    mkdir tmp
)

if not exist env\python311\python311.exe (
    echo "python311依赖环境不存在,开始下载python311.zip"
    if not exist tmp\python311.zip (
        curl -L https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/python311.zip -o tmp\python311.zip
        
        if %errorlevel% neq 0 (
            echo "下载异常，请检查网络问题"
            del tmp\python311.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\python311.zip (
        echo "解压python311.zip"
        env\bandizip\Bandizip.x64.exe x -y  -target:auto -o:env tmp\python311.zip
        del tmp\python311.zip
    )
)

if not exist env\PowerShell\pwsh.exe (
    echo "PowerShell依赖环境不存在,开始下载PowerShell.zip"
    if not exist tmp\PowerShell.zip (
        curl -L https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PowerShell.zip -o tmp\PowerShell.zip
        if %errorlevel% neq 0 (
            echo "下载异常，请检查网络问题"
            del tmp\PowerShell.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\PowerShell.zip (
        echo "解压PowerShell.zip"
        env\bandizip\Bandizip.x64.exe x -y  -target:auto -o:env tmp\PowerShell.zip
        del tmp\PowerShell.zip
    )
)
if not exist env\java1.8\bin\java.exe (
    echo "java1.8依赖环境不存在,开始下载java1.8.zip"
    if not exist tmp\java1.8.zip (
        curl -L https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/jre1.8.zip -o tmp\java1.8.zip
        if %errorlevel% neq 0 (
            echo "下载异常，请检查网络问题"
            del tmp\java1.8.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\java1.8.zip (
        echo "解压java1.8.zip"
        env\bandizip\Bandizip.x64.exe  x -y -target:auto -o:env tmp\java1.8.zip
        del tmp\java1.8.zip
    )
)

if not exist env\java17\bin\java.exe (
    echo "java17依赖环境不存在,开始下载java17.zip"
    if not exist tmp\java17.zip (
        curl -L https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/jre17.zip -o tmp\java17.zip
        if %errorlevel% neq 0 (
            echo "下载异常，请检查网络问题"
            del tmp\java17.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\java17.zip (
        echo "解压java17.zip"
        env\bandizip\Bandizip.x64.exe x -y  -target:auto -o:env tmp\java17.zip
        del tmp\java17.zip
    )
)
if not exist env\PortableGit\bin\git.exe (
    echo "git依赖环境不存在,开始下载PortableGit.zip"
    if not exist tmp\PortableGit.zip (
        curl -L https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PortableGit.zip -o tmp\PortableGit.zip
        if %errorlevel% neq 0 (
            echo "下载异常，请检查网络问题"
            del tmp\PortableGit.zip
            pause
            exit /b 1
        )
    )
    if exist tmp\PortableGit.zip (
        echo "解压PortableGit.zip"
        env\bandizip\Bandizip.x64.exe x -y  -target:auto -o:env tmp\PortableGit.zip
        del tmp\PortableGit.zip
    )
)

if not exist .venv\Scripts\python.exe (
    echo "安装python依赖环境"
    env\Python311\python311.exe -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
    env\Python311\python311.exe -m pip install pdm 
    env\Python311\python311.exe -m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/
    env\Python311\python311.exe -m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/
    env\Python311\python311.exe -m pdm install
)else (
    start http://127.0.0.1:60001
    .venv\Scripts\python.exe -m  flask -A start_web  run --host 0.0.0.0 --port 60001
)

pause
