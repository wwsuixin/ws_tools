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

tool_name = "clean"  # 工具名称
tool_info = {
    "path": "",
    "download_url": "",
    "shell": "",
}  # 工具信息
tool_path = tool_info["path"]
down_url = tool_info["download_url"]
shell_str = tool_info["shell"]
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

bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)


@bp.route(f"/{tool_name}/")
def index():
    # 结果文件遍历回显
    result_output_list = []
    for filename in os.listdir(res_output_path):
        result_output_list.append(os.path.join(tool_name, filename))
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
            form_create="true",
            form_run="true",
            path=tool_path,  # 工具路径
            dir_path=file_dir,  # 工具文件夹
            targets_name=targets_name,  # 目标文件名称
            help_document=help_document,  # 帮助文件路径
            target_document=target_document,  # 目标文件路径
            result_path=res_output_path,  # 结果路径
            down_url=down_url,  # 工具下载路径
            result_output_list=result_output_list,  # 结果列表
        ),
    )


def clean_exec(url_file="", plugins="", output_name=""):
    fr = open(help_documnet_path, "r", encoding="utf-8")
    clean_path_list = fr.read().splitlines()
    shell = ""
    for clean_path in clean_path_list:
        shell += f"""Remove-Item -Force  "{clean_path}"  -recurse ;"""

    return shell


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)

    clean_path_str = post_data.get("clean_path_str")

    clean_path_list = list(clean_path_str.split("\n"))
    clean_path_list = [x.strip() for x in clean_path_list]  # 删除 左右 空格
    clean_path_list = [x.strip('"') for x in clean_path_list]  # 兼容 双引号 路径

    res_list = []
    for clean_path in clean_path_list:
        clean_path = clean_path.replace('"', "")
        res_list.append(clean_path)

    if len(res_list) > 0:
        with open(help_documnet_path, "w", encoding="utf-8") as fw:
            fw.write("\n".join(res_list))
    output_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    output_name = f"{tool_name}_output-{output_time}"
    res["data"] = clean_exec()
    return res
