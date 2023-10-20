# ------------------------------------------------------------
Set-PSDebug -Trace 1
# 以下命令执行结束，请查看结果
# ------------------------------------------------------------

$path="C:\Users\Public\ws_tools\tmp\start_web.zip"
Invoke-WebRequest -Uri "https://raw.fgit.cf/test7911/deployment/main/start_web.zip" -OutFile $path

if (!(Test-Path -Path $path)) {
    Write-Host "File does not exist. Exiting program."
    pause
    exit
}

    $source="C:\Users\Public\ws_tools\start_web"
    $destination="C:\Users\Public\ws_tools\start_web_1697715107"
    Rename-Item -Path $source -NewName $destination

C:\Users\Public\ws_tools\env\BANDIZIP-PORTABLE\Bandizip.x64.exe x -target:auto -o:C:\Users\Public\ws_tools C:\Users\Public\ws_tools\tmp\start_web.zip

# ------------------------------------------------------------
Get-Content 'C:\Users\Public\ws_tools\start_web\static\output\exec\1.ps1'  | Select-Object -Skip 2  | Select-Object -SkipLast 1
