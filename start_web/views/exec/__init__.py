import base64
import os
import json
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from start_web.config.settings import *

tool_name = "exec"
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)

res_output_path = os.path.join(STATIC_OUTPUT_PATH, tool_name)

targets_name = f"{tool_name}.ps1"  # 目标存放文件名称


@bp.route(f"/{tool_name}/")
def index():
    return render_template(f"{tool_name}/{tool_name}.html", res={"h1": "命令执行"})


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update(shell=""):
    post_data = request.get_data()
    post_data = json.loads(post_data)
    shell = post_data.get("shell")
    res = shell_exec(shell=shell)

    return res


def shell_exec(shell=""):
    try:
        os.makedirs(res_output_path)
    except Exception as e:
        pass
    res = dict(code=0, msg="开始执行,请查看cmd窗口")
    shell_list = shell.split("\n------------------------------\n")
    # print(f"{shell_list=}")
    i = 1
    if len(shell_list) > 0:
        for shell in shell_list:
            # print(f"{shell=}")
            if shell:  # 修复多个回车导致多次执行空命令bug
                # shell = shell.replace("\n", ";")
                # format_shell仿照linux echo “SGVsbG8sIFdvcmxkIQ==” |base64 -d 写一个powershell版本
                # encoded_command = base64.b64encode(shell.encode("utf-16-le")).decode("utf-8")
                target_file_path = os.path.join(
                    res_output_path, f"{i}.ps1"
                )  # 目标存放路径

                shell_res = f"""# ------------------------------------------------------------
Set-PSDebug -Trace 1
# 以下命令执行结束，请查看结果
# ------------------------------------------------------------
{shell}
# ------------------------------------------------------------
Get-Content '{target_file_path}'  | Select-Object -Skip 2  | Select-Object -SkipLast 1
"""
                with open(
                    target_file_path,
                    "w",
                    encoding="utf-8",
                ) as fw:
                    fw.write(shell_res)
                    fw.close()
                os.system(f"""start {PWSH_PATH} -NoExit -NoLogo {target_file_path}""")
                i += 1
    else:
        res["code"] = 1
        res["msg"] = "请输入需要执行的命令"
    return res
