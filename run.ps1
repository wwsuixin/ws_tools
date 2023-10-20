Set-Location -Path $PSScriptRoot
if (-not (Test-Path -Path "tmp")) {
    New-Item -ItemType Directory -Path "tmp"
}

if (-not (Test-Path -Path "env\python311\python311.exe")) {
    Write-Host "python311依赖环境不存在,开始下载python311.zip"
    if (-not (Test-Path -Path "tmp\python311.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\python311.zip https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/python311.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\python311.zip").Length -eq 0) {
            Write-Host "下载的文件大小为0KB，请检查网络问题"
            Remove-Item -Path "tmp\python311.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }

    }
    if (Test-Path -Path "tmp\python311.zip") {
        Write-Host "解压python311.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\python311.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\python311.zip"
    }
}

if (-not (Test-Path -Path "env\PowerShell\pwsh.exe")) {
    Write-Host "PowerShell依赖环境不存在,开始下载PowerShell.zip"
    if (-not (Test-Path -Path "tmp\PowerShell.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\PowerShell.zip https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PowerShell.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\PowerShell.zip").Length -eq 0) {
            Write-Host "下载的文件大小为0KB，请检查网络问题"
            Remove-Item -Path "tmp\PowerShell.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\PowerShell.zip") {
        Write-Host "解压PowerShell.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\PowerShell.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\PowerShell.zip"
    }
}
if (-not (Test-Path -Path "env\java1.8\bin\java.exe")) {
    Write-Host "java1.8依赖环境不存在,开始下载java1.8.zip"
    if (-not (Test-Path -Path "tmp\java1.8.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\java1.8.zip https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/java1.8.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\java1.8.zip").Length -eq 0) {
            Write-Host "下载的文件大小为0KB，请检查网络问题"
            Remove-Item -Path "tmp\java1.8.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\java1.8.zip") {
        Write-Host "解压java1.8.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y -target:auto -o:env tmp\java1.8.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\java1.8.zip"
    }
}

if (-not (Test-Path -Path "env\java17\bin\java.exe")) {
    Write-Host "java17依赖环境不存在,开始下载java17.zip"
    if (-not (Test-Path -Path "tmp\java17.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\java17.zip https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/java17.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\java17.zip").Length -eq 0) {
            Write-Host "下载的文件大小为0KB，请检查网络问题"
            Remove-Item -Path "tmp\java17.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\java17.zip") {
        Write-Host "解压java17.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\java17.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\java17.zip"
    }
}
if (-not (Test-Path -Path "env\PortableGit\bin\git.exe")) {
    Write-Host "git依赖环境不存在,开始下载PortableGit.zip"
    if (-not (Test-Path -Path "tmp\PortableGit.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\PortableGit.zip https://git.xfj0.cn/https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PortableGit.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\PortableGit.zip").Length -eq 0) {
            Write-Host "下载的文件大小为0KB，请检查网络问题"
            Remove-Item -Path "tmp\PortableGit.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\PortableGit.zip") {
        Write-Host "解压PortableGit.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\PortableGit.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\PortableGit.zip"
    }
}

if (-not (Test-Path -Path ".venv\Scripts\python.exe")) {
    Write-Host "安装python依赖环境"
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/"
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pip install pdm"
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/"
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pdm install"
}
else {
    Start-Process -FilePath "http://127.0.0.1:60001"
    Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m  flask -A start_web  run --host 0.0.0.0 --port 60001"
}

Read-Host -Prompt "Press Enter to exit"

