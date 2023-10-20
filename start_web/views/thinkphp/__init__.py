import re
from ...views.xray import xray_exec
from ...views.nuclei import nuclei_exec
from ...views.exec import shell_exec
from ...views.tidefinger import tidefinger_exec
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

tool_info = thinkphp_INFO  # 工具信息
tool_name = tool_info["name"]
tool_path = tool_info["path"]
down_url = tool_info["download_url"]
shell_str = tool_info["shell"]
update_path = tool_info["update_path"]
deployment_exec = tool_info["deployment_exec"]
poc_list = tool_info["poc"]
exp_list = tool_info["exp"]
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
        print(f"{filename=}")
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
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=tool_name,
            tool_name=tool_name,
            path=tool_path,
            dir_path=dir_name,
            targets_name=targets_name,
            help_document=help_document,
            target_document=target_document,
            result_path=res_output_path,
            down_url=down_url,
            result_output_list=result_output_list,
            form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            shell="",
        ),
    )


@bp.route(f"/{tool_name}/tool_init", methods=("POST",))
def tool_init():
    res = dict(code=0, msg="工具初始化成功", data="")
    shell_exec(deployment_exec)
    return res


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    targets = post_data.get("targets")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()
    if targets:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write(targets)
    # dir_name, full_file_name = os.path.split(thinkphp_path)
    output_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))

    xray_output_file_path = (
        f"""{os.path.join(res_output_path,f"xray_{output_time}")}.html"""
    )
    nuclei_output_file_path = (
        f"""{os.path.join(res_output_path,f"nuclei_{output_time}")}.html"""
    )
    tidefinger_output_file_path = (
        f"""{os.path.join(res_output_path,f"tidefinger_{output_time}")}.html"""
    )
    thinkphp_output_file_path = (
        f"""{os.path.join(res_output_path,f"thinkphp_{output_time}")}.html"""
    )

    data_list = [
        xray_exec(
            target_file_path=target_file_path,
            plugins="thinkphp",
            output_file_path=xray_output_file_path,
        ),
        nuclei_exec(
            target_file_path=target_file_path,
            plugins="thinkphp",
            output_file_path=nuclei_output_file_path,
        ),
        tidefinger_exec(
            target_file_path=target_file_path,
            plugins="thinkphp",
            output_file_path=tidefinger_output_file_path,
        ),
    ]
    shell_list = thinkphp_poc_exec(
        target_file_path=target_file_path, output_file_path=thinkphp_output_file_path
    )
    # print(f"{shell_list}")
    data_list += shell_list
    # 前台显示需要换行
    res["data"] = "\n------------------------------\n".join(data_list)
    # res["data"] = data_list
    return res


@bp.route(f"/{tool_name}/exp", methods=("POST",))
def exp():
    data_list = thinkphp_exp_exec()

    res = shell_exec(shell="\n------------------------------\n".join(data_list))

    return res


def thinkphp_exp_exec(url_file="", plugins="", output_name=""):
    shell_list = []
    for exp_info in exp_list:
        shell = ""
        dir_name, full_file_name = os.path.split(exp_info["path"])
        output_path = f"""{os.path.join(res_output_path,f"{output_name}")}.html"""
        output_path_dir, _ = os.path.split(output_path)
        if exp_info["version"] == "java_gui":
            shell += f"""cd '{dir_name}'; """
            shell += f"""{exp_info['run_exec']}  -jar .\{full_file_name} ;"""
        shell_list.append(shell)
    return shell_list


def thinkphp_poc_exec(url_file="", plugins="", output_name=""):
    shell_list = []
    for poc_info in poc_list:
        shell = ""
        dir_name, full_file_name = os.path.split(poc_info["path"])
        output_path = f"""{os.path.join(res_output_path,f"{output_name}")}.html"""
        output_path_dir, _ = os.path.split(output_path)

        shell += f"""cd '{dir_name}'; """
        shell += (
            f"""{poc_info['run_exec']}  .\{full_file_name} {eval(poc_info['argv'])};"""
        )
        shell_list.append(shell)

    return shell_list


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
