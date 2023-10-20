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

tool_info = edu_ip_search_INFO  # 工具信息
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
help_documnet_name = f"{tool_name}_help_document.txt"
help_documnet_path = os.path.join(WEB_ROOT_PATH, "views", tool_name, help_documnet_name)
edu_ip_name = f"edu_ip.txt"
edu_ip_file_path = os.path.join(WEB_ROOT_PATH, "views", tool_name, "files", edu_ip_name)


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

    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=tool_name,
            tool_name=tool_name,
            # path=tool_path,
            # dir_path=dir_name,
            # targets_name=targets_name,
            # help_document=help_document,
            # result_output_list=result_output_list,
            # target_document=target_document,
            # result_path=res_output_path,
            # down_url=down_url,
            # form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            # shell="",
        ),
    )


@bp.route(f"/{tool_name}/list", methods=("POST", "GET"))
def list():
    res = dict(code=0, msg="获取成功", data="")
    # Inserted code starts here
    
    school = request.form.get("school")
    if not school:
        school = ""

    page = request.form.get("page")
    limit = request.form.get("limit")

    with open(edu_ip_file_path, "r", encoding="utf-8") as f:
        edu_ip_data_list = f.read().splitlines()
    re_str = f".*{school}.*"
    # print(f"{re_str=}")
    res_data_list = []
    id = 1
    for line in edu_ip_data_list:
        if re.match(re_str, line):
            line_list = line.split(",")
            res_data_list.append(
                {
                    "id": id,
                    "ips": line_list[0],
                    "location": line_list[1],
                    "school": line_list[2],
                    "network_type": line_list[3],
                }
            )
            id = id + 1
    res['count']=len(res_data_list)
    # print(f"{res_data_list=}")
    start = (int(page) - 1) * int(limit)
    end = start + int(limit)
    # print(f"{start=},{end=}")
    res["data"] = res_data_list[start:end]

    return res
