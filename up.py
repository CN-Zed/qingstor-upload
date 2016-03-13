# coding=utf-8
import os
import sys
import re
import qingcloud.qingstor


def each_files(path):
    global failed
    if os.access(path, os.R_OK):
        pass
    else:
        failed += 1
        print >> sys.stderr, "[%s] can not read!!!" % path
    if os.path.isfile(path):
        upload_file(path)
    else:
        try:
            files = os.listdir(path)
        except WindowsError:
            failed += 1
            print >> sys.stderr, "[%s] can not read!!!" % path
        else:
            for my_file in files:
                current = path + "\\" + my_file
                each_files(current)


def upload_file(path):
    global success, failed
    try:
        my_file = open(path)
    except IOError:
        failed += 1
        print >> sys.stderr, "[%s] can not be open!!!" % path
    else:
        key_name = path.replace(base_path, "").replace("\\", "/")
        if key_name[0] == "/":
            key_name = key_name[1:]
        key = bucket.new_key(key_name)
        if key.send_file(my_file, get_type(key_name)):
            print("[%s]上传成功。" % key_name)
            success += 1
        else:
            failed += 1
            print >> sys.stderr, "[%s] upload failed!!!" % key_name


def get_type(key_name):
    match = re.match("^.+/[^\.]+\.([a-zA-Z]+)$", key_name)
    if match:
        type_name = match.group(1)
        if type_name == "jpg" or type_name == "png" or type_name == "gif" or type_name == "jpeg":
            return "image/*"
        elif type_name == "txt":
            return "text/plain"
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    success, failed = 0, 0
    url = raw_input("请输入URL（PEK3A区直接回车）：")
    if url == "":
        url = "pek3a.qingstor.com"
    conn = qingcloud.qingstor.connect(url, raw_input("请输入Access Key："), raw_input("请输入Access Secret："))
    bucket_name = raw_input("请输入Bucket：")
    print("稍等，正在获取Bucket...")
    bucket = conn.get_bucket(bucket_name)
    print "connect complete:\t", bucket.stats()
    base_path = raw_input("请输入要上传的文件夹路径(or input 'q' to exit)：")
    if base_path == "q":
        print("终止程序，退出！")
        sys.exit()
    print("===========开始上传=========")
    each_files(base_path)
    print("===========开始结束=========")
    print("成功上传 {0:d} 个文件，{1:d} 个文件失败".format(success, failed))
