# ws\_tools使用手册

# 安装说明
## 先看注意

1. **当前项目不支持存在中文路径**
2. **复制以下代码到某空白文件夹下，并保存为bat双击即可自动安装运行,注意文件格式必须为gb2312**
3. 所有环境安装完成后将开启60001服务端口并自动使用默认浏览器打开**http://127.0.0.1:60001**
4. 后续运行也仅需要双击该bat文件启动
5. 如果日常使用过程中升级后出现无法启动情况请运行核心重装脚本
6. 若还有其他问题请添加微信公众号`无尽信安`联系作者排查
## 安装脚本
```bat
@echo off
title ws_tools
setlocal enabledelayedexpansion

@REM 切换到当前目录
cd /d %~dp0

@REM 设置代理url
set http_proxy=https://gh.con.sh
if not exist tmp (
    mkdir tmp
)

if not exist w_version.txt (
    echo [-]检测到当前环境还未安装, 开始下载运行脚本
    choice /C YN /M "询问是否开始安装Y继续，回N退出:"
    if errorlevel 2 (
        echo [-]安装已取消
        exit
    )
    echo [-]开始下载运行脚本
    powershell -ExecutionPolicy Bypass -Command "& {iwr -useb !http_proxy!/https://github.com/wwsuixin/ws_tools/releases/download/main/ws_tools.zip -OutFile tmp/ws_tools.zip}"
    @REM 解压ws_tools.zip到指定文件夹
   @REM 覆盖解压ws_tools.zip到指定文件夹
   powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path 'tmp\ws_tools.zip' -DestinationPath './' -Force"
)

if not exist w_version.txt (
    echo [-]网络环境异常,请检查网络......
    pause
    exit
)
@REM 删除tmp/ws_tools.zip
if exist tmp\ws_tools.zip (
    del tmp\ws_tools.zip
)

powershell -ExecutionPolicy Bypass -File run.ps1 !http_proxy!
```
## 重装脚本

```bat
@echo off 
echo 该脚本仅用于服务无法启动时进行核心程序重装,没啥影响,放心装
choice /C YN /M "是否开始[Y/N]:"
if errorlevel 2 (
    echo [-]安装已取消
    exit
)
@REM 删除.venv、start_web、pyproject.toml等目录
if exist .venv (
    rmdir /s /q .venv/w_version.txt
)

if exist w_version.txt (
    del w_version.txt
)

start start.bat
```

# 项目简介
1.  项目说明
    -   本项目支持免安装运行
    -   本项目通过python-flask作为服务端、layui作为web前端进行开发，意在提高日常渗透中常用工具使用的效率，如sqlmap的post注入不在需要手动创建文件、指定路径等重复工作
    -   本项目内python脚本均使用pdm虚拟环境进行运行
    -   项目基于AMD x64 windows 10环境开发，其他环境可能存在不兼容情况，请自测
2.  项目地址
    -  https://github.com/wwsuixin/ws_tools


# 工具使用说明[编写中]

## 信息收集
### 单位名称
#### 教育网IP查询
- [github地址](files/教育网IP查询)
- [微信公众号地址](https://mp.weixin.qq.com/s/jPHsVteFBdVhuZczXsGkDw)
## 漏洞扫描
### 框架扫描
#### 小程序反编译
- [github地址](files/小程序反编译.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/M3mf04rmHV3S5AvvgWv-BA)
## 数据处理
### 综合
### 正则-同类数据提取
- [github地址](files/正则-同类数据提取.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/PvQaFzZRuxgb2IlhR9-1Mg)
## 内网渗透
### 内网横向
#### fscan结果分析&批量验证
- [github地址](files/fscan结果分析&批量验证.md)
- 微信公众号地址
## 其他
#### 报告平台
- [github地址](files/报告平台.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/TQQXFuoVf8POpzQpBwXilw)

# 常见问题

- 问题：升级后出现无法启动情况
	- 解答：运行上述重装脚本，将自动重装依赖环境来解决，如无法解决则联系作者排查
- 问题：bat脚本运行乱码
	- 解答：需要保存为gb2312编码执行
- 问题：默认内置版本为python3.11
	- 解答：python311不支持win10以下版本
- 问题：安装python依赖环境遇到报错：` Microsoft Visual C++ 14.0 or greater is required`
	- 解答：参考文章：https://zhuanlan.zhihu.com/p/471661231


# 功能展示

## 工具首页

![readme-3.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112103518.png)


## 信息收集

![readme-1.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112103333.png)

## 漏洞扫描

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112104373.png)

## 漏洞利用

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112104834.png)

## 数据处理

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112104324.png)

## 系统工具

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112104296.png)



# 联系我

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202311112107408.png)

