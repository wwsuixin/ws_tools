chcp 65001
@echo off 
cd %~dp0

echo 当前版本信息：
type version.txt
echo 获取github更新
env\PortableGit\bin\git.exe  clone https://github.com/wwsuixin/ws_tools.git
echo 已更新到最新版本：
type version.txt
pause