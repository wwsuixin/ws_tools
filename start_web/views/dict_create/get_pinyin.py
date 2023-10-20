from xpinyin import Pinyin


def GET_PINYIN(string):
    if string == None:
        return None
    res_list = []
    # 获取中文全拼
    # pinyin_str = Pinyin().get_pinyin(string, "")
    # res_list+=[pinyin_str, pinyin_str.capitalize()]
    # 获取中文首拼
    pinyin_str = Pinyin().get_initials(string, "")
    # 中文首拼小写
    res_list.append(pinyin_str.lower())
    # 中文首拼首字母大写
    res_list.append(pinyin_str.capitalize())
    return res_list


if __name__ == '__main__':
    try:
        xingming_filepath = input("请输入中文姓名文件路径:")
        fr = open(xingming_filepath, 'r', encoding="utf-8")

        xingming_list = fr.read().splitlines()
        res_list = []
        for i in xingming_list:
            try:
                res_list.append(GET_PINYIN(i))
            except Exception as e:
                print(i, e)
        with open("./dict/kehu_xingming.txt", "w", encoding="utf-8") as fw:
            fw.write("\n".join(res_list))
        input("文件保存到./dict/kehu_xingming.txt中了,你可以运行字典碰撞md5了")
    except Exception as e:
        print(e)
        input()
