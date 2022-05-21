"""
mcq_tag_img.py
coding:utf-8

Developed by @Luke.Tang 2022
This program cuts a level mcqs in pdfs to single question as image file.
For more information, please visit github.com/Clob4k/a-level-mcq-cutter
"""

import os
import re
import cv2
import pytesseract


def create_path():   
    # 查询clip目录
    if not os.path.exists(os.path.normpath(current_dir + "\\.clip")):
        print("'clip' folder is mot found.")
        exit()
    # 创建信息目录 
    if not os.path.exists(os.path.normpath(current_dir + "\\.info")):
        os.makedirs(os.path.normpath(current_dir + "\\.info"))


def create_info(pic_dir):
    point = set()

    ignore_list = ["what", "which", "have", "has", "could", "with", "used", "take",\
                   "from", "that", "when", "they", "them", "their", "there", "shows"]

    img = cv2.imread(pic_dir, 1)
    text = pytesseract.image_to_string(img, lang='eng')
    line_list = text.split('\n')
    for line in line_list:
        # 排除不含有字母的行
        if re.search(r'[A-Z]', line):
            # 以空格分词
            question_char = line.split(" ")
            for char in question_char:
                char = char.lower()
                # 判断长度并为字母组成
                if len(char) >= 4 and char.isalpha():
                    if char in ignore_list:
                        continue
                    else:
                        point.add(char)
    print("="*100)
    print(text)
    print("="*100)
    print(point)
    print("="*100)

    write_info(str(point))


def write_info(line):
    option = input("Enter the key point: ")
    if option == "1":
        k1 = open("D:\\Program_Design\\dataset\\1_physical_quantities_and_units.txt", 'a')
        k1.write(line + "\n")
        k1.close()
    elif option == "2":
        k2 = open("D:\\Program_Design\\dataset\\2_kinematics.txt", 'a')
        k2.write(line + "\n")
        k2.close()
    elif option == "3":
        k3 = open("D:\\Program_Design\\dataset\\3_dynamics.txt", 'a')
        k3.write(line + "\n")
        k3.close()
    elif option == "4":
        k4 = open("D:\\Program_Design\\dataset\\4_forces, density_and_pressure.txt", 'a')
        k4.write(line + "\n")
        k4.close()
    elif option == "5":
        k5 = open("D:\\Program_Design\\dataset\\5_work, energy_and_power.txt", 'a')
        k5.write(line + "\n")
        k5.close()+6
        
    elif option == "6":
        k6 = open("D:\\Program_Design\\dataset\\6_deformation_of_solids.txt", 'a')
        k6.write(line + "\n")
        k6.close()
    elif option == "7":
        k7 = open("D:\\Program_Design\\dataset\\7_waves.txt", 'a')
        k7.write(line + "\n")
        k7.close()
    elif option == "8":
        k8 = open("D:\\Program_Design\\dataset\\8_superposition.txt", 'a')
        k8.write(line + "\n")
        k8.close()
    elif option == "9":
        k9 = open("D:\\Program_Design\\dataset\\9_electricity.txt", 'a')
        k9.write(line + "\n")
        k9.close()
    elif option == "10":
        k10 = open("D:\\Program_Design\\dataset\\10_D.C._circuits.txt", 'a')
        k10.write(line + "\n")
        k10.close()
    elif option == "11":
        k11 = open("D:\\Program_Design\\dataset\\11_particle_physics.txt", 'a')
        k11.write(line + "\n")
        k11.close()
    elif option == "12":
        k12 = open("D:\\Program_Design\\dataset\\12_electric_fields.txt", 'a')
        k12.write(line + "\n")
        k12.close()
    else:
        print("wrong input.")
        write_info(line)


def main():
    # 创建目录  
    create_path()
    # 获取目录下文件个数
    file_list = os.listdir(os.path.normpath(current_dir + "\\.clip"))
    # 切分每张图片
    for file in file_list:
        file_path = os.path.normpath(current_dir + "\\.clip") + "/{}".format(file)
        if os.path.exists(file_path):
            create_info(file_path)        


if __name__ == "__main__":  
    # current_dir = os.getcwd()
    current_dir = "D:\\Program_Design"
    print("working in dict: " + current_dir)
    main()