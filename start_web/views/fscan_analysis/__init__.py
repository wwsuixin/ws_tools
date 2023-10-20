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
import json
import re

tool_info = fscan_analysis_INFO  # 工具信息
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
ssh_file_path = f"""{os.path.join(res_output_path,f"ssh.txt")}"""
sql_file_path = f"""{os.path.join(res_output_path,f"sql.txt")}"""
web_file_path = f"""{os.path.join(res_output_path,f"web.txt")}"""
infoscan_file_path = f"""{os.path.join(res_output_path,f"infoscan.txt")}"""
other_file_path = f"""{os.path.join(res_output_path,f"other.txt")}"""
ms17010_file_path = f"""{os.path.join(res_output_path,f"ms17010.txt")}"""
ftp_file_path = f"""{os.path.join(res_output_path,f"ftp.txt")}"""


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
    ssh_content = ""
    try:
        fr = open(file=ssh_file_path, mode="r", encoding="utf-8")
        ssh_content = fr.read()
    except Exception as e:
        ssh_content = e
    sql_content = ""
    try:
        fr = open(file=sql_file_path, mode="r", encoding="utf-8")
        sql_content = fr.read()
    except Exception as e:
        sql_content = e
    web_content = ""
    try:
        fr = open(file=web_file_path, mode="r", encoding="utf-8")
        web_content = fr.read()
    except Exception as e:
        web_content = e
    other_content = ""
    try:
        fr = open(file=other_file_path, mode="r", encoding="utf-8")
        other_content = fr.read()
    except Exception as e:
        other_content = e
    infoscan_content = ""
    try:
        fr = open(file=infoscan_file_path, mode="r", encoding="utf-8")
        infoscan_content = fr.read()
    except Exception as e:
        infoscan_content = e
    ms17010_content = ""
    try:
        fr = open(file=ms17010_file_path, mode="r", encoding="utf-8")
        ms17010_content = fr.read()
    except Exception as e:
        ms17010_content = e
    ftp_content = ""
    try:
        fr = open(file=ftp_file_path, mode="r", encoding="utf-8")
        ftp_content = fr.read()
    except Exception as e:
        ftp_content = e
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1="fscan结果分析",
            tool_name=tool_name,
            path=tool_path,
            dir_path=dir_name,
            targets_name=targets_name,
            help_document=help_document,
            target_document=target_document,
            web_content=web_content,
            sql_content=sql_content,
            ssh_content=ssh_content,
            other_content=other_content,
            ftp_content=ftp_content,
            infoscan_content=infoscan_content,
            ms17010_content=ms17010_content,
            res_output_path=res_output_path,
            down_url=down_url,
            result_output_list=result_output_list,
            # form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            shell="",
        ),
    )


# 生成主动扫描命令


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    targets = post_data.get("targets")
    if targets:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write(targets)

        ssh_list = []
        sql_list = []
        web_list = []
        other_list = []
        infoscan_list = []
        ms17010_list = []
        ftp_list = []
        target_list = targets.split("\n")
        for line in range(len(target_list)):
            target = target_list[line]
            should_continue = False  # 标志变量
            if "[+] ftp" in target:
                ftp_list.append(target)
                for i in range(1, 7):
                    target = target_list[line + i]
                    if "   [->]" in target:
                        ftp_list.append(target)
                        continue
                    break
                continue
            if "MS17-010" in target:
                ms17010_list.append(target)
                continue
            if "[+] InfoScan" in target:
                infoscan_list.append(target)
                continue
            if "[+] SSH" in target:
                ssh_list.append(target)
                continue
            for i in ["mysql", "Redis", "mssql", "Memcached"]:
                if f"""[+] {i}""" in target:
                    should_continue = True
                    sql_list.append(target)
                    break
            if should_continue:
                continue
            for i in ["[*] WebTitle", "[+] http"]:
                if f"""{i}""" in target:
                    should_continue = True
                    web_list.append(target)
                    break
            if should_continue:
                continue
            other_list.append(target)
        ssh_list.sort()
        sql_list.sort()
        web_list.sort()
        infoscan_list.sort()
        ms17010_list.sort()
        with open(ftp_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(ftp_list))
            fw.close()
        with open(ms17010_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(ms17010_list))
            fw.close()
        with open(infoscan_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(infoscan_list))
            fw.close()
        with open(ssh_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(ssh_list))
            fw.close()
        with open(sql_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(sql_list))
            fw.close()
        with open(web_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(web_list))
            fw.close()
        with open(other_file_path, "w", encoding="u8") as fw:
            fw.write("\n".join(other_list))
            fw.close()
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
