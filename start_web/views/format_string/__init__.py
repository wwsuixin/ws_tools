import base64
import os
import json
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from start_web.config.settings import *

tool_info = format_string_INFO  # 工具信息
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
            h1="格式化字符串",  # h1标题
            tool_name=tool_name,  # 标题名称
            help_document=help_document,  # 帮助文件路径
            target_document=target_document,  # 目标文件路径
        ),
    )


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update(data=""):
    res = dict(code=0, msg="处理完成.", data=[])
    post_data = request.get_data()
    post_data = json.loads(post_data)
    data = post_data.get("data")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()
    res["data"] = format_string(old_data=data)

    return res


def format_string(old_data, format_type_list=["URL", "DOMAIN", "IP"]):
    import re

    line_list = old_data.split("\n")
    # 去重
    line_list = sorted(list(set(line_list)), key=line_list.index)
    new_line_list = []
    # 循环处理每行数据---初次处理原始数据
    for line in line_list:
        line = line.replace(" ", "")
        # 处理空行
        if line == "":
            continue
        # 处理空格开头字符串
        if re.match(r"^ .*", line):
            line_list.append(line.lstrip())
        # 处理同行多个域名情况
        for i in ["，", "；", ";", "、", "|", " "]:
            if i in line:
                line.replace(i, ",")
        if "," in line:
            line_list += line.split(",")
            continue
        # 添加到新列表中，处理规则须在上方添加
        new_line_list.append(line)
    # 二次去重
    new_line_list = sorted(list(set(new_line_list)), key=new_line_list.index)
    # 处理成url格式，头部添加http
    http_line_list = []
    if "URL" in format_type_list:
        tmp_new_line_list = new_line_list  # 防止处理数据污染其他规则
        for line in tmp_new_line_list:
            if not re.match(r"^https?:/{2}.*", line):
                tmp_new_line_list += ["http://" + line, "https://" + line]
                continue
            http_line_list.append(line)
        url_list = sorted(list(set(http_line_list)), key=http_line_list.index)
    # 处理成domain格式，提取域名
    domain_line_list = []
    if "DOMAIN" in format_type_list:
        tmp_new_line_list = new_line_list  # 防止处理数据污染其他规则
        for line in tmp_new_line_list:
            pattern = re.compile(
                r"\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b"
            )
            if pattern.search(line):
                domain_line_list.append(pattern.search(line)[0])
        domain_list = sorted(list(set(domain_line_list)), key=domain_line_list.index)
    # 处理成ip 格式，提取IP
    ip_line_list = []
    if "DOMAIN" in format_type_list:
        tmp_new_line_list = new_line_list  # 防止处理数据污染其他规则
        for line in tmp_new_line_list:
            pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
            if pattern.search(line):
                ip_line_list.append(pattern.search(line)[0])
        ip_list = sorted(list(set(ip_line_list)), key=ip_line_list.index)

    # 保存处理的数据
    return dict(
        url_list=url_list,
        domain_list=domain_list,
        ip_list=ip_list,
    )
    print(new_line_list)


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
