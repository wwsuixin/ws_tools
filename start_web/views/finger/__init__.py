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

tool_info = finger_INFO  # 工具信息
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
    # print(e)
    pass
targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(res_output_path, targets_name)  # 目标存放路径
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径

config_file_name = f"config.py"  # 配置文件名称
config_file_path = os.path.join(file_dir,"config", config_file_name)


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
    # 读取配置文件并回显
    config_file_content = ""
    try:
        fr = open(file=config_file_path, mode="r", encoding="utf-8")
        config_file_content = fr.read()
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
            result_output_list=result_output_list,
            down_url=down_url,
            form_run="true",  # 运行按钮
            form_create="true",  # 生成按钮
            shell="",
            config_file_content=config_file_content,
        ),
    )


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="命令生成成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    targets = post_data.get("targets")
    target_list = targets.split("\n")
    target_list = [x.strip() for x in target_list]
    if len(target_list) > 0:
        with open(target_file_path, "w", encoding="utf-8") as fw:
            fw.write("\n".join(target_list))
    output_time = (
        f"""{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}"""
    )
    output_file_path = f"""{os.path.join(res_output_path,f"{output_time}")}.html"""

    res["data"] = finger_exec(target_file_path=target_file_path, output_file_path=output_file_path)
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


@bp.route(f"/{tool_name}/tool_init", methods=("POST",))
def tool_init():
    res = dict(code=0, msg="工具初始化成功", data="")
    shell_exec(deployment_exec)
    return res


def finger_exec(target_file_path="", plugins="", output_file_path=""):
    shell = ""

    dir_name, full_file_name = os.path.split(tool_info["path"])
    output_dir_path, output_file_name = os.path.split(output_file_path)
    if tool_info["version"] == "python" or tool_info["version"] == "exe":
        shell = f"""cd '{dir_name}';
{tool_info['run_exec']}  .\{full_file_name} {eval(tool_info['argv'])};
"""
        return shell
    if tool_info["version"] == "java" or tool_info["version"] == "java_gui":
        shell = f"""cd '{dir_name}';
{tool_info['run_exec']}  -jar  .\{full_file_name} {eval(tool_info['argv'])};
"""
        return shell
    return "请检查version版本是否兼容"



@bp.route(f"/{tool_name}/save_config_file", methods=("POST",))
def save_config_file():
    res = dict(code=0, msg="配置文件保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    config_file = post_data.get("config_file")
    if config_file:
        with open(file=config_file_path, mode="w", encoding="utf-8") as fw:
            fw.write(config_file)
            fw.close()
    return res

