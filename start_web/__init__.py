import os
from flask import Flask
from start_web.config.settings import *


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # 设置密钥
    )

    for i in [STATIC_OUTPUT_PATH]:
        try:
            os.makedirs(i)

        except OSError:
            pass

    # 注册 index 蓝图
    from .views import index
    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    # 注册其他蓝图
    from .views import (
        bbscan,
        sqlmap,
        fofaviewer,
        dirsearch,
        finger,
        dumpall,
        ip2domain,
        ip_attribution,
        fofamap,
        enscan,
        comprehensive_tool,
        xray,
        nuclei,
        tidefinger,
        xpoc,
        info,
        thinkphp,
        weblogic,
        oa_dirpath,
        heapdump,
        shiro_dirpath,
        nacosleak,
        dbeaver,
        mdut,
        redis,
        format_string,
        json2csv,
        dict_create,
        ip_create,
        re_tool,
        ak_search,
        gorailgun,
        avcheck,
        exec,
        ProxyPoolxSocks,
        test,
        MobaXterm,
        fastgithub,
        antsword,
        behinder,
        godzilla,
        penetration,
        clean,
        reverse_shell_generator,
        SocialEngineeringDictionaryGenerator,
        burpsuite,
        Sunny,
        wxapp,
        PackerFuzzer,
        report,
        default_user_pass_dict,
        server_login,
        fscan_analysis,
        edu_ip_search,
        urlfinder,
        ihoneyBakFileScan_Modify,
        update,
    )

    app.register_blueprint(update.bp)
    app.register_blueprint(ihoneyBakFileScan_Modify.bp)
    app.register_blueprint(bbscan.bp)
    app.register_blueprint(urlfinder.bp)
    app.register_blueprint(fscan_analysis.bp)
    app.register_blueprint(edu_ip_search.bp)
    app.register_blueprint(server_login.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(wxapp.bp)
    app.register_blueprint(enscan.bp)
    app.register_blueprint(sqlmap.bp)
    app.register_blueprint(fofaviewer.bp)
    app.register_blueprint(dirsearch.bp)
    app.register_blueprint(default_user_pass_dict.bp)
    app.register_blueprint(finger.bp)
    app.register_blueprint(dumpall.bp)
    app.register_blueprint(PackerFuzzer.bp)
    app.register_blueprint(ip2domain.bp)
    app.register_blueprint(ip_attribution.bp)
    app.register_blueprint(fofamap.bp)
    app.register_blueprint(SocialEngineeringDictionaryGenerator.bp)
    app.register_blueprint(avcheck.bp)
    app.register_blueprint(comprehensive_tool.bp)
    app.register_blueprint(xray.bp)
    app.register_blueprint(xpoc.bp)
    app.register_blueprint(nuclei.bp)
    app.register_blueprint(tidefinger.bp)
    app.register_blueprint(info.bp)
    app.register_blueprint(thinkphp.bp)
    app.register_blueprint(heapdump.bp)
    app.register_blueprint(weblogic.bp)
    app.register_blueprint(oa_dirpath.bp)
    app.register_blueprint(shiro_dirpath.bp)
    app.register_blueprint(nacosleak.bp)
    app.register_blueprint(dbeaver.bp)
    app.register_blueprint(mdut.bp)
    app.register_blueprint(redis.bp)
    app.register_blueprint(gorailgun.bp)
    app.register_blueprint(format_string.bp)
    app.register_blueprint(json2csv.bp)
    app.register_blueprint(dict_create.bp)
    app.register_blueprint(ip_create.bp)
    app.register_blueprint(re_tool.bp)
    app.register_blueprint(ak_search.bp)
    app.register_blueprint(exec.bp)
    app.register_blueprint(ProxyPoolxSocks.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(MobaXterm.bp)
    app.register_blueprint(fastgithub.bp)
    app.register_blueprint(burpsuite.bp)
    app.register_blueprint(Sunny.bp)
    app.register_blueprint(antsword.bp)
    app.register_blueprint(behinder.bp)
    app.register_blueprint(godzilla.bp)
    app.register_blueprint(penetration.bp)
    app.register_blueprint(clean.bp)
    app.register_blueprint(reverse_shell_generator.bp)

    return app
