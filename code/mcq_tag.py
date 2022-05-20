"""
mcq_tag.py
coding:utf-8

Developed by @Luke.Tang 2022
This program cuts a level mcqs in pdfs to single question as image file.
For more information, please visit github.com/Clob4k/a-level-mcq-cutter
"""

import os
import cv2
import pytesseract


def create_path():
    # 创建缓存目录
    if not os.path.exists('D:\\Program_Design\\.info'):
        os.makedirs('D:\\Program_Design\\.info')


def create_info(pic_dir):
    img = cv2.imread(pic_dir, 1)
    text = pytesseract.image_to_string(img, lang='eng+equ')
    text = text.lower()
    for ch in ' \n':
        text = text.replace(ch, "")
    print(text)
    print("="*100)


def main():
    # 创建目录  
    create_path()

    # 获取目录下文件个数
    file_list = os.listdir("D:\\Program_Design\\.clip")

    # 切分每张图片
    for file in file_list:
        file_path = "D:\\Program_Design\\.clip\\{}".format(file)
        if os.path.exists(file_path):
            create_info(file_path)
            print("question extracted: " + file)
        else:
            pass

if __name__ == "__main__":  
    main()