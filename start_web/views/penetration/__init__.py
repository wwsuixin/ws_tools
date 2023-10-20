import re
from ...views.exec import shell_exec
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from start_web.config.settings import * 
import os
import time
tool_name = "penetration"
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",    # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)


@bp.route(f'/{tool_name}/', methods=('POST',))
def exp():
    shell = ""
    for i in PENETRATION_EXP_LIST:
        dir_name, full_file_name = os.path.split(i['path'])
        # print(f'''{i['version']=},{i['path']=}''')
        if "java" in i["version"]:
            shell += f'''cd '{dir_name}'; '''
            shell += f'''{eval(i['version'])} -jar .\{full_file_name} ;'''
        elif "python" in i["version"]:
            shell += f'''cd '{dir_name}'; '''
            shell += f'''{eval(i['version'])}  .\{full_file_name} ;'''
        else:
            shell += f'''{i['path']} ;'''
        shell += "\n"  # 拆分为多条命令同时执行,以回车分割
    print(shell)
    res = shell_exec(shell=shell)
    return res
    # return redirect('/index/', code=301)
