"""
Author: wwsuixin
Date: 2022-02-09 09:31:53
LastEditors: wwsuixin
LastEditTime: 2022-02-09 17:56:24
Description: file content
"""
# -*- coding: utf-8 -*-
import pythoncom
import win32com.client as win32
import re
import os
import pypandoc
from docxtpl import DocxTemplate, InlineImage
import jinja2
import datetime
from docx import Document
import lxml
from docx.shared import Mm, Inches, Pt, Cm
from pathlib import Path
from PIL import Image
import time
from bs4 import BeautifulSoup
import base64
# 输入输出函数,用来获取目录路径


class auto_report_shell:
    def __init__(self, 报告输出绝对路径, data, project_template):
        self.报告输出绝对路径 = 报告输出绝对路径
        self.报告输出文件夹绝对路径 = os.path.dirname(os.path.dirname(报告输出绝对路径))

        self.报告输出文件夹绝对路径 = self.报告输出文件夹绝对路径
        self.REPORT_PATH = os.path.join(self.报告输出文件夹绝对路径, r"report")
        self.VULS_PATH = os.path.join(self.报告输出文件夹绝对路径, r"vuls")
        self.上传文件夹绝对路径 = os.path.join(self.报告输出文件夹绝对路径, r"upload")
        self.data = data
        self.project_template = project_template
        try:
            os.makedirs(self.REPORT_PATH)
            os.makedirs(self.VULS_PATH)
        except Exception as e:
            pass

    def auto_report(self):
        for i in range(0, len(self.data["vuls"])):
            vulno = "vul_" + str(i) + "_" + str(int(time.time()))
            htmlbody = self.data["vuls"][i]["vul_content"]
            soup = BeautifulSoup(htmlbody, "html.parser")
            num = 0
            image = []
            for img in soup.find_all("img"):
                src = img.get("src")
                # print(f"{src=}")
                if "data:image/png;base64," not in src:
                    imageid = "vul_img_" + \
                        os.path.basename(src).split(".")[0]
                else:
                    # 将base64图片保存到文件
                    img_data = src.split(",")[1]
                    image_name = f"base64_{num}"
                    imageid = f"vul_img_{image_name}"
                    with open(os.path.join(self.上传文件夹绝对路径, f"{image_name}.png"), "wb") as f:
                        f.write(base64.b64decode(img_data))
                    num += 1

                img["src"] = ""
                img.string = "{{" + imageid + "}}"
                image.append(imageid)
            self.data["vuls"][i]["image"] = image
            self.data["vuls"][i]["vul_content"] = "{{" + vulno + "}}"
            output = pypandoc.convert_text(
                soup,
                "docx",
                "html",
                outputfile=os.path.join(self.VULS_PATH, f"{vulno}.docx"),
            )
        # 替换漏洞相关信息##################
        tpl = DocxTemplate(self.project_template)
        context = self.data
        jinja_env = jinja2.Environment()
        jinja_env.filters["datetimeformat"] = datetimeformat
        jinja_env.filters["vul_statistics"] = vul_statistics
        tpl.render(context, jinja_env, autoescape=True)

        temp_filepath = os.path.join(self.REPORT_PATH, "temp.docx")
        tpl.save(temp_filepath)
        # exit()

        # 替换漏洞详情##################
        tpl1 = DocxTemplate(temp_filepath)

        vuls = {}
        for i in range(0, len(self.data["vuls"])):
            vulid = (
                self.data["vuls"][i]["vul_content"].replace(
                    "{", "").replace("}", "")
            )
            sub_doc = tpl1.new_subdoc(os.path.join(
                self.VULS_PATH, f"{vulid}.docx"))
            vuls[vulid] = sub_doc
        # print(vuls)
        tpl1.render(vuls)
        tpl1.save(temp_filepath)
        # exit()
        # 替换图片
        tpl2 = DocxTemplate(temp_filepath)
        images = {}
        for i in range(0, len(self.data["vuls"])):
            imageno = self.data["vuls"][i]["image"]
            for image in imageno:
                if "data:image/png;base64," not in image:
                    imageid = image.replace("vul_img_", "")
                    imageid_filepath = os.path.join(
                        self.上传文件夹绝对路径, f"{imageid}.png")
                    img = Image.open(imageid_filepath)
                    if img.width > 1600:
                        img = img.resize(
                            (1600, int(img.height * (1600 / img.width))))
                    a = InlineImage(tpl2, imageid_filepath, width=Cm(16))

                images[image] = a
        tpl2.render(images)
        tpl2.save(temp_filepath)

        set_updatefields_true(temp_filepath)

        docx_save(temp_filepath, self.报告输出绝对路径)

        return True


def set_updatefields_true(docx_path):
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    doc = Document(docx_path)
    # add child to doc.settings element
    element_updatefields = lxml.etree.SubElement(
        doc.settings.element, namespace + "updateFields"
    )
    element_updatefields.set(namespace + "val", "true")
    doc.save(docx_path)


# 更新目录


def docx_save(old_file_path, new_file_path):
    pythoncom.CoInitialize()
    word = win32.gencache.EnsureDispatch("Word.Application")
    # 启动word对象应用
    word.Visible = True

    doc = word.Documents.Open(old_file_path)

    doc.SaveAs(new_file_path)

    doc.Close()


# 时间格式化


def datetimeformat(value):
    utc_date = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_date = utc_date + datetime.timedelta(hours=8)
    local_date_str = datetime.datetime.strftime(local_date, "%Y-%m-%d")
    return local_date_str


# 漏洞统计
def vul_statistics(value, x):
    num = 0
    # print(x)
    for i in value:
        if i["vul_level"] == str(x):
            num = num + 1
    return num

    # if __name__ == '__main__':
    #     data = {
    #         "report_center": "测试项目",
    #         "report_systemname": "测试系统",
    #         "report_author": "作者",
    #         "report_start_time": "2022-02-08",
    #         "report_end_time": "2022-03-10",
    #         "vuls": [
    #             {
    #                 "vul_name": "Apache样例文件泄漏",
    #                 "vul_level": "1",
    #                 "vul_url": "http://127.0.0.1:8080/?name=%3C/script%3E",
    #                 "vul_content": '''
    #                 1钱钱钱钱钱钱钱钱钱钱钱
    #                 ''',
    #                 "vul_describe": "apache一些样例文件没有删除,可能存在cookie、session伪造,进行后台登录操作",
    #                 "vul_modify_repair": '''
    #                 1、删除样例文件
    # 2、对apache中web.xml进行相关设置
    #                 ''',
    #             }, {
    #                 "vul_name": "代码注入",
    #                 "vul_url": "http://127.0.0.2",
    #                 "vul_content": '''
    #                 1钱钱钱钱钱钱钱钱钱钱钱
    #                 ''',
    #                 "vul_level": "2",
    #                 "vul_recurrence": "123",
    #                 "vul_describe": "apache一些样例文件没有删除,可能存在cookie、session伪造,进行后台登录操作",
    #                 "vul_modify_repair": '''
    #                 1、删除样例文件
    # 2、对apache中web.xml进行相关设置
    #                 ''',
    #             }
    #         ]
    #     }

    #     auto_report(data=data, project_template="./demo/demo.docx")
