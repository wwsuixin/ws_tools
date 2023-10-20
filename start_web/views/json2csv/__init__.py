import base64
import os
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from start_web.config.settings import *

tool_name = "json2csv"
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",    # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, f"{tool_name}_document.txt")  # 帮助文档路径


@bp.route(f'/{tool_name}/')
def index():
    help_document = ""
    try:
        fr = open(file=help_documnet_path, mode="r", encoding="utf-8")
        help_document = fr.read()
    except Exception as e:
        pass
    return render_template(f'{tool_name}/{tool_name}.html', res=dict(
        h1="json转表格",  # h1标题
        tool_name=tool_name,  # 标题名称
        help_document=help_document,  # 帮助文件路径
    ))


@bp.route(f'/{tool_name}/update', methods=('POST',))
def update(data=""):
    res = dict(
        code=0,
        msg="处理完成.",
        data=[]
    )
    post_data = request.get_data()
    post_data = json.loads(post_data)
    data = post_data.get("data")
    help_document = post_data.get("help_document")
    if help_document:
        with open(file=help_documnet_path, mode='w', encoding="utf-8")as fw:
            fw.write(help_document)
            fw.close()
    res['msg']  = json2csv(json_data=data)

    return res


def json2csv(json_data):
    json_data = json.loads(json_data)
    res_list = []
    headers = []
    try:
        for name in json_data[0].keys():
            headers.append(name)
        res_list.append(",".join(headers))
        for item in json_data:
            # for id in item.values():
            #     try:
            #         id = id.replace("\r\n", "")
            #     except Exception as e:
            #         id = id
            #     res_list.append(",".join(f'''"{str(id)}"'''))

            res_list.append(",".join(f'''"{str(id)}"''' for id in item.values()))
            # res_list.append(",".join(str(id) for id in item.values()))
        res_str = "\n".join(res_list)
        res_bytes_utf8 = res_str.encode(encoding="utf-8")
        file_path = os.path.join(STATIC_OUTPUT_PATH, "json2csv.csv")
        
        with  open(file_path,"wb") as fw:
            fw.write(res_bytes_utf8)
            fw.close()
    except Exception as e :
        return str(e)
    return "处理完成"