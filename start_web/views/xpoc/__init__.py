import json
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from start_web.config.settings import *
from start_web.views.exec import *

import os
import time
import re

tool_info = xpoc_INFO  # 工具信息
tool_name = tool_info["name"]
tool_path = tool_info["path"]
down_url = tool_info["download_url"]
shell_str = tool_info["shell"]
update_path = tool_info["update_path"]
deployment_exec = tool_info["deployment_exec"]
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)


file_dir, file_name = os.path.split(tool_path)
res_output_path = os.path.join(STATIC_OUTPUT_PATH, tool_name)
try:
    os.makedirs(res_output_path)
except Exception as e:
    pass
targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(res_output_path, targets_name)  # 目标存放路径
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径
plugins_documnet_name = f"{tool_name}_plugins_document.txt"  # 帮助文件名称
plugins_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, plugins_documnet_name
)


@bp.route(f"/{tool_name}/")
def index():
    # 判断工具是否已经初始化，
    tool_path = tool_info["path"]
    if not os.path.exists(tool_path):
        tool_path = ""
    # ----------------------------------------------

    dir_name, full_file_name = os.path.split(tool_path)
    # 结果文件遍历回显
    result_output_list = []
    for filename in os.listdir(res_output_path):
        result_output_list.append(os.path.join(tool_name, filename))
    result_output_list.sort(reverse=True)
    # 读取帮助文档并回显
    help_document = ""
    try:
        fr = open(file=help_documnet_path, mode="r", encoding="utf-8")
        help_document = fr.read()
    except Exception as e:
        pass
    # 读取目标文件显示到前端
    target_document = ""
    try:
        fr = open(file=target_file_path, mode="r", encoding="utf-8")
        target_document = fr.read()
    except Exception as e:
        pass
    # 读取插件文档并回显
    plugins_documnet = ""
    try:
        fr = open(file=plugins_documnet_path, mode="r", encoding="utf-8")
        plugins_documnet = fr.read()
    except Exception as e:
        pass
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=tool_name,
            tool_name=tool_name,
            path=tool_path,
            dir_path=dir_name,
            targets_name=targets_name,
            help_document=help_document,
            result_output_list=result_output_list,
            target_document=target_document,
            result_path=res_output_path,
            down_url=down_url,
            form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            shell="",
            plugins_documnet=plugins_documnet,  # 插件列表
        ),
    )


def exec_shell_command(command):
    result = ""
    try:
        result = os.popen(command).read()
    except Exception as e:
        result = str(e)
    return result


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    target_list = []
    targets_str = post_data.get("targets")
    plugins_str = post_data.get("plugins")
    if "全部" in plugins_str:
        plugins_str="*"
    targets_list = list(targets_str.split("\n"))
    res_list = [x.strip() for x in targets_list]

    if len(res_list) > 0:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write("\n".join(res_list))
    output_time = (
        f"""{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}"""
    )
    output_file_path = f"""{os.path.join(res_output_path,f"{output_time}")}.html"""

    res["data"] = xpoc_exec(
        target_file_path=target_file_path, plugins=plugins_str, output_file_path=output_file_path
    )
    return res
# 既可以判断执行是否成功，还可以获取执行结果
import subprocess
def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() == None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait() != 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("命令执行失败，请检查设备连接状态")
            return False
        else:
            re = p.stdout.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('gb2312').strip('\r\n')
                result.append(res)
            return result
        
@bp.route(f"/{tool_name}/get_plugins", methods=("GET",))
def get_plugins():
    res = dict(code=0, msg="获取成功", data="")
    shell = ""

    dir_name, full_file_name = os.path.split(tool_info["path"])
    shell = rf"""cd {dir_name} & {full_file_name} --config xpoc-config.yaml --quiet -v """
    # shell = rf"""cd C:\Users\Public\ws_tools\start_web\views\xpoc && dir && {full_file_name} --config xpoc-config.yaml --quiet -v|findstr poc"""
    # print(f"{shell=}")
    exec_res = exec_shell_command(shell)
    # exec_res_list = subprocess.check_output(shell).decode('utf-8')
    # print(f"{exec_res_list=}")
    exec_res_list = exec_res.split("\n")
    plugin_list = []
    for plugin in exec_res_list:
        # print(f"{plugin=}")
        if "type:poc" in plugin:
            plugin_list.append(
                {
                    "name":plugin.split(" ")[-1],
                    "vaule":plugin.split(" ")[-1]
                }
            )
    plugin_length = len(plugin_list)
    plugin_list.insert(0, {
            "name":f'''全部（{plugin_length}个）''',
            "vaule":"*"
    })
 
    res['data']=plugin_list
    return res


@bp.route(f"/{tool_name}/save", methods=("POST",))
def save():
    res = dict(code=0, msg="帮助文件保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()
    return res


@bp.route(f"/{tool_name}/save_plugins_documnet", methods=("POST",))
def save_plugins_documnet():
    res = dict(code=0, msg="插件列表保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    plugins_documnet = post_data.get("plugins_documnet")
    if plugins_documnet:
        with open(file=plugins_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(plugins_documnet)
            fw.close()
    return res


@bp.route(f"/{tool_name}/tool_init", methods=("POST",))
def tool_init():
    res = dict(code=0, msg="工具初始化成功", data="")
    shell_exec(deployment_exec)
    return res

def xpoc_exec(target_file_path="", plugins="", output_file_path=""):
    shell = ""

    dir_name, full_file_name = os.path.split(tool_info["path"])
    output_dir_path, output_file_name = os.path.split(output_file_path)
    if tool_info["version"] == "python" or tool_info["version"] == "exe":
        shell = f"""cd '{dir_name}';
{tool_info['run_exec']}  .\{full_file_name} {eval(tool_info['argv'])};
"""
        return shell
    if tool_info["version"] == "java" or tool_info["version"] == "java_gui":
        shell = f"""cd '{dir_name}';
{tool_info['run_exec']}  -jar  .\{full_file_name} {eval(tool_info['argv'])};
"""
        return shell
    return "请检查version版本是否兼容"

