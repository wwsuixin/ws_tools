from werkzeug.utils import secure_filename
import zipfile
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
from start_web.views.report.module.sqliteDbtools import *
from start_web.views.report.module.auto_report_shell import *

script_path = os.path.dirname(os.path.realpath(__file__))


tool_info = report_INFO  # 工具信息
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
工具输出绝对路径 = os.path.join(STATIC_OUTPUT_PATH, tool_name)
工具输出静态访问路径 = os.path.join("/static/output/", tool_name)
临时文件夹绝对路径 = os.path.join(工具输出静态访问路径, "tmp")
上传文件夹静态访问路径 = os.path.join(工具输出静态访问路径, "upload")
上传文件夹绝对路径 = os.path.join(工具输出绝对路径, "upload")
下载文件夹静态访问路径 = os.path.join(工具输出静态访问路径, "download")
下载文件夹绝对路径 = os.path.join(工具输出绝对路径, "download")
try:
    os.makedirs(上传文件夹绝对路径)
    os.makedirs(下载文件夹绝对路径)
except Exception as e:
    pass
targets_name = f"{tool_name}_targets.txt"  # 目标存放文件名称
target_file_path = os.path.join(res_output_path, targets_name)  # 目标存放路径
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径
db_file_name = f"{tool_name}.db"
db_file_path = os.path.join(WEB_ROOT_PATH, "views",
                            tool_name, "files", db_file_name)
docx_demo_file_name = "demo.docx"
docx_demo_file_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, "files", docx_demo_file_name
)


@bp.route(f"/{tool_name}/list")
def list():
    return render_template(
        f"{tool_name}/list.html",
        res=dict(
            h1="漏洞管理",
        ),
    )


@bp.route(f"/{tool_name}/vul_list")
def vul_list():
    return render_template(
        f"{tool_name}/vul_list.html",
        res=dict(
            h1="漏洞描述",
        ),
    )


@bp.route(f"/{tool_name}/add", methods=["GET", "POST"])
def add():
    method = request.method
    if method == "GET":
        data = request.args
    elif method == "POST":
        data = request.form
    else:
        data = {}
    # 添加漏洞--通过传入的id查询vul_info数据库，将对应的数据返回
    vul_id = data.get("id")
    db = sqlliteDBtool(db_filepath=db_file_path)
    tmp = {}

    sql = "SELECT * FROM vul_info WHERE id = ?;"
    param = (vul_id,)
    data_list = db.excuteQuery(sql, param)
    for item in data_list:
        tmp = item

    db.close()
    return render_template(
        f"{tool_name}/add.html",
        res=dict(h1="添加漏洞", data=tmp),
    )


# 【漏洞描述】功能
@bp.route(f"/{tool_name}/api/vul", methods=["GET", "POST"])
def api_vul():
    method = request.method
    if method == "GET":
        data = request.args
    elif method == "POST":
        data = request.form
    else:
        data = {}
    action = data["action"]
    tmp = []
    db = sqlliteDBtool(db_filepath=db_file_path)
    # 【漏洞描述】功能--查询
    if action == "program_list":
        sql = 'SELECT *  FROM "program" ORDER BY "id" ;'
        param = ()
        tmp = db.excuteQuery(sql, param)
    # 【漏洞描述】功能--添加功能
    if action == "add":
        sql = 'INSERT INTO "main"."program" ("vul_type_name", "vul_name", "vul_desc", "vul_repair", "vul_level") VALUES (?, ?, ?, ?, ?)'
        param = [
            (
                data.get("vul_type_name"),
                data.get("vul_name"),
                data.get("vul_desc"),
                data.get("vul_repair"),
                data.get("vul_level"),
            )
        ]
        res = db.executeUpdate(sql, param)
        if res == True:
            tmp = "添加成功"
        else:
            tmp = str(res)

    if action == "update":
        sql = 'UPDATE "main"."program" SET "vul_type_name"=?, "vul_name"=?,"vul_desc" = ?,"vul_repair"=?,"vul_level"=? WHERE rowid = ?'
        param = [
            (
                data.get("vul_type_name"),
                data.get("vul_name"),
                data.get("vul_desc"),
                data.get("vul_repair"),
                data.get("vul_level"),
                data.get("id"),
            )
        ]
        res = db.executeUpdate(sql, param)
        if res == True:
            tmp = "更新成功"
        else:
            tmp = str(res)
    # 【漏洞描述】---删除
    if action == "del":
        try:
            ids = data.get("ids")
            tmp_id_list = ids.split(",")
            # print(id_list)
        except Exception as e:
            return return_res(data=e)
        zhanwei_list = []
        id_list = []
        for i in tmp_id_list:
            if i == "":
                continue
            zhanwei_list.append("?")
            id_list.append(int(i))
        sql = (
            f"""DELETE FROM "main"."program"  WHERE id IN ({",".join(zhanwei_list)});"""
        )
        param = tuple(id_list)
        res = db.excuteDelete(sql, param)
        if res == True:
            tmp = "删除成功"
        else:
            tmp = res
    db.close()
    return return_res(data=tmp)


@bp.route(f"/{tool_name}/api", methods=["GET", "POST"])
def api():
    method = request.method
    if method == "GET":
        data = request.args
    elif method == "POST":
        data = request.form
    else:
        data = {}
    action = data["action"]
    tmp = []
    db = sqlliteDBtool(db_filepath=db_file_path)
    # 添加漏洞--获取已有项目名称
    if action == "report_center":
        sql = "SELECT DISTINCT report_center FROM vul_info;"
        param = ()
        data_list = db.excuteQuery(sql, param)
        for item in data_list:
            tmp.append(
                {
                    "name": item["report_center"],
                    "value": item["report_center"],
                    "selected": False,
                    "disabled": False,
                }
            )
    # 添加漏洞--获取漏洞类型
    if action == "vul_type_name":
        sql = "SELECT DISTINCT vul_type_name FROM program;"
        param = ()
        data_list = db.excuteQuery(sql, param)
        for item in data_list:
            tmp.append({"name": item["vul_type_name"],
                       "value": item["vul_type_name"]})
    # 添加漏洞--点击漏洞类型--获取漏洞名称

    if action == "vul_name":
        sql = "SELECT DISTINCT vul_name FROM program ;"
        param = ()
        data_list = db.excuteQuery(sql, param)
        for item in data_list:
            tmp.append({"name": item["vul_name"], "value": item["vul_name"]})
    # 添加漏洞--点击漏洞类型--点击漏洞名称--获取漏洞详情
    if action == "vul_info":
        vul_name = data["vul_name"]
        sql = "SELECT * FROM program WHERE vul_name = ?;"
        param = (vul_name,)
        data_list = db.excuteQuery(sql, param)
        for item in data_list:
            tmp.append(item)
    # 添加漏洞--保存漏洞
    if action == "save":
        # 添加漏洞--保存漏洞
        if action == "save":
            report_id = data.get("report_id")
            if report_id:
                sql = "UPDATE vul_info SET report_center=?, report_systemname=?, report_author=?, report_start_time=?, report_end_time=?, report_test_url=?, report_test_ip=?, vul_type_name=?, vul_name=?, vul_level=?, vul_url=?, vul_desc=?, vul_content=?, vul_repair=? WHERE id=?"
                param = [
                    (
                        data.get("report_center"),
                        data.get("report_systemname"),
                        data.get("report_author"),
                        data.get("report_start_time"),
                        data.get("report_end_time"),
                        data.get("report_test_url"),
                        data.get("report_test_ip"),
                        data.get("vul_type_name"),
                        data.get("vul_name"),
                        data.get("vul_level"),
                        data.get("vul_url"),
                        data.get("vul_desc"),
                        data.get("vul_content"),
                        data.get("vul_repair"),
                        report_id,
                    )
                ]
                data_list = db.executeUpdate(sql, param)
            else:
                sql = "INSERT INTO vul_info(report_center,report_systemname,report_author,report_start_time,report_end_time,report_test_url,report_test_ip,vul_type_name,vul_name,vul_level,vul_url,vul_desc,vul_content,vul_repair) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                param = [
                    (
                        data.get("report_center"),
                        data.get("report_systemname"),
                        data.get("report_author"),
                        data.get("report_start_time"),
                        data.get("report_end_time"),
                        data.get("report_test_url"),
                        data.get("report_test_ip"),
                        data.get("vul_type_name"),
                        data.get("vul_name"),
                        data.get("vul_level"),
                        data.get("vul_url"),
                        data.get("vul_desc"),
                        data.get("vul_content"),
                        data.get("vul_repair"),
                    )
                ]
                data_list = db.executeUpdate(sql, param)
            tmp = data_list

    # 添加漏洞---点击项目名称--获取系统名称
    if action == "report_systemname":
        report_center = data.get("report_center")
        sql = "SELECT DISTINCT report_systemname FROM vul_info WHERE report_center = ?;"
        param = (report_center,)
        data_list = db.excuteQuery(sql, param)
        for item in data_list:
            tmp.append(
                {"name": item["report_systemname"],
                    "value": item["report_systemname"]}
            )
    # 添加漏洞---点击项目名称--点击系统名称--获取测试uurl等信息

    if action == "report_test_url":
        try:
            report_center = data.get("report_center")
            report_systemname = data.get("report_systemname")
        except Exception as e:
            return return_res(data=tmp)

        # 获取访问地址并去重
        sql = "SELECT DISTINCT report_test_url FROM vul_info WHERE report_center = ? AND report_systemname = ? LIMIT 0,1;"
        param = (report_center, report_systemname)
        data_list = db.excuteQuery(sql, param)
        tmp = {
            "report_test_url": [],
            "report_author": [],
            "report_start_time": [],
            "report_end_time": [],
        }
        for item in data_list:
            tmp["report_test_url"].append(
                {"name": item["report_test_url"],
                    "value": item["report_test_url"]}
            )

        # 获取测试人员名称并去重
        sql = "SELECT DISTINCT report_author FROM vul_info WHERE report_center = ? AND report_systemname = ?;"
        param = (report_center, report_systemname)
        data_list = db.excuteQuery(sql, param)

        for item in data_list:
            tmp["report_author"].append(
                {"name": item["report_author"], "value": item["report_author"]}
            )
        # 获取测试日期并去重
        sql = "SELECT * FROM vul_info WHERE report_center = ? AND report_systemname = ? LIMIT 0,1;"
        param = (report_center, report_systemname)
        data_list = db.excuteQuery(sql, param)

        for item in data_list:
            tmp["report_start_time"] = item["report_start_time"]
            tmp["report_end_time"] = item["report_end_time"]
    # 报告管理-----获取漏洞列表
    if action == "vul_list":
        report_center = data.get("report_center")
        report_systemname = data.get("report_systemname")
        sql = 'SELECT *  FROM "vul_info" ;'
        param = ()
        if report_center:
            sql = 'SELECT *  FROM "vul_info" WHERE "report_center"=?;'
            param = (report_center,)
        if report_systemname:
            sql = 'SELECT *  FROM "vul_info" WHERE "report_center"=? AND "report_systemname"=? ;'
            param = (report_center, report_systemname)
        tmp = db.excuteQuery(sql, param)
    # 报告管理----报告导出
    if action == "report_export":
        try:
            report_center = data.get("report_center")
            report_systemname = data.get("report_systemname")
        except Exception as e:
            return return_res(data=tmp)
        data_list = []
        生成报告绝对路径列表 = []
        if report_systemname:
            # data_list.append(
            #     {
            #         report_center: report_center,
            #         report_systemname: report_systemname,
            #     }
            # )
            sql = 'SELECT DISTINCT report_systemname FROM vul_info WHERE report_center = ? AND "report_systemname"=?;'
            param = (
                report_center,
                report_systemname,
            )
            data_list = db.excuteQuery(sql, param)
        else:
            sql = "SELECT DISTINCT report_systemname FROM vul_info WHERE report_center = ?;"
            param = (report_center,)
            data_list = db.excuteQuery(sql, param)

        for i in data_list:
            report_systemname = i["report_systemname"]
            file_path = create_docx(
                report_center=report_center, report_systemname=report_systemname
            )
            生成报告绝对路径列表.append(file_path)
        压缩包文件名 = f"{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}_{report_center}.zip"
        压缩包文件绝对路径 = os.path.join(下载文件夹绝对路径, 压缩包文件名)
        压缩包文件访问路径 = os.path.join(下载文件夹静态访问路径, 压缩包文件名)

        fw = zipfile.ZipFile(压缩包文件绝对路径, "w", zipfile.ZIP_DEFLATED)
        for 生成报告绝对路径 in 生成报告绝对路径列表:
            fw.write(生成报告绝对路径, os.path.basename(生成报告绝对路径))
        fw.close()

        tmp = 压缩包文件访问路径
    # 报告管理---删除漏洞
    if action == "del":
        try:
            ids = data.get("ids")
            tmp_id_list = ids.split(",")
            # print(id_list)
        except Exception as e:
            return return_res(data=e)
        zhanwei_list = []
        id_list = []
        for i in tmp_id_list:
            if i == "":
                continue
            zhanwei_list.append("?")
            id_list.append(int(i))
        sql = f"""DELETE FROM vul_info WHERE id IN ({",".join(zhanwei_list)});"""
        param = tuple(id_list)
        data_list = db.excuteDelete(sql, param)
        tmp = "删除成功"

    db.close()
    return return_res(data=tmp)


@bp.route(f"/{tool_name}/api/upload", methods=["GET", "POST"])
def api_upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            if not (
                "." in filename
                and filename.rsplit(".", 1)[1].lower() in ["png", "jpg", "jpeg", "gif"]
            ):
                return "文件类型不支持"
            file.save(os.path.join(上传文件夹绝对路径, filename))
            文件相对路径 = os.path.join(上传文件夹静态访问路径, filename)
            return json.dumps({"location": 文件相对路径})

    return

    # f = open(res_path, "rb")
    # web.header('Content-Type', 'application/msword')
    # web.header('Content-Disposition', 'attachment;filename=' +
    #            quote(os.path.basename(res_path)))
    # return f.read()


def return_res(code=0, msg="success", data=[]):
    return json.dumps({"code": code, "msg": msg, "data": data})


def create_docx(report_center, report_systemname):
    db = sqlliteDBtool(db_filepath=db_file_path)

    sql = (
        'SELECT *  FROM "vul_info" WHERE "report_center"=? AND "report_systemname"=? ;'
    )
    param = (report_center, report_systemname)
    res = db.excuteQuery(sql, param)

    data = {
        "report_center": "",
        "report_systemname": "",
        "report_author": "",
        "report_start_time": "",
        "report_end_time": "",
        "report_test_url": "",
        "report_test_ip": "",
        "vuls": [],
    }
    for item in res:
        data["report_center"] = item["report_center"]
        data["report_systemname"] = item["report_systemname"]
        data["report_author"] = item["report_author"]
        data["report_start_time"] = item["report_start_time"]
        data["report_end_time"] = item["report_end_time"]
        data["report_test_url"] = item["report_test_url"]
        data["report_test_ip"] = item["report_test_ip"]
        data["vuls"].append(
            {
                "vul_name": item["vul_name"],
                "vul_url": item["vul_url"],
                "vul_level": item["vul_level"],
                "vul_content": item["vul_content"],
                "vul_desc": item["vul_desc"],
                "vul_repair": item["vul_repair"],
            }
        )
    docx报告输出名称 = f"{data['report_center']}_{data['report_systemname']}系统渗透测试报告_{time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))}.docx"
    docx报告输出绝对路径 = os.path.join(下载文件夹绝对路径, docx报告输出名称)
    auto_report_class = auto_report_shell(
        报告输出绝对路径=docx报告输出绝对路径, data=data, project_template=docx_demo_file_path
    )
    res = auto_report_class.auto_report()
    return docx报告输出绝对路径


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
