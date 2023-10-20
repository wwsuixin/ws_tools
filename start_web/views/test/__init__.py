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
import os
import time
import re

tool_name = "test"  # 工具名称
tool_info = xray_INFO  # 工具信息
tool_path = tool_info["path"]
down_url = tool_info["download_url"]
shell_str = tool_info["shell"]
update_path = tool_info["update_path"]
file_dir, file_name = os.path.split(tool_path)

bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)

# 定义输出目录-start
res_output_path = os.path.join(STATIC_OUTPUT_PATH, tool_name)
try:
    os.makedirs(res_output_path)
except Exception as e:
    pass
# 定义输出目录-end

targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(res_output_path, targets_name)  # 目标存放路径

# 定义帮助文档信息-start
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径
# 定义帮助文档信息-end


# tool_path = XRAY_PATH  # 工具路径
# targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
# target_file_path = os.path.join(STATIC_OUTPUT_PATH, targets_name)  # 目标存放路径
# help_documnet_path = os.path.join(
#     WEB_ROOT_PATH, "views", tool_name, f"{tool_name}_document.txt")  # 帮助文档路径
# down_url = XRAY_DOWN_URL  # 工具下载地址


@bp.route(f"/{tool_name}/")
def index():
    dir_name, full_file_name = os.path.split(tool_path)
    # 结果文件遍历回显
    result_output_list = []
    for filename in os.listdir(STATIC_OUTPUT_PATH):
        result_output_list.append(filename)
    # print(f"{output_list=}")
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
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=tool_name,  # h1标题
            tool_name=tool_name,  # 标题名称
            form_create="true",  # 生成按钮
            form_run="true",  # 运行按钮
            path=tool_path,  # 工具路径
            dir_path=dir_name,  # 工具文件夹
            targets_name=targets_name,  # 目标文件名称
            help_document=help_document,  # 帮助文件路径
            target_document=target_document,  # 目标文件路径
            result_path=STATIC_OUTPUT_PATH,  # 结果路径
            down_url=down_url,  # 工具下载路径
            result_output_list=result_output_list,  # 结果列表
        ),
    )


# 命令生成


def xray_exec(url_file="", plugins="", output_name=""):
    dir_name, full_file_name = os.path.split(tool_path)
    output_path = f"""{os.path.join(STATIC_OUTPUT_PATH,output_name)}.html"""
    output_path_dir, _ = os.path.split(output_path)

    shell = f"""cd '{dir_name}'; """
    shell += f""" .\{full_file_name} --config ./config.yaml webscan --html-output '{output_path}' --url-file '{url_file}' """
    if plugins:
        shell += f""" --plugins {plugins} """
    shell += f""";echo '------结果输出---------------------------------------';"""
    shell += f"""echo '{output_path}' ;"""
    return shell


# 生成主动扫描命令


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    plugins = post_data.get("plugins")
    targets = post_data.get("targets")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()
    if targets:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write(targets)
    output_name = f"""{tool_name}_output-{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}"""

    res["data"] = xray_exec(
        url_file=target_file_path, plugins=plugins, output_name=output_name
    )
    return res


# 生成被动扫描命令


@bp.route(f"/{tool_name}/update_listen", methods=("POST",))
def update_listen():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    listen_port = post_data.get("listen_port")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()

    xray_output_file = os.path.join(
        STATIC_OUTPUT_PATH,
        f"{tool_name}_output-{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}.html",
    )

    dir_name, full_file_name = os.path.split(tool_path)

    res["data"] = f"""cd '{dir_name}'; """
    res[
        "data"
    ] += f""" .\{full_file_name} webscan --html-output {xray_output_file} --listen  127.0.0.1:{listen_port} """
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
