#! /usr/bin/python
#-*- coding:utf-8 -*-
#author:zhanhao

from http.cookiejar import CookieJar
from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from PIL import Image
import code2string
import re

#请求
login = "http://bioinformatics.suda.edu.cn/sg/checklogin.php"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
course_select = "http://bioinformatics.suda.edu.cn/sg/course_select.php"
exam_type_select = "http://bioinformatics.suda.edu.cn/sg/exam_type_select.php"
exam_mode_select = "http://bioinformatics.suda.edu.cn/sg/exam_mode_select.php"
vcode = "http://bioinformatics.suda.edu.cn/sg/TestCode.php"

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))

#打开图片并写入
imgb = opener.open(vcode)
local = open('vv.jpg','wb')
local.write(imgb.read())
local.close()

#vcode
image = Image.open('vv.jpg')
vv = code2string.img2code(image)
print(vv)

login_data = urlencode({
'UserName':'1430416020',
'Password':'123456',
'TestCode2':''+vv,
'submit':'登录=>'
}).encode('utf-8')
select_course_data = urlencode({
    'imgbtn.x':'10',
    'imgbtn.y':'60',
    'Course_ID':'BIOI1015',
    'Course_Name':'网络管理与WEB编程',
    'Teacher_ID':'SY0532'
}).encode('utf-8')
select_exam_type_data = urlencode({
    'submit':'章节测验',
    'Exam_Type_ID':'3',
    'Exam_Type_Name':'章节测验',
    'NextMode':'exam_mode',
    'URL':'#'
}).encode('utf-8')
select_exam_mode_data = urlencode({
    'submit':'随便玩玩【综合】',
    'Exam_Mode_ID':'BIOI1015-3-1'
}).encode('utf-8')
req = Request(login,login_data,header)
opener.open(req)
req2 = Request(course_select,select_course_data,header)
opener.open(req2)
req3 = Request(exam_type_select,select_exam_type_data,header)
opener.open(req3)
req4 = Request(exam_mode_select,select_exam_mode_data,header)
opener.open(req4)
#exam_mode和exam_do交互提交，达到重复爬取的目的
link="http://bioinformatics.suda.edu.cn/sg/main.php"

print(opener.open(link).read().decode('utf-8'))
req4 = Request(exam_mode_select,select_exam_mode_data,header)
opener.open(req4)
print(opener.open(link).read().decode('utf-8'))
QID = re.findall("(BIO.*?)'",opener.open(link).read().decode('utf-8'))
print(QID)