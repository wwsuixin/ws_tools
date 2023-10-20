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


tool_info = nuclei_INFO  # 工具信息
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


@bp.route("/nuclei/")
def index():
    dir_name, full_file_name = os.path.split(tool_path)
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


# nuclei命令生成


def nuclei_exec(url_file="", plugins="", output_name=""):
    # -as 参数，先使用 wappalyzer 进行指纹识别，在进行扫描。
    # -exclude-id 排除规则id
    # -exclude-severity templates to exclude based on severity. Possible values: info, low, medium, high, critical, unknown

    shell = ""
    dir_name, full_file_name = os.path.split(tool_info["path"])
    output_path = f"""{os.path.join(res_output_path,f"{output_name}")}.txt"""
    output_path_dir, _ = os.path.split(output_path)

    nuclei_templates_path = os.path.join(dir_name, "nuclei-templates")

    shell = f"""cd '{dir_name}'; """
    shell += f""" .\{full_file_name} -templates {nuclei_templates_path} -exclude-severity info,low  -exclude-id  general-tokens,http-missing-security-headers,header-reflection-body,Application-dos,yonyou_NC_bsh_servlet_BshServlet -list {url_file} -me {os.path.join(res_output_path,output_name)} -output {output_path} """
    if plugins:
        shell += f""" -tags {plugins} """
    shell += f""";echo '------结果输出---------------------------------------';"""
    shell += f"""echo '{output_path}' ;"""

    return shell


@bp.route("/nuclei/update", methods=("POST",))
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
    # dir_name, full_file_name = os.path.split(NUCLEI_PATH)
    output_name = f"""{tool_name}_output-{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}"""

    # res['data'] = f'''cd '{dir_name}';'''
    # res['data'] += f''' .\{full_file_name} webscan --html-output {nuclei_OUTPUT_PATH} --url-file {target_file_path}'''
    # if plugins:
    #     res['data'] += f'''--plugins {plugins}'''
    res["data"] = nuclei_exec(
        url_file=target_file_path, plugins=plugins, output_name=output_name
    )
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
