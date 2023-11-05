
Set-Location -Path $PSScriptRoot
$tmp_dir_path = "tmp"
if (-not (Test-Path -Path $tmp_dir_path)) {
    New-Item -ItemType Directory -Path $tmp_dir_path
}
$env_dir_path = "env"
if (-not (Test-Path -Path $env_dir_path)) {
    New-Item -ItemType Directory -Path $env_dir_path
}



# ��ȡ�����д�����ֵ����ֵ��http_proxy
if ($args.Length -eq 1) {
    $http_proxy = $args[0]
}




function InstallTool($tool_name, $tmp_dir_path, $env_dir_path, $http_proxy) {
    Write-Host "��ʼ����Ƿ�װ$tool_name..."
    $tmp_tool_file_path = "$tmp_dir_path/$tool_name.zip"
    $env_tool_dir_path = "$env_dir_path/$tool_name"
    $env_tool_version_path = "$env_dir_path/$tool_name/w_version.txt"
    $URL = "$http_proxy/https://github.com/wwsuixin/ws_tools/releases/download/latest/$tool_name.zip"
    if ($tool_name -eq "start_web") {
        $env_tool_version_path = "$tool_name/w_version.txt"
    }
    if ($tool_name -eq "venv") {
        $env_tool_version_path = ".venv/w_version.txt"
    }
    if (-not (Test-Path -Path $env_tool_version_path)) {
        Write-Host "[-] $tool_name ������,��ʼ����......"
        # ʹ��powershell��������һ���ļ�
        if (-not (Test-Path -Path $tmp_tool_file_path)) {
            if (-not (Test-Path -Path "env\aria2c\aria2c.exe")) {
                # ʹ��Invoke-WebRequest cmdlet�����ļ�
                (New-Object System.Net.WebClient).DownloadFile($URL, $tmp_tool_file_path)
            }
            else {
                Start-Process -FilePath "env\aria2c\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o $tmp_tool_file_path $URL"
                $process = Get-Process -Name "aria2c"
                $process.WaitForExit()
            }
            
            #�ж��ļ������ڻ��СΪ0KB
            if (-not (Test-Path -Path $tmp_tool_file_path)) {
                Write-Host "[-] $tool_name.zip����ʧ�ܣ�������������"
                Read-Host -Prompt "�밴���������. . ."
                exit 1
            }
            #�ж��ļ���СΪ0KB
            if ((Get-Item $tmp_tool_file_path).Length -eq 0) {
                Write-Host "[-] ���ص��ļ���СΪ0KB��������������"
                Read-Host -Prompt "�밴���������. . ."
                Remove-Item -Path $tmp_tool_file_path
                exit 1
            }
        }
        # ��ѹ���ļ�
        if (-not (Test-Path -Path "env\bandizip\bandizip.exe")) {
            Expand-Archive -Path $tmp_tool_file_path -DestinationPath "$env_tool_dir_path/"
        }
        else {
            if ($tool_name -eq "start_web") {
                Start-Process -FilePath "env\bandizip\bandizip.exe" -ArgumentList "x -y  -o:./ $tmp_tool_file_path"
            }
            elseif ($tool_name -eq "venv") {
                Start-Process -FilePath "env\bandizip\bandizip.exe" -ArgumentList "x -y  -o:./.venv $tmp_tool_file_path"
            }
            else {
                Start-Process -FilePath "env\bandizip\bandizip.exe" -ArgumentList "x -y  -target:auto -o:$env_dir_path $tmp_tool_file_path"
            }
            $process = Get-Process -Name "bandizip"
            $process.WaitForExit()
        }

        if (-not (Test-Path -Path $env_tool_version_path)) {
            Write-Host "[-] $tool_name.zip��ѹʧ�ܣ�����"
            Read-Host -Prompt "�밴���������. . ."
            exit 1
        }
        Write-Host "[+] ��װ���$tool_name"

        Remove-Item -Path $tmp_tool_file_path
    }
    Write-Host "[+] �Ѱ�װ$tool_name..."

}

InstallTool "aria2c" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "bandizip" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "python311" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "powershell" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "jdk1.8" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "jdk11" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "jdk17" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "start_web" $tmp_dir_path $env_dir_path $http_proxy
InstallTool "venv" $tmp_dir_path $env_dir_path $http_proxy

Start-Process -FilePath "chrome" -ArgumentList "http://127.0.0.1:60001"
Start-Process -FilePath ".venv\Scripts\python.exe" -ArgumentList "-m", "flask", "-A", "start_web", "run",  "--host", "0.0.0.0", "--port", "60001"
