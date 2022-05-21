"""
mcq_cutter.py
coding:utf-8

Developed by @Luke.Tang 2022
This program cuts a level mcqs in pdfs to single question as image file.
For more information, please visit github.com/Clob4k/a-level-mcq-cutter
"""

import os
import cv2
import fitz

# A4 Raw 
# image pixel : (841.89, 595.28)
# image-gen
# image shape : (2105, 1488, 3)


def sep_line():
    print("=" * 50)



def access_pixels(image):
    # 存储题目左上角像素的值
    location = []
    img_height = image.shape[0]
    img_width = image.shape[1]
    skip_pixel = 120
    skip_pixel_flag = False
    count = 0
    for row in range(img_height):
        for col in range(img_width):
            if skip_pixel_flag:
                # 忽略掉来自同一数字的黑色像素
                count += 1
                if count == skip_pixel:
                    skip_pixel_flag = False
                continue
            else:
                pixel = image[row , col]              
                if pixel[0] == 0:
                    location.append(row)
                    skip_pixel_flag = True
                    count = 0
    return location


def delete_blank(question_zone):
    retval, question_zone_bi = cv2.threshold(question_zone, 127, 255, cv2.THRESH_BINARY)
    q_height = question_zone_bi.shape[0]
    q_width = question_zone_bi.shape[1]
    ignore_wid = int(q_width * (52.25/595.28))
    for row in range(0,q_height,20):
        inv_height = q_height - row - 1
        for col in range(ignore_wid, q_width-ignore_wid, 5):
            pixel = question_zone_bi[inv_height, col]
            if pixel[0] == 0:
                return inv_height
    return q_height


def create_path():
    # 创建缓存目录
    # tem_dir = os.path.normpath(current_dir + "\\.temp")
    # if not os.path.exists(tem_dir):
    #    os.makedirs(tem_dir)
    # 创建题目目录
    que_dir = os.path.normpath(current_dir + "\\.clip")
    if not os.path.exists(que_dir):
        os.makedirs(que_dir)
    # 创建PDF目录
    img_dir = os.path.normpath(current_dir + "\\.pdf")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)


def pdf_to_image(path):
    name = os.path.basename(path)
    pdf = fitz.open(path)
    zx = zy = 2.5
    for i, page in enumerate(pdf):
        # 输出序号：三位以下向左填充"0"
        index = str(i).rjust(3,'0')
        pic_dir = os.path.normpath(current_dir + "\\.pdf\\{}_Page_{}.jpg".format(name[:-4], index))
        if os.path.exists(pic_dir):
            continue
        else:
            mat = fitz.Matrix(zx, zy).preRotate(0)
            pix = page.getPixmap(matrix=mat)
            pix.writePNG(pic_dir)
            print("image extracted: " + os.path.basename(pic_dir))


def clip(pic_dir):
    # 读取图片
    file_name = os.path.basename(pic_dir)
    img = cv2.imread(pic_dir, 1)
    height = img.shape[0]
    width = img.shape[1]

    # 题目间距
    gap_val = int(height * (15/841.89))

    # 裁剪区坐标
    delete_zone_height = int(height * (50/841.89))
    delete_zone_width = width

    # 检查区坐标
    # check_zone_width = int(width * (64/595.28))
    # check_zone_height = height
    check_line_start = int(width * (52.25/595.28))
    check_line_end = check_line_start + 4

    # 裁剪坐标为[y0:y1, x0:x1]
    delete_zone_1 = img[0:delete_zone_height, 0:delete_zone_width]
    delete_zone_2 = img[height-delete_zone_height:height, 0:width]
    #check_zone = img[0:check_zone_height, 0:check_zone_width]
    check_line = img[0:height-delete_zone_height, check_line_start:check_line_end]

    # 写入裁剪区域
    # cv2.imwrite(os.path.normpath(current_dir + "\\.temp\\temp_delete_zone_1.jpg"), delete_zone_1)
    # cv2.imwrite(os.path.normpath(current_dir + "\\.temp\\temp_delete_zone_2.jpg"), delete_zone_2)
    # cv2.imwrite(os.path.normpath(current_dir + "\\.temp\\temp_check_zone.jpg"), check_zone)
    # cv2.imwrite(os.path.normpath(current_dir + "\\.temp\\temp_line_zone.jpg"), check_line)

    # 生成二值图像
    # retval: 阈值
    # check_zone_bi: 处理后的图像
    retval, check_line_bi = cv2.threshold(check_line, 127, 255, cv2.THRESH_BINARY)
    # cv2.imwrite(os.path.normpath(current_dir + "\\.temp\\temp_check_line_bi.jpg"), check_line_bi)

    # 取得题目左上角像素的值
    location_list = access_pixels(check_line_bi)
    # location_list = valid_pixels(check_zone, gap_val, location_list)

    for i in range(len(location_list)):
        if i == len(location_list) - 1:
            question_zone = img[(location_list[i]-gap_val):height-delete_zone_height, 0:width]
        else:
            question_zone = img[(location_list[i]-gap_val):location_list[i+1]-gap_val, 0:width]
        
        # 裁剪多余的空白区域
        lower_limit = delete_blank(question_zone)
        lower_gap_val = int(1.5 * gap_val)
        if lower_limit + lower_gap_val < height:
            question_zone = question_zone[0:lower_limit + lower_gap_val, 0:width]

        if question_zone.shape[0] <= 150:
            # 删除错误（高度过小）部分
            continue
        else:
            cv2.imwrite(os.path.normpath(current_dir + "\\.clip\\" + file_name[:-4] + "_" + str(i) + ".jpg"), question_zone)


def main():
    # 创建目录  
    create_path()

    # 输出pdf图像文件
    pdf_to_image(pdf_dir)
    sep_line()

    # 获取目录下文件个数
    file_list = os.listdir(os.path.normpath(current_dir + "\\.pdf"))

    # 切分每张图片
    for file in file_list:
        file_path = os.path.normpath(current_dir + "\\.pdf\\{}".format(file))
        if os.path.exists(file_path):
            clip(file_path)
            print("question extracted: " + file)
        else:
            pass
    
    sep_line()
    print("extraction complete")

# 参数设置
pdf_dir = "D:\\Downloads\\PastPapers\\9702\\2021\\9702_s21_qp_11.pdf"
# current_dir = os.getcwd()
current_dir = "D:\\Program_Design"
print("working in dict: " + current_dir)
sep_line()

# 主程序
main()
os.system("pause")
