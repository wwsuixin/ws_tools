import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from start_web.config.settings import *
import os
tool_name = "ProxyPoolxSocks"  # 工具名称
tool_path = ProxyPoolxSocks_PATH
down_url = ProxyPoolxSocks_DOWN_URL
shell_str = ProxyPoolxSocks_EXEC

file_dir, file_name = os.path.split(tool_path)
targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(STATIC_OUTPUT_PATH, targets_name)  # 目标存放路径
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name)  # 帮助文档路径


bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",    # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)


@bp.route(f'/{tool_name}/')
def index():
    # 读取帮助文档并回显
    help_document = ""
    try:
        fr = open(file=help_documnet_path, mode="r", encoding="utf-8")
        help_document = fr.read()
    except Exception as e:
        pass
    return render_template(f'{tool_name}/{tool_name}.html', res=dict(
        h1=tool_name,  # h1标题
        tool_name=tool_name,  # 标题名称
        form_run="true",
        path=tool_path,  # 工具路径
        dir_path=file_dir,
        targets_name=targets_name,  # 目标文件名称
        help_document=help_document,  # 帮助文件路径
        down_url=down_url,  # 工具下载路径
        shell=shell_str
    ))


@bp.route(f'/{tool_name}/save', methods=('POST',))
def save():
    res = dict(
        code=0,
        msg="帮助文件保存成功",
        data=""
    )
    post_data = request.get_data()
    post_data = json.loads(post_data)
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode='w', encoding="utf-8")as fw:
            fw.write(help_document)
            fw.close()
    return res
