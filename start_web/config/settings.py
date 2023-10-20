"""
注意：
    定义的常量后不要有逗号
"""
import os

# 定义常量---禁止修改
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TMP_PATH = os.path.join(ROOT_PATH, "tmp")
TOOLS_PATH = os.path.join(ROOT_PATH, "tools")
OTHER_PATH = os.path.join(ROOT_PATH, "other")
DEPLOYMENT_PATH = os.path.join(ROOT_PATH, "deployment")
DEPLOYMENT_TOOLS_PATH = os.path.join(ROOT_PATH, "deployment_tools")
ENV_PATH = os.path.join(ROOT_PATH, "env")


WEB_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
STATIC_OUTPUT_PATH = os.path.join(WEB_ROOT_PATH, "static", "output")
CONFIG_PATH = os.path.join(WEB_ROOT_PATH, "config")
for i in [TMP_PATH, TOOLS_PATH, DEPLOYMENT_PATH, DEPLOYMENT_TOOLS_PATH]:
    try:
        os.makedirs(res_output_path)
    except Exception as e:
        pass


# 定义常用环境变量路径s
PWSH_PATH = os.path.join(ROOT_PATH, r"env\PowerShell\pwsh.exe")
PYTHON3_PATH = os.path.join(ROOT_PATH, r".venv\Scripts\python.exe")
BANDIZIP_PATH = os.path.join(ENV_PATH, r"BANDIZIP-PORTABLE\Bandizip.x64.exe")
JAVA15_PATH = r"C:\Penetration\ProgramTools\Java\jre15.0.2\bin\java.exe"
JAVA8_PATH = os.path.join(ENV_PATH, r"jre1.8\bin\java8.exe")
JAVA17_PATH = os.path.join(ENV_PATH, r"jre17\bin\java17.exe")
# 定义常用工具路径


# ProxyPoolxSocks
ProxyPoolxSocks_PATH = os.path.join(TOOLS_PATH, r"ProxyPoolxSocks\run.py")
ProxyPoolxSocks_DOWN_URL = "https://github.com/Anyyy111/ProxyPoolxSocks"
ProxyPoolxSocks_DIR, ProxyPoolxSocks_FILENAME = os.path.split(
    ProxyPoolxSocks_PATH)
ProxyPoolxSocks_EXEC = (
    f"""cd {ProxyPoolxSocks_DIR};{PYTHON3_PATH}  {ProxyPoolxSocks_FILENAME}"""
)
################################# 案例模板区域#######################################
# 功能开发模板
report_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "report",
}

# 外部页面模板
reverse_shell_generator_INFO = {
    "run_exec": "start",
    "version": "html",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"reverse_shell_generator\index.html"),
    "argv": """ f"  " """,
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"reverse_shell_generator.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "reverse_shell_generator",
}
# python直接运行案例模板
wxapp_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"wxapp\wxapp.py"),
    "argv": """ f" --intput_dirpath='{target_file_path}' --output_dirpath='{output_dir_path}' " """,
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"wxapp.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "wxapp",
}
# python-多个目标典型案例模板

dirsearch_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"dirsearch\dirsearch.py"),
    "argv": """ f"     --config='./config.ini'  --url-file='{target_file_path}' --output='{output_file_path}' " """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"dirsearch.zip")}""",
    "download_url": "https://github.com/maurosoria/dirsearch",
    "shell": "",
    "update_path": "",
    "name": "dirsearch",
}
# python-单个目标典型案例模板
dumpall_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"dumpall\dumpall.py"),
    "argv": """ f" --url='{target_file_path}' --outdir='{output_dir_path}' " """,
    "download_url": "https://github.com/0xHJK/dumpall",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"dumpall.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "dumpall",
}
# 文件夹案例模板
shiro_dirpath_INFO = {
    "run_exec": "",
    "version": "dir",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"shiro\\"),
    "argv": """""",
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"shiro.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "shiro_dirpath",
}

# exe-gui案例模板
antsword_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"antsword\antsword.exe"),
    "argv": """""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"antsword.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "antsword",
}
# java-gui案例模板
behinder_INFO = {
    "run_exec": JAVA17_PATH,
    "version": "java",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"behinder\Behinder.jar"),
    "argv": "   ",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"behinder.zip")}""",
    "download_url": "",
    "shell": f"""{JAVA17_PATH} -jar {os.path.join(TOOLS_PATH, r"behinder/Behinder.jar")}""",
    "update_path": "",
    "name": "behinder",
}
# 参数说明
# "run_exec": PYTHON3_PATH、JAVA17_PATH、JAVA15_PATH
# "version": python、exe、dir、java
# "path": DEPLOYMENT_TOOLS_PATH
# "argv": url_file-目标文件路径、output_path-输出文件路径、output_path_dir-输出文件目录
# "deployment_exec":解压命令
# "download_url":工具官网
# "shell": 默认命令，常用于gui软件开启
# "update_path": 更新脚本路径，暂时弃用
# "name": 工具名称，用于flask蓝图声明
# 参数说明-end
################################# 案例模板区域-end#######################################
github_proxy_LIST = [
    ['https://raw.fgit.cf', '香港',
        '[中国 香港] - 该公益加速源由 [FastGit 群组成员] 提供&#10;&#10; - 缓存：无（或时间很短）'],
    ['https://ghproxy.com/https://raw.githubusercontent.com', '韩国',
        '[日本、韩国、德国等]（CDN 不固定） - 该公益加速源由 [ghproxy] 提供&#10;&#10; - 缓存：无（或时间很短）'],
    ['https://fastly.jsdelivr.net/gh', '日本 1',
        '[日本 东京] - 该公益加速源由 [JSDelivr CDN] 提供&#10;&#10; - 缓存：有&#10; - 不支持大小超过 50 MB 的文件&#10; - 不支持版本号格式的分支名（如 v1.2.3）'],
    ['https://ghproxy.net/https://raw.githubusercontent.com',
        '日本 3', '[日本 大阪]&#10;&#10; - 缓存：无（或时间很短）'],
    ['https://gcore.jsdelivr.net/gh', '其他 1',
        '[移动走香港、电信走日本] - 该公益加速源由 [JSDelivr CDN] 提供&#10;&#10; - 缓存：有&#10; - 不支持大小超过 50 MB 的文件&#10; - 不支持版本号格式的分支名（如 v1.2.3）'],
    ['https://jsdelivr.b-cdn.net/gh', '其他 2',
        '[香港、台湾、日本、新加坡等]（CDN 不固定） - 该公益加速源由 [rttwyjz] 提供&#10;&#10; - 缓存：有'],
    ['https://github.moeyy.xyz/https://raw.githubusercontent.com',
        '其他 2', '[新加坡、香港、日本等]（CDN 不固定）&#10;&#10; - 缓存：无（或时间很短）'],
    ['https://raw.githubusercontent.com', 'Github 原生', '[日本 东京]'],
]
update_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "version_url": "https://raw.githubusercontent.com/test7911/deployment/main/version.json",
    "name": "update",
}
weblogic_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "weblogic",
}

format_string_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "format_string",
}

re_tool_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "re_tool",
}
ihoneyBakFileScan_Modify_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"ihoneyBakFileScan_Modify\ihoneyBakFileScan_Modify.py"),
    "argv": """ 
f"   -f '{target_file_path}'  -o '{output_file_path}' "  " 
""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"ihoneyBakFileScan_Modify.zip")}""",
    "download_url": "https://github.com/VMsec/ihoneyBakFileScan_Modify",
    "shell": "",
    "update_path": "",
    "name": "ihoneyBakFileScan_Modify",
}
bbscan_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"BBScan\w_BBScan.py"),
    "argv": """ 
f"  --no-browser  -f '{target_file_path}'  -o '{output_file_path}'  " 
""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"BBScan.zip")}""",
    "download_url": "https://github.com/lijiejie/BBScan",
    "shell": "",
    "update_path": "",
    "name": "bbscan",
}
urlfinder_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"urlfinder\urlfinder.exe"),
    "argv": """
f''' -s all -m 3 -f '{target_file_path}' -o '{output_file_path}' '''
""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"urlfinder.zip")}""",
    "download_url": "https://github.com/pingc0y/URLFinder",
    "shell": "",
    "update_path": "",
    "name": "urlfinder",
}
ak_search_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"ak_search\ak_search.py"),
    "argv": """ f" --input_dir_path='{target_file_path}' --output_file_path='{output_file_path}' " """,
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"ak_search.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "ak_search",
}
ip_create_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "ip_create",
}
edu_ip_search_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "edu_ip_search",
}
fscan_analysis_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "fscan_analysis",
}
server_login_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"server_login\server_login.py"),
    "argv": """ 
f''' --server_type='{plugins}'  --input_file_path='{target_file_path}' --output_file_path='{output_file_path}' ''' 
""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"server_login.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "server_login",
}

default_user_pass_dict_INFO = {
    "run_exec": "",
    "version": "",
    "path": "",
    "argv": """  """,
    "download_url": "",
    "deployment_exec": f"""""",
    "shell": "",
    "update_path": "",
    "name": "default_user_pass_dict",
}
finger_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"finger\Finger_w.py"),
    "argv": """ f"  -f '{target_file_path}' -o '{output_file_path}' " """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"finger.zip")}""",
    "download_url": "https://github.com/EASY233/Finger",
    "shell": "",
    "update_path": "",
    "name": "finger",
}

fofaviewer_INFO = {
    "run_exec": JAVA17_PATH,
    "version": "java",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"fofaviewer\fofaviewer.jar"),
    "argv": "   ",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"fofaviewer.zip")}""",
    "download_url": "",
    "shell": f"""{JAVA17_PATH} -jar {os.path.join(TOOLS_PATH, r"fofaviewer/fofaviewer.jar")}""",
    "update_path": "",
    "name": "fofaviewer",
}
fofamap_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"fofamap\fofamap.py"),
    "argv": """ 
f''' -q '{target_file_path}'  -o '{output_file_path}' '''
""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"fofamap.zip")}""",
    "download_url": "https://github.com/asaotomo/FofaMap",
    "shell": "",
    "update_path": "",
    "name": "fofamap",
}

ip2domain_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"ip2domain\w_ip2domain.py"),
    "argv": """ 
f'''  --icp --file='{target_file_path}' --output='{output_file_path}'   '''
""",
    "download_url": "https://github.com/Sma11New/ip2domain",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"ip2domain.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "ip2domain",
}


SocialEngineeringDictionaryGenerator_INFO = {
    "run_exec": "start",
    "version": "html",
    "path": os.path.join(
        DEPLOYMENT_TOOLS_PATH, r"SocialEngineeringDictionaryGenerator\index.html"
    ),
    "argv": """ f"  " """,
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"SocialEngineeringDictionaryGenerator.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "SocialEngineeringDictionaryGenerator",
}
heapdump_INFO = {
    "run_exec": JAVA17_PATH,
    "version": "java",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"heapdump\JDumpSpider.jar"),
    "argv": "   ",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"heapdump.zip")}""",
    "download_url": "",
    "shell": f"""{JAVA17_PATH} -jar {os.path.join(DEPLOYMENT_TOOLS_PATH, r"heapdump/JDumpSpider.jar")}""",
    "update_path": "",
    "name": "heapdump",
}
PackerFuzzer_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"PackerFuzzer\PackerFuzzer.py"),
    "argv": """ f"--silent -f 1 -r html -t adv --url='{target_file_path}' " """,
    "download_url": "https://github.com/rtcatc/Packer-Fuzzer",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"PackerFuzzer.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "PackerFuzzer",
}

xray_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"xray\xray.exe"),
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"xray.zip")}""",
    "argv": """ f"  --config ./config.yaml webscan  --url-file '{target_file_path}'  --plugins '{plugins}'  --html-output '{output_file_path}' " """,
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "xray",
}
xpoc_INFO = {
    "run_exec": " ",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"xpoc\xpoc_windows_amd64.exe"),
    "argv": """ f" --config xpoc-config.yaml --run '{plugins}' -i '{target_file_path}' -o '{output_file_path}'" """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"xpoc.zip")}""",
    "download_url": "https://stack.chaitin.com/tool/detail?id=1036",
    "shell": "",
    "update_path": "",
    "name": "xpoc",
}
nacosleak_INFO = {
    "run_exec": " ",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"nacosleak\nacosleak.exe"),
    "argv": """ f" -ts '{target_file_path}' -s '{output_dir_path}'" """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"nacosleak.zip")}""",
    "download_url": "https://github.com/a1phaboy/nacosleak/releases",
    "shell": "",
    "update_path": "",
    "name": "nacosleak",
}

oa_dirpath_INFO = {
    "run_exec": "",
    "version": "dir",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"oa\\"),
    "argv": """""",
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"oa.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "oa_dirpath",
}
godzilla_INFO = {
    "run_exec": JAVA15_PATH,
    "version": "java",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"godzilla\godzilla.jar"),
    "argv": "   ",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"godzilla.zip")}""",
    "download_url": "",
    "shell": f"""""",
    "update_path": "",
    "name": "godzilla",
}
Sunny_INFO = {
    "run_exec": "start",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"Sunny\Sunny.exe"),
    "argv": """""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"Sunny.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "Sunny",
}
fastgithub_INFO = {
    "run_exec": "start",
    "version": "exe",
    "name": "fastgithub",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"fastgithub\FastGithub.UI.exe"),
    "argv": """""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"fastgithub.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
}
burpsuite_INFO = {
    "run_exec": "start",
    "version": "vbs",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"burpsuite\burpsuite_pro\汉化启动.vbs"),
    "argv": """""",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"burpsuite.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "burpsuite",
}
MobaXterm_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"MobaXterm\MobaXterm.exe"),
    "argv": """""",
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"MobaXterm.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "MobaXterm",
}
redis_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(
        DEPLOYMENT_TOOLS_PATH,
        r"redis\redis.exe",
    ),
    "argv": """""",
    "download_url": "",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"redis.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "redis",
}
mdut_INFO = {
    "run_exec": JAVA8_PATH,
    "version": "java",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"mdut\mdut.jar"),
    "argv": """""",
    "download_url": "https://github.com/SafeGroceryStore/MDUT",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"mdut.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "mdut",
}
gorailgun_INFO = {
    "run_exec": "start",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"gorailgun\gorailgun.exe"),
    "argv": """""",
    "download_url": "https://dbeaver.io/download/",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"gorailgun.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "gorailgun",
}
dbeaver_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"dbeaver\dbeaver.exe"),
    "argv": """""",
    "download_url": "https://dbeaver.io/download/",
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"dbeaver.zip")}""",
    "shell": "",
    "update_path": "",
    "name": "dbeaver",
}


tidefinger_INFO = {
    "run_exec": " ",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"TideFinger\TideFinger.exe"),
    "argv": """ f" -pd  -uf '{target_file_path}' -o  '{output_file_path}'  " """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"TideFinger.zip")}""",
    "download_url": "",
    "shell": "",
    "update_path": "",
    "name": "tidefinger",
}


nuclei_INFO = {
    "run_exec": "",
    "version": "exe",
    "path": os.path.join(TOOLS_PATH, r"nuclei\nuclei.exe"),
    "deployment_exec": "",
    "argv": """""",
    "download_url": "https://github.com/projectdiscovery/nuclei",
    "shell": "",
    "update_path": "",
    "name": "nuclei",
}


enscan_INFO = {
    "run_exec": " ",
    "version": "exe",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"enscan\enscan.exe"),
    "argv": """ f" -f '{target_file_path}' -o '{output_dir_path}' " """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"enscan.zip")}""",
    "download_url": "https://github.com/wgpsec/ENScan_GO/",
    "shell": "",
    "update_path": "",
    "name": "enscan",
}


sqlmap_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"sqlmap\sqlmap.py"),
    "argv": """ f" --random-agent -o 10   -r '{target_file_path}' --output-dir='{output_dir_path}' --batch " """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"sqlmap.zip")}""",
    "shell": "",
    "update_path": "",
    "download_url": "https://github.com/sqlmapproject/sqlmap",
    "name": "sqlmap",
}
thinkphp_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"thinkphp\poc\TPscan\TPscan.py"),
    "argv": """ """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"thinkphp.zip")}""",
    "shell": "",
    "update_path": "",
    "download_url": "",
    "name": "thinkphp",
    "poc": [
        {
            "run_exec": PYTHON3_PATH,
            "version": "python",
            "path": os.path.join(
                DEPLOYMENT_TOOLS_PATH, r"thinkphp\poc\TPscan\TPscan.py"
            ),
            "argv": """   f" '{target_file_path}' > '{output_file_path}' ;cat '{output_file_path}' "  """,
            "download_url": "",
            "name": "TPscan",
        }
    ],
    "exp": [
        {
            "run_exec": JAVA8_PATH,
            "version": "java_gui",
            "path": os.path.join(
                DEPLOYMENT_TOOLS_PATH,
                r"thinkphp\exp\ThinkPHP_bewhale\ThinkPHP_bewhale.jar",
            ),
            "argv": """""",
            "download_url": "",
            "shell": "",
            "update_path": "",
            "name": "ThinkPHP_bewhale",
        },
        {
            "run_exec": JAVA8_PATH,
            "version": "java_gui",
            "path": os.path.join(
                DEPLOYMENT_TOOLS_PATH, r"thinkphp\exp\TPScan\TPScan.jar"
            ),
            "argv": """""",
            "download_url": "",
            "shell": "",
            "update_path": "",
            "name": "TPScan",
        },
    ],
}
# 多工具案例模板

INFO_PATH_LIST = []
info_INFO = {
    "run_exec": PYTHON3_PATH,
    "version": "python",
    "path": os.path.join(DEPLOYMENT_TOOLS_PATH, r"thinkphp\poc\TPscan\TPscan.py"),
    "argv": """ """,
    "deployment_exec": f"""{BANDIZIP_PATH} x -target:auto -o:{os.path.join(DEPLOYMENT_TOOLS_PATH)} {os.path.join(DEPLOYMENT_PATH,"thinkphp.zip")}""",
    "shell": "",
    "update_path": "",
    "download_url": "",
    "name": "info",
    "poc": [
        {
            "run_exec": PYTHON3_PATH,
            "version": "python",
            "path": os.path.join(TOOLS_PATH, r"BBScan-master\BBScan.py"),
            "argv": """ f" -f '{target_file_path}' " """,
        },
        {
            "run_exec": PYTHON3_PATH,
            "version": "python",
            "path": os.path.join(
                TOOLS_PATH, r"ihoneyBakFileScan_Modify-main\ihoneyBakFileScan_Modify.py"
            ),
            "argv": """ f" --thread 10   --url-file '{target_file_path}' --output-file '{output_file_path}' "  """,
        },
        {
            "run_exec": "",
            "version": "exe",
            "path": os.path.join(TOOLS_PATH, r"URLFinder\URLFinder-windows-amd64.exe"),
            "argv": """ f" -s all  -f '{target_file_path}' -o '{output_dir_path}' "  """,
        },
    ],
    "exp": [],
}


# 定义批量利用工具启动脚本路径,
# 仅支持GUI
# version参数必须是已定义的环境变量路径,exe程序此选项为空
# python脚本需要使用pdm虚拟环境启动


WEBLOGIC_EXP_LIST = [
    {
        "version": "JAVA8_PATH",
        "path": os.path.join(TOOLS_PATH, r"weblogic_exp\Java反序列化漏洞利用工具V1.7.jar"),
    },
    {
        "version": "JAVA8_PATH",
        "path": os.path.join(TOOLS_PATH, r"weblogic_exp\JAVA反序列化漏洞利用工具-WebLogic.jar"),
    },
    {
        "version": "JAVA8_PATH",
        "path": os.path.join(TOOLS_PATH, r"weblogic_exp\Java反序列化终极测试工具.jar"),
    },
    {
        "version": "JAVA8_PATH",
        "path": os.path.join(
            TOOLS_PATH, r"weblogic_exp\weblogic_exploit-1.0-SNAPSHOT-all.jar"
        ),
    },
    {
        "version": "JAVA8_PATH",
        "path": os.path.join(TOOLS_PATH, r"weblogic_exp\weblogic-framework.jar"),
    },
]
# 一键日站
PENETRATION_EXP_LIST = [
    {
        "version": "",
        "path": r"""C:\Users\Anonymous\Desktop\119-ws_start\Chrome\wschrome.exe""",
    },
    {
        "version": "",
        "path": r"C:\Users\Anonymous\AppData\Local\Programs\yakit\Yakit.exe",
    },
]
