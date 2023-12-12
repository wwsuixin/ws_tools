# ws\_tools使用手册

# 安装说明
## 先看注意

- **当前项目不支持存在中文路径**
- **运行安装脚本出现乱码：解决方案：cmd /c "chcp 936 > nul && type start.bat >  start.bat.tmp && move /y  start.bat.tmp  start.bat"**
- **运行start.bat即可进行安装，后续使用也仅需要双击该bat文件启动**
- 所有依赖环境安装完成后将开启60001服务端口并自动使用默认浏览器打开**http://127.0.0.1:60001**
- 如果日常使用过程中升级后出现无法启动情况请运行核心重装脚本
- 若还有其他问题请添加微信公众号`无尽信安`联系作者排查



# 项目简介
- 项目说明
    -   本项目通过python-flask作为服务端、layui作为web前端进行开发，意在提高日常渗透中常用工具使用的效率，如sqlmap的post注入不在需要手动创建文件、指定路径等重复工作
    -   本项目内python脚本均使用pdm虚拟环境进行运行
    -   项目基于AMD x64 windows 10环境开发，其他环境可能存在不兼容情况，请自测
- 项目地址
    -  https://github.com/wwsuixin/ws_tools


# 工具使用说明【编写中】

## 信息收集
### 单位名称
### 企业信息收集
#### 教育网IP查询
- [github地址](files/教育网IP查询)
- [微信公众号地址](https://mp.weixin.qq.com/s/jPHsVteFBdVhuZczXsGkDw)
### 域名、IP
#### fofamap
#### Fofa客户端
#### Ip查询\[域名、权重、备案\]
#### Ip查询\[归属地\]
### 指纹识别
#### finger
### 抓包工具
#### burpsuite
#### ~~微信小程序抓包~~

## 漏洞扫描
### 目录扫描
#### dirsearch
#### PackerFuzzer
#### 网站敏感信息扫描-bbscan
#### 网站备份文件扫描-ihoneyBakFileScan_Modify
#### ~~集成扫描~~
### 综合扫描
#### xray
#### xpoc
#### nuclei
#### tidefinger
#### gorailgun
### 框架扫描
#### thinkphp
#### weblogic
#### 小程序反编译
- [github地址](files/小程序反编译.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/M3mf04rmHV3S5AvvgWv-BA)
#### OA
#### Shiro
## 漏洞利用
### 漏洞利用

#### sqlmap
#### dbeaver
#### 数据库连接
#### mdut
#### 数据库取样-DataMiner
### webshell连接
#### 中国蚁剑
#### 冰蝎
#### 哥斯拉
### 框架利用
#### .git/.svn/.DS_Store利用
#### Nacos
#### heapdump
### 反弹shell
#### 生成命令-reverse_shell_generator
#### 写马辅助-webshell_encode
#### 临时服务器
- [github地址](files/临时服务器.md)
- 微信公众号地址
## 数据处理
### 综合
#### URL处理
#### 掩码转IP
### 正则-同类数据提取
- [github地址](files/正则-同类数据提取.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/PvQaFzZRuxgb2IlhR9-1Mg)
#### 正则-敏感数据提取
### 社工字典
#### md5碰撞
#### 字典生成
#### 默认用户密码查询
## 内网渗透
### 内网资产
#### 进程识别
- [github地址](files/进程识别.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/i-ND212vKRm_a82rbg60VA)
### 内网横向
#### fscan结果分析
- [github地址](files/fscan结果分析&批量验证.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/uTBLbq7DxKHSdwlMuxdQDg)
#### 服务登录验证
### 内网穿透
#### frp

#### 防溯源
## 系统工具
### 代理
#### socks代理
#### fastgithub
### 综合
#### 系统命令执行

#### ~~痕迹清理~~
#### MobaXterm

## 其他
#### 报告平台
- [github地址](files/报告平台.md)
- [微信公众号地址](https://mp.weixin.qq.com/s/TQQXFuoVf8POpzQpBwXilw)
#### 其他工具快捷方式
#### 下载器


# 常见问题

- 问题：升级后出现无法启动情况
	- 解答：运行上述重装脚本，将自动重装依赖环境来解决，如无法解决则联系作者排查
- 问题：bat脚本运行乱码
	- 解答：需要保存为gb2312编码执行
- 问题：默认内置版本为python3.11
	- 解答：python311不支持win10以下版本
- 问题：安装python依赖环境遇到报错：` Microsoft Visual C++ 14.0 or greater is required`
	- 解答：参考文章：https://zhuanlan.zhihu.com/p/471661231


# 界面展示

## 工具首页

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202312121422306.png)



# 联系我
添加微信公众号**无尽信安**