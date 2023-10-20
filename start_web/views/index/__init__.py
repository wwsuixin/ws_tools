import json
import os
import requests
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from start_web.config.settings import *

tool_name = "index"  # 工具名称
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


@bp.route("/")
@bp.route(f"/index/")
def index():
    # ip_info = get_public_ip()
    ip_info = ""
    help_document = ""
    try:
        fr = open(file=help_documnet_path, mode="r", encoding="utf-8")
        help_document = fr.read()
    except Exception as e:
        pass
    # print(ip_info)
    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            ip_info=ip_info,
            h1=tool_name,
            tool_name=tool_name,  # 标题名称
            help_document=help_document,  # 帮助文件路径
        ),
    )


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update():
    res = dict(code=0, msg="执行成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode="w", encoding="utf-8") as fw:
            fw.write(help_document)
            fw.close()

    return res


def get_public_ip():
    url = "http://whois.pconline.com.cn/ipJson.jsp?json=true"
    ip_info_json = {"ip": "", "addr": ""}
    try:
        ip_info = requests.get(url=url, timeout=5)
        ip_info_json = ip_info.json()
    except Exception as e:
        pass
    # handle connection timeout error here
    return ip_info_json
