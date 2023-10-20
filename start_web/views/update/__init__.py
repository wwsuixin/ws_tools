from werkzeug.utils import secure_filename
import requests
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

script_path = os.path.dirname(os.path.realpath(__file__))


tool_info = update_INFO  # 工具信息
tool_name = tool_info["name"]
tool_path = tool_info["path"]
down_url = tool_info["download_url"]
shell_str = tool_info["shell"]
update_path = tool_info["update_path"]
version_url = tool_info["version_url"]
deployment_exec = tool_info["deployment_exec"]
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)


file_dir, file_name = os.path.split(tool_path)


targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(res_output_path, targets_name)  # 目标存放路径
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径
version_name = f"version.json"
version_file_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, version_name
)  # 帮助文档路径


@bp.route(f"/{tool_name}/")
def index():
    return render_template(
        f"{tool_name}/index.html",
        res=dict(
            h1="工具管理",
        ),
    )


@bp.route(f"/{tool_name}/update", methods=['POST'])
def api_update():
    res = dict(code=0, msg="执行成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    name = post_data.get("name")
    update_url = post_data.get("url")
    url = ""
    for github_proxy in github_proxy_LIST:
        try:
            url = update_url.replace(
                "https://github.com", github_proxy[0])
            req = requests.head(url=url, timeout=5)
            if req.status_code == 200:
                break
        except Exception as e:
            print(f"{e=}")
            continue
    if not url:
        res['msg'] = "服务端网络异常,请科学上网"
        return res
    bak_name = f"{name}_{int(time.time())}"
    zip_name = f"{name}.zip"
    # 开始下载新版本文件
    shell_str = f'''
$path="{os.path.join(TMP_PATH,zip_name)}"
Invoke-WebRequest -Uri "{url}" -OutFile $path
'''
# 判断是否下载完成
    shell_str += '''
if (!(Test-Path -Path $path)) {
    Write-Host "File does not exist. Exiting program."
    pause
    exit
}
'''

    path = DEPLOYMENT_TOOLS_PATH
    if name == "start_web":
        path = ROOT_PATH

    # 备份旧版本
    shell_str += f'''
    $source="{os.path.join(path, name)}"
    $destination="{os.path.join(path, bak_name)}"
    Rename-Item -Path $source -NewName $destination
'''
# 开始解压新文件
    shell_str += f'''
{BANDIZIP_PATH} x -target:auto -o:{os.path.join(path)} {os.path.join(TMP_PATH,zip_name)}
'''
    shell_exec(shell_str)
    return res


@bp.route(f"/{tool_name}/list")
def api_list():
    version_list = []
    res = {"code": 0, "msg": "success", "data": []}
    for github_proxy in github_proxy_LIST:
        try:
            url = version_url.replace(
                "https://raw.githubusercontent.com", github_proxy[0])
            req = requests.get(url=url, timeout=5)
            if req.status_code == 200:
                version_list = req.json()
                break
        except Exception as e:
            print(f"{e=}")
            continue
    if len(version_list) == 0:
        res['msg'] = "服务端网络异常,请科学上网"
        return res
    with open(version_file_path, "r") as f:
        local_version_list = json.load(f)
    res_data_list = []
    num = 1
    for version_dict in version_list:
        name = version_dict['name']
        tmp_dict = version_dict
        tmp_dict['id'] = num
        num += 1
        version_path = os.path.join(DEPLOYMENT_TOOLS_PATH, name, "version.txt")
        if name == "start_web":
            version_path = os.path.join(ROOT_PATH, name, "version.txt")
        try:
            with open(version_path, "r") as f:
                tmp_dict['local_version'] = f.read().strip()
        except Exception as e:
            tmp_dict['local_version'] = ""
        tmp_dict['update_bool'] = 0
        if tmp_dict['local_version'] < tmp_dict['version']:
            tmp_dict['update_bool'] = 1
        res_data_list.append(tmp_dict)

    res['data'] = res_data_list
    return res
