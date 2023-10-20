import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from start_web.config.settings import *
from start_web.views.dict_create.get_pinyin import *
import json
import time

tool_info = re_tool_INFO  # 工具信息
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
        help_document = e
    # 读取目标文件显示到前端
    target_document = ""
    try:
        fr = open(file=target_file_path, mode="r", encoding="utf-8")
        target_document = fr.read()

        target_document_list = target_document.split("\n")
        if len(target_document_list) > 9:
            target_document_list = target_document_list[:9]
            target_document_list.append("......")
        target_document = "\n".join(target_document_list)
    except Exception as e:
        target_document = e
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=tool_name,
            tool_name=tool_name,
            path=tool_path,
            # dir_path=dir_name,
            targets_name=targets_name,
            help_document=help_document,
            target_document=target_document,
            # result_path=res_output_path,
            down_url=down_url,
            result_output_list=result_output_list,
            # form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            shell="",
        ),
    )


import re


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    re_type = post_data.get("re_type")
    re_str = post_data.get("re_str")
    if re_type == "text":
        targets = post_data.get("targets")
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write(targets)
        target_document = targets
    if re_type == "file":
        with open(file=target_file_path, mode="r", encoding="utf-8") as f:
            target_document = f.read()
    result = re.findall(re_str, target_document)

    res["data"] = "\n".join(result)
    return res


@bp.route(f"/{tool_name}/upload", methods=("POST",))
def upload():
    file = request.files["file"]
    file.save(target_file_path)
    res = dict(code=0, msg="文件保存成功", data="")
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
