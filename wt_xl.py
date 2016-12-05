#! /usr/bin/python3
# -*- coding:utf-8 -*-
#author:zhanhao
#Date:2016.11.25
#file:_0015.py

import xlwt

def write_xls(list_data):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('testsheet')
    col = 0
    row = 0
    for line in list_data:
        col = 0
        for value in line:
            sheet.write(row,col,value)
            col += 1
        row += 1
    wb.save("test.xls")
    

