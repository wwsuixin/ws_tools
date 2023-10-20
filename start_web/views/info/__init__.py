import shutil
import re
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

tool_info = info_INFO  # 工具信息
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


def info_exec(url_file="", plugins="", output_name=""):
    # eval(i['argv']) 内包含url_file ,output_name参数
    shell = ""
    for i in INFO_PATH_LIST:
        dir_name, full_file_name = os.path.split(i["path"])
        # print(f'''{i['version']=},{i['path']=}''')
        output_path = f"""{os.path.join(STATIC_OUTPUT_PATH,f"{output_name}_{full_file_name}")}.txt"""
        output_path_dir, _ = os.path.split(output_path)

        shell += f"""cd '{dir_name}'; """
        shell += f"""{i['run_exec']}  .\{full_file_name} {eval(i['argv'])};"""

        shell += "\n------------------------------\n"  # 拆分为多条命令同时执行,以回车分割
    print(shell)
    return shell


@bp.route(f"/{tool_name}/")
def index():
    # 同步结果到程序输出目录
    # bbscan_report_rsync()

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
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1="信息收集",  # h1标题
            tool_name=tool_name,  # 标题名称
            targets_name=targets_name,  # 目标文件名称
            help_document=help_document,  # 帮助文件路径
            target_document=target_document,  # 目标文件路径
            result_path=STATIC_OUTPUT_PATH,  # 结果路径
            result_output_list=result_output_list,  # 结果列表
            form_run="true",  # 运行按钮
            form_create="true",  # 运行按钮
        ),
    )


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
    # dir_name, full_file_name = os.path.split(info_path)
    output_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    output_name = f"{tool_name}_output-{output_time}"
    # data_list = [
    #     bbscan_exec(url_file=target_file_path),
    #     ihoneyBakFileScan_Modify_exec(
    #         url_file=target_file_path, output_name=output_name_ihoneyBakFileScan_Modify)
    # ]
    # 前台显示需要换行
    # res["data"] = "\n".join(data_list)
    res["data"] = info_exec(url_file=target_file_path, output_name=output_name)
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