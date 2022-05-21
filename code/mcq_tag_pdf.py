"""
mcq_tag_pdf.py
coding:utf-8

Developed by @Luke.Tang 2022
This program cuts a level mcqs in pdfs to single question as image file.
For more information, please visit github.com/Clob4k/a-level-mcq-cutter
"""

import pdfplumber
import PyPDF2
import re


def pypdf():
    pdf = open("D:\\Downloads\\PastPapers\\9702\\2021\\9702_m21_qp_12.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf)
    page = pdfReader.getPage(3)
    page_text = page.extractText()
    return page_text


def pdfplumb():
    page_text = ""
    with pdfplumber.open('D:\\Downloads\\PastPapers\\9702\\2021\\9702_m21_qp_12.pdf') as pdf:
        for i, page in enumerate(pdf.pages):
            if i <= 2:
                continue
            else:
                page = pdf.pages[i]
                page_text = page_text + page.extract_text() 
    return page_text

if __name__ == "__main__":
    page = pdfplumb()
    text_question = ""
    line_list = page.split('\n')
    for line in line_list:
        if re.search(r'[A-Z]', line):
            print(line)
    
