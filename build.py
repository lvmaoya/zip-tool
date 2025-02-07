# -*- coding: utf-8 -*-
# python 2.7
import os
import zipfile

# 初始版本号，你可以根据需要修改初始值
VERSION = 3
# 指定存放 ZIP 文件的文件夹
OUTPUT_FOLDER = 'output'

def zip_folder(folder_path, zipf):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 计算相对于当前工作目录的相对路径
            relative_path = os.path.relpath(file_path)
            zipf.write(file_path, relative_path)

def zip_files(files, zipf):
    for file in files:
        if os.path.isfile(file):
            # 计算相对于当前工作目录的相对路径
            relative_path = os.path.relpath(file)
            zipf.write(file, relative_path)

if __name__ == "__main__":
    # 要压缩的文件夹路径
    folder_to_zip = './testFolder'
    # 要压缩的文件列表
    files_to_zip = ['./test.html', './test.js']

    try:
        # 确保输出文件夹存在
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # 生成的 ZIP 文件路径，添加版本号，使用 str.format() 进行格式化
        zip_file_path = os.path.join(OUTPUT_FOLDER, 'output_v{}.zip'.format(VERSION))
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 检查文件夹是否存在
            if os.path.isdir(folder_to_zip):
                zip_folder(folder_to_zip, zipf)
            else:
                print("文件夹 %s 不存在，跳过。" % folder_to_zip)

            # 压缩文件
            zip_files(files_to_zip, zipf)

        # 累加版本号
        new_version = VERSION + 1
        # 动态修改脚本文件中的版本号
        with open(__file__, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("VERSION ="):
                lines[i] = "VERSION = {}\n".format(new_version)
        with open(__file__, 'w') as f:
            f.writelines(lines)

        print("已成功将文件和文件夹打包到 %s" % zip_file_path)
    except Exception as e:
        print("创建 ZIP 文件时出错: %s" % e)