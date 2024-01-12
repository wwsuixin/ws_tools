# 背景

- 日常渗透中常常会考虑该系统使用的是什么框架，然后对其进行指纹识别，再查询是否存在历史漏洞，再一步进行poc验证
- 日常中我们经常会使用xray的被动扫描来检测是否存在sql注入、xss等其他常规漏洞
# 解决方案

- 针对上述问题，将通过【无尽工具箱】联动实现，提高渗透效率
# 方案1

- 使用finger实现指纹识别

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121631981.png)

- 点击【运行】后，等待任务执行结束

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121634157.png)

- 分析识别后的结果

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121639934.png)

- 点击【漏洞扫描】将自动跳转到【w_scan】，数据也将同步输入，该功能也可直接访问该页面使用，自行输入【目标】、【插件】

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121641447.png)

- 自动调用xpoc等漏扫工具实现专项漏洞扫描
- 
![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121647781.png)

# 方案2

- 使用xray的被动扫描实现全面打击

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121649309.png)

- 默认开启代理端口为【1111】

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121650665.png)

- 浏览器访问目标网站并将流量代理到该端口，直接实现历史漏洞检测

![image.png](https://raw.githubusercontent.com/wwsuixin/images/main/202401121652490.png)
