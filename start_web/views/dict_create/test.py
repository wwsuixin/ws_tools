import hashlib


def calculate_md5_16(string):
    md5_hash = hashlib.md5(string.encode()).hexdigest()
    md5_16 = md5_hash[:16]
    return md5_16


def md5_string_40(string):
    md5_hash = hashlib.md5(string.encode()).hexdigest()
    return md5_hash


def sha1_string(s):

    m = hashlib.sha1()

    m.update(s.encode('utf-8'))

    return m.hexdigest()


# 输入字符串
input_string = "sangfor"

# 计算 16 位 MD5 值
md5_16_result = sha1_string(input_string)

# 输出结果
print("16 位 MD5 值:", md5_16_result)
