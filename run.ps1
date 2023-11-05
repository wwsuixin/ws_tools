
Set-Location -Path $PSScriptRoot
$tmp_dir_path = "tmp"
if (-not (Test-Path -Path $tmp_dir_path)) {
    New-Item -ItemType Directory -Path $tmp_dir_path
}
$env_dir_path = "env"
if (-not (Test-Path -Path $env_dir_path)) {
    New-Item -ItemType Directory -Path $env_dir_path
}



# 获取命令行传来的值，赋值到http_proxy
if ($args.Length -eq 1) {
    $http_proxy = $args[0]
}




function InstallTool($tool_name, $tmp_dir_path, $env_dir_path, $http_proxy) {
    Write-Host "开始检测是否安装$tool_name..."
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
        Write-Host "[-] $tool_name 不存在,开始下载......"
        # 使用powershell命令下载一个文件
        if (-not (Test-Path -Path $tmp_tool_file_path)) {
            if (-not (Test-Path -Path "env\aria2c\aria2c.exe")) {
                # 使用Invoke-WebRequest cmdlet下载文件
                (New-Object System.Net.WebClient).DownloadFile($URL, $tmp_tool_file_path)
            }
            else {
                Start-Process -FilePath "env\aria2c\aria2c.exe" -ArgumentList "-x 16 -s 16 -k 1M -o $tmp_tool_file_path $URL"
                $process = Get-Process -Name "aria2c"
                $process.WaitForExit()
            }
            
            #判断文件不存在或大小为0KB
            if (-not (Test-Path -Path $tmp_tool_file_path)) {
                Write-Host "[-] $tool_name.zip下载失败，请检查网络问题"
                Read-Host -Prompt "请按任意键继续. . ."
                exit 1
            }
            #判断文件大小为0KB
            if ((Get-Item $tmp_tool_file_path).Length -eq 0) {
                Write-Host "[-] 下载的文件大小为0KB，请检查网络问题"
                Read-Host -Prompt "请按任意键继续. . ."
                Remove-Item -Path $tmp_tool_file_path
                exit 1
            }
        }
        # 解压缩文件
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
            Write-Host "[-] $tool_name.zip解压失败，请检查"
            Read-Host -Prompt "请按任意键继续. . ."
            exit 1
        }
        Write-Host "[+] 安装完成$tool_name"

        Remove-Item -Path $tmp_tool_file_path
    }
    Write-Host "[+] 已安装$tool_name..."

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
