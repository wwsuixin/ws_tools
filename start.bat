@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM �л�����ǰĿ¼
cd /d %~dp0

@REM ���ô���url
set http_proxy=https://gh.h233.eu.org/
if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]��⵽��ǰ������δ��װ, ��ʼ�������нű�
    choice /C YN /M "ѯ���Ƿ�ʼ��װY��������N�˳�:"
    if errorlevel 2 (
        echo [-]��װ��ȡ��
        exit
    )
    echo [-]��ʼ�������нű�
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !http_proxy!/https://github.com/wwsuixin/ws_tools/releases/download/main/ws_tools.zip -OutFile tmp/ws_tools.zip}"
    @REM ��ѹws_tools.zip��ָ���ļ���
   @REM ���ǽ�ѹws_tools.zip��ָ���ļ���
   powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'tmp\ws_tools.zip' -DestinationPath './' -Force"
)

if not exist w_version.txt (
    echo [-]���绷���쳣,��������......
    pause
    exit
)
@REM ɾ��tmp/ws_tools.zip
if exist tmp\ws_tools.zip (
    del tmp\ws_tools.zip
)

powershell -ExecutionPolicy Bypass -File run.ps1 !http_proxy!