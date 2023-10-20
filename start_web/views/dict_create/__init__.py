import base64
import os
import json
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import time
from start_web.config.settings import *
from start_web.views.dict_create.get_pinyin import *
from tqdm import tqdm
import hashlib

tool_name = "dict_create"
bp = Blueprint(
    tool_name,
    __name__,
    template_folder="../",  # 模版目录, 相对路径
    # static_folder="static",         # 静态文件目录, 相对路径
    # url_prefix="/example"           # 蓝图 url 前缀
)

# 定义输出目录-start
res_output_path = os.path.join(STATIC_OUTPUT_PATH, tool_name)
try:
    os.makedirs(res_output_path)
except Exception as e:
    pass
# 定义输出目录-end


# 定义帮助文档信息-start
help_documnet_name = f"{tool_name}_help_document.txt"  # 帮助文件名称
help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, help_documnet_name
)  # 帮助文档路径
# 定义帮助文档信息-end

help_documnet_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, f"{tool_name}_document.txt"
)  # 帮助文档路径

username_dict_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, "dicts", f"username_dict.txt"
)  # 用户字典路径
password_dict_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, "dicts", f"password_dict.txt"
)  # 密码字典路径
default_password_path = os.path.join(
    WEB_ROOT_PATH, "views", tool_name, "dicts", f"deafult_password.txt"
)  # 密码字典路径

output_default_md5_path = os.path.join(res_output_path, f"default_md5.txt")
output_default_pinyin_path = os.path.join(res_output_path, f"default_pinyin.txt")
output_password_path = os.path.join(res_output_path, f"password.txt")
output_result_demd5_path = os.path.join(res_output_path, f"result_demd5.txt")


@bp.route(f"/{tool_name}/")
def index():
    help_document = ""
    try:
        fr = open(file=help_documnet_path, mode="r", encoding="utf-8")
        help_document = fr.read()
    except Exception as e:
        pass

    # 读取用户字典显示到前端
    username_str = ""
    try:
        fr = open(file=username_dict_path, mode="r", encoding="utf-8")
        username_str = fr.read()
    except Exception as e:
        pass
    # 读取密码字典显示到前端
    password_str = ""
    try:
        fr = open(file=password_dict_path, mode="r", encoding="utf-8")
        password_str = fr.read()
    except Exception as e:
        pass
    # 读取默认口令显示到前端
    default_password_str = ""
    try:
        fr = open(file=default_password_path, mode="r", encoding="utf-8")
        default_password_str = fr.read()
    except Exception as e:
        pass

    return render_template(
        f"{tool_name}/{tool_name}.html",
        res=dict(
            h1=f"字典工具-{tool_name}",  # h1标题
            targets_name=f"{tool_name}.txt",
            tool_name=tool_name,  # 标题名称
            help_document=help_document,  # 帮助文件路径
            # target_document=target_document,  # 目标文件路径
            username_str=username_str,  # 用户字典
            password_str=password_str,  # 密码字典
            default_password_str=default_password_str,  # 默认口令字典
            result_path=output_result_demd5_path,
        ),
    )


global TOP1000_LIST, TOP100_LIST, TOP10_LIST, FUHAO_LIST
# 读取top1000
fr = open(os.path.join(ENV_PATH, "dicts", "top1000.txt"), "r", encoding="utf-8")
TOP1000_LIST = fr.read().splitlines()
# 读取top100
fr = open(os.path.join(ENV_PATH, "dicts", "top100.txt"), "r", encoding="utf-8")
TOP100_LIST = fr.read().splitlines()
# 读取top10
fr = open(os.path.join(ENV_PATH, "dicts", "top10.txt"), "r", encoding="utf-8")
TOP10_LIST = fr.read().splitlines()


@bp.route(f"/{tool_name}/update", methods=("POST",))
def update(data=""):
    global TOP1000_LIST, TOP100_LIST, TOP10_LIST, FUHAO_LIST
    res = dict(code=0, msg="处理完成.", data=[])
    post_data = request.get_data()
    post_data = json.loads(post_data)
    # 定义变量

    password_list = []  # 统计所有数据，写入字典文件中

    print("开始处理...内置拼音字典")
    start_time = time.time()
    # 内置拼音字典MD5值是否生成-来源于somd5
    default_pinyin_list = []  # 读取内置字典，数据量较大，用top10
    default_password_list = []
    # 添加常用字典用于生成默认md5
    default_pinyin_filepath = output_default_pinyin_path
    if not os.path.exists(default_pinyin_filepath):
        with open(
            os.path.join(ENV_PATH, "dicts", "somd5_pinyin.txt"), "r", encoding="utf-8"
        ) as fr:
            default_pinyin_list = fr.read().splitlines()
        for string in tqdm(default_pinyin_list):
            default_password_list += password_create(string, "top10")
        default_pinyin_list = list(set(default_pinyin_list))
        with open(default_pinyin_filepath, "w", encoding="utf-8") as fw:
            fw.write("\n".join(default_password_list))
            fw.close()
    else:
        print("开始处理...内置拼音字典已存在，如需重置请删除dict_create_default_pinyin.txt文件")

    print(f"耗时：{time.time()-start_time}")
    # 中文姓名转换为首字母
    print("开始处理...中文姓名转换为首字母")
    start_time = time.time()
    xingming = post_data.get("xingming")
    xingming_list = []
    if xingming != None:
        tmp_xingming_list = xingming.splitlines()
        for xingming_str in tqdm(list(set(tmp_xingming_list))):
            # 过滤左右空格
            xingming_str = xingming_str.strip()
            # 判断是否空行
            if len(xingming_str) == 0:
                continue
            tmp = GET_PINYIN(xingming_str)
            for i in tmp:
                if i not in xingming_list:  # 判断是否已经处理过
                    password_list += password_create(i, "top100")
                    xingming_list.append(i)  # 处理过的拼音放入列表中
    print(f"耗时：{time.time()-start_time}")

    # 关键词处理
    print("开始处理...关键词")
    start_time = time.time()
    keyword_list = []  # 前台传入的关键词数据 ，数据量最少，用top1000
    keyword = post_data.get("keyword")
    if keyword != None:
        tmp_keyword_list = keyword.splitlines()
        tmp_keyword_list = list(set(tmp_keyword_list))
        for keyword_str in tqdm(tmp_keyword_list):
            # 过滤左右空格
            keyword_str = keyword_str.strip()
            # 判断是否空行
            if len(keyword_str) == 0:
                continue
            # keyword本身作为字典
            password_list.append(keyword_str)
            # keyword组合字符作为字典
            password_list += password_create(keyword_str, "top1000")
    print(f"耗时：{time.time()-start_time}")
    # 去重处理
    print("开始字典去重")
    start_time = time.time()
    password_list = set(list(password_list))
    print(f"生成字典数量：{len(password_list)}")
    print(f"耗时：{time.time()-start_time}")

    with open(file=output_password_path, mode="w", encoding="utf-8") as fw:
        fw.write("\n".join(password_list))
        fw.close()
    return res


@bp.route(f"/{tool_name}/contrast", methods=("POST",))
def contrast():
    res = dict(code=0, msg="字典不够强呀！", data=[])
    post_data = request.get_data()
    post_data = json.loads(post_data)
    md5 = post_data.get("md5").strip()
    if len(md5) == 0:
        res["msg"] = "md5为空，无法比较"
        return res
    md5_list = md5.splitlines()
    md5_list = list(set(md5_list))
    md5_lower_list = []
    for i in md5_list:  # 循环前台的md5值并转为小写
        if len(i) == 0:
            continue
        md5_lower_list.append(i.lower())
    # 判断md5版本
    md5_type = 0
    if len(md5_lower_list[0]) == 16:
        md5_type = 16
    if len(md5_lower_list[0]) == 32:
        md5_type = 32
    if len(md5_lower_list[0]) == 40:
        md5_type = 40
    # 读取默认字典
    default_md5_list = []
    print("开始处理......默认字典")
    start_time = time.time()
    try:
        with open(output_default_md5_path, "r", encoding="utf-8") as fr:
            default_md5_list = fr.read().splitlines()
    except Exception as e:
        print("开始处理......默认字典不存在，初始化一下")
        fr = open(
            os.path.join(res_output_path, "default_pinyin.txt"),
            "r",
            encoding="utf-8",
        )
        default_pinyin_list = fr.read().splitlines()
        default_pinyin_list = (
            default_pinyin_list + TOP1000_LIST + TOP100_LIST + TOP10_LIST
        )
        for string in tqdm(default_pinyin_list):
            if md5_type == 16:
                default_md5_list.append(f"{md5_string_16(string).lower()}\t{string}")
            if md5_type == 32:
                default_md5_list.append(f"{md5_string_32(string).lower()}\t{string}")
            if md5_type == 40:
                default_md5_list.append(f"{md5_string_40(string).lower()}\t{string}")

        with open(
            os.path.join(res_output_path, "dict_create_default_md5.txt"),
            "w",
            encoding="utf-8",
        ) as fw:
            fw.write("\n".join(default_md5_list))
            fw.close()
    print(f"耗时:{time.time()-start_time}")
    print("开始......通过默认字典查找MD5 ")
    with open(output_result_demd5_path, "a", encoding="utf-8") as fw:
        fw.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        fw.close()
    del_list = []
    for i in tqdm(default_md5_list):  # 循环默认字典
        for j in md5_lower_list:  # 循环前台获取的md5
            if j in i:
                print(f"\n{i}\n")
                with open(output_result_demd5_path, "a", encoding="utf-8") as fw:
                    fw.write(f"{i}\n")
                    fw.close()
                del_list.append(i.split()[1])
                res["msg"] = "出货了......"
                break

    print("开始......通过密码字典查找MD5")

    # 读取密码字典
    with open(output_password_path, "r", encoding="utf-8") as fr:
        password_list = fr.read().splitlines()
    # 删除已经解密的MD5
    password_list = list(set(password_list).difference(set(del_list)))
    # 计算每一行字符串的md5值
    for string in tqdm(password_list):
        if md5_type == 16:
            md5 = md5_string_16(string)
        if md5_type == 32:
            md5 = md5_string_32(string)
        if md5_type == 40:
            md5 = md5_string_40(string)
        md5_lower = md5.lower()
        if md5_lower in md5_lower_list:
            tmp_res_str = f"{md5_lower}\t{string}"
            print(f"\n{tmp_res_str}\n")
            with open(output_result_demd5_path, "a", encoding="utf-8") as fw:
                fw.write(f"{tmp_res_str}\n")
                fw.close()
            res["msg"] = "出货了......"

    return res


# 计算字符串16位md5
def md5_string_16(string):
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()[:8]


# 计算字符串32位md5
def md5_string_32(string):
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


# 计算字符串40位md5


def md5_string_40(string):
    m = hashlib.sha1()
    m.update(string.encode("utf-8"))
    return m.hexdigest()


def password_create(string, password_type):
    FUHAO_LIST = "!@._~-"
    res_list = []
    if password_type in ["top1000"]:
        # 获取今年年份
        CURRENT_YEAR = int(time.strftime("%Y", time.localtime(time.time())))
        for i in range(1970, CURRENT_YEAR + 1):
            # 用户名+年份
            res_list.append(f"{string}{i}")
            # 用户名+符号+年份
            for j in FUHAO_LIST:
                res_list.append(f"{string}{j}{i}")

    top_list = TOP10_LIST
    if password_type == "top100":
        top_list = TOP100_LIST
    if password_type == "top1000":
        top_list = TOP1000_LIST
    for i in top_list:
        if len(top_list) < 1000:
            # 用户名+符号+top1000
            for j in FUHAO_LIST:
                res_list.append(f"{string}{j}{i}")
        else:
            res_list.append(f"{string}{i}")
            res_list.append(f"{string}@{i}")
            res_list.append(f"{string}{i}!")
    return res_list


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


@bp.route(f"/{tool_name}/save_username", methods=("POST",))
def save_username():
    res = dict(code=0, msg="用户字典保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    res_str = post_data.get("username_str")
    res_list = list(res_str.split("\n"))
    res_list = [x.strip() for x in res_list]
    res_list = list(set(res_list))
    if len(res_list) > 0:
        with open(file=username_dict_path, mode="w", encoding="utf-8") as fw:
            fw.write("\n".join(res_list))
            fw.close()
    return res


@bp.route(f"/{tool_name}/save_password", methods=("POST",))
def save_password():
    res = dict(code=0, msg="密码字典保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    res_str = post_data.get("password_str")
    res_list = list(res_str.split("\n"))
    res_list = [x.strip() for x in res_list]
    res_list = list(set(res_list))
    if len(res_list) > 0:
        with open(file=password_dict_path, mode="w", encoding="utf-8") as fw:
            fw.write("\n".join(res_list))
            fw.close()
    return res


@bp.route(f"/{tool_name}/save_default_password", methods=("POST",))
def save_default_password():
    res = dict(code=0, msg="默认口令保存成功", data="")
    post_data = request.get_data()
    post_data = json.loads(post_data)
    res_str = post_data.get("default_password_str")
    # res_list = list(res_str.split("\n"))
    # res_list = [x.strip() for x in res_list]
    # res_list = list(set(res_list))
    if res_str:
        with open(file=default_password_path, mode="w", encoding="utf-8") as fw:
            # fw.write("\n".join(res_list))
            fw.write(res_str)
            fw.close()
    return res
