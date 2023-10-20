# ------------------------------------------------------------
Set-PSDebug -Trace 1
# 以下命令执行结束，请查看结果
# ------------------------------------------------------------
explorer C:\Users\Public\ws_tools\deployment_tools\oa;exit
# ------------------------------------------------------------
Get-Content 'C:\Users\Public\ws_tools\start_web\static\output\exec\1.ps1'  | Select-Object -Skip 2  | Select-Object -SkipLast 1
