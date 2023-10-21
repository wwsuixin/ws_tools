Set-Location -Path $PSScriptRoot
if (-not (Test-Path -Path "tmp")) {
    New-Item -ItemType Directory -Path "tmp"
}




if (-not (Test-Path -Path "env\python311\python311.exe")) {
    Write-Host "python311��������������,��ʼ����python311.zip"
    if (-not (Test-Path -Path "tmp\python311.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\python311.zip https://github.com/wwsuixin/ws_tools/releases/download/202310201112/python311.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\python311.zip").Length -eq 0) {
            Write-Host "���ص��ļ���СΪ0KB��������������"
            Remove-Item -Path "tmp\python311.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }

    }
    if (Test-Path -Path "tmp\python311.zip") {
        Write-Host "��ѹpython311.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\python311.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\python311.zip"
    }
}

if (-not (Test-Path -Path "env\PowerShell\pwsh.exe")) {
    Write-Host "PowerShell��������������,��ʼ����PowerShell.zip"
    if (-not (Test-Path -Path "tmp\PowerShell.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\PowerShell.zip https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PowerShell.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\PowerShell.zip").Length -eq 0) {
            Write-Host "���ص��ļ���СΪ0KB��������������"
            Remove-Item -Path "tmp\PowerShell.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\PowerShell.zip") {
        Write-Host "��ѹPowerShell.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\PowerShell.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\PowerShell.zip"
    }
}
if (-not (Test-Path -Path "env\java1.8\bin\java.exe")) {
    Write-Host "java1.8��������������,��ʼ����java1.8.zip"
    if (-not (Test-Path -Path "tmp\java1.8.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\java1.8.zip https://github.com/wwsuixin/ws_tools/releases/download/202310201112/java1.8.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\java1.8.zip").Length -eq 0) {
            Write-Host "���ص��ļ���СΪ0KB��������������"
            Remove-Item -Path "tmp\java1.8.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\java1.8.zip") {
        Write-Host "��ѹjava1.8.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y -target:auto -o:env tmp\java1.8.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\java1.8.zip"
    }
}

if (-not (Test-Path -Path "env\java17\bin\java.exe")) {
    Write-Host "java17��������������,��ʼ����java17.zip"
    if (-not (Test-Path -Path "tmp\java17.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\java17.zip https://github.com/wwsuixin/ws_tools/releases/download/202310201112/java17.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\java17.zip").Length -eq 0) {
            Write-Host "���ص��ļ���СΪ0KB��������������"
            Remove-Item -Path "tmp\java17.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\java17.zip") {
        Write-Host "��ѹjava17.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\java17.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\java17.zip"
    }
}
if (-not (Test-Path -Path "env\PortableGit\bin\git.exe")) {
    Write-Host "git��������������,��ʼ����PortableGit.zip"
    if (-not (Test-Path -Path "tmp\PortableGit.zip")) {
        Start-Process -FilePath "env\aria2\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o tmp\PortableGit.zip https://github.com/wwsuixin/ws_tools/releases/download/202310201112/PortableGit.zip"
        $process = Get-Process -Name "aria2c"
        $process.WaitForExit()
        if ((Get-Item "tmp\PortableGit.zip").Length -eq 0) {
            Write-Host "���ص��ļ���СΪ0KB��������������"
            Remove-Item -Path "tmp\PortableGit.zip"
            Read-Host -Prompt "Press Enter to exit"
            exit 1
        }
    }
    if (Test-Path -Path "tmp\PortableGit.zip") {
        Write-Host "��ѹPortableGit.zip"
        Start-Process -FilePath "env\bandizip\Bandizip.x64.exe" -ArgumentList "x -y  -target:auto -o:env tmp\PortableGit.zip"
        $process = Get-Process -Name "Bandizip.x64"
        $process.WaitForExit()
        Remove-Item -Path "tmp\PortableGit.zip"
    }
}

if (-not (Test-Path -Path ".venv\Scripts\python.exe")) {
    Write-Host "��װpython��������"
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/"
    $process = Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pip install pdm" -PassThru
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) {
        Write-Host "pdm��װʧ��"
        Read-Host -Prompt "��Enter���˳�"
        exit 1
    }
    Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/"
    $process = Start-Process -FilePath "env\Python311\python311.exe" -ArgumentList "-m pdm install" -PassThru
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) {
        Write-Host "pdm install����ִ��ʧ��"
        Read-Host -Prompt "��Enter���˳�"
        exit 1
    }

}

    Write-Host "��װ��ɣ�����������start.bat"


Read-Host -Prompt "Press Enter to exit"


