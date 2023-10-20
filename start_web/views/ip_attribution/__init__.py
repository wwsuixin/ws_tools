import re
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from start_web.config.settings import *
import os
import time
from start_web.views.exec import shell_exec
tool_name = "ip_attribution"
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",    # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)
targets_name = f"{tool_name}_targets.txt"
target_file_path = os.path.join(STATIC_OUTPUT_PATH, targets_name)
help_documnet_name = f"{tool_name}_help_document.txt"
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name)  # 帮助文档路径
tool_path = ""
download_url = ""




@bp.route(f'/{tool_name}/')
def index():
    dir_name, full_file_name = os.path.split(tool_path)

    # 结果文件遍历回显
    result_output_list = []
    for filename in os.listdir(STATIC_OUTPUT_PATH):
        if len(re.findall(rf"^{tool_name}_.*", filename)) > 0:
            result_output_list.append(filename)
    print(f"{result_output_list=}")
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
    return render_template(f'{tool_name}/{tool_name}.html', res=dict(
        h1=tool_name,  # h1标题
        tool_name=tool_name,  # 标题名称
        path=tool_path,  # 工具路径
        dir_path=dir_name,  # 工具文件夹
        targets_name=targets_name,  # 目标文件名称
        help_document=help_document,  # 帮助文件路径
        target_document=target_document,  # 目标文件路径

        result_path=STATIC_OUTPUT_PATH,  # 结果路径
        result_output_list=result_output_list,  # 结果列表
        down_url=download_url,  # 工具下载路径

    ))


@bp.route(f'/{tool_name}/update', methods=('POST',))
def update():
    res = dict(
        code=0,
        msg="命令生成成功",
        data=""
    )
    post_data = request.get_data()
    post_data = json.loads(post_data)
    targets = post_data.get("targets")
    targets = targets.replace(" ", "")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode='w', encoding="utf-8")as fw:
            fw.write(help_document)
            fw.close()
    if targets:
        shell_exec(f"start {targets}")
    return res

