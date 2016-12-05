#! /usr/bin/python3
# -*- coding:utf-8 -*-
#author:zhanhao
#Date:2016.11.26
#file:crawler_SG.py

from http.cookiejar import CookieJar
from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from PIL import Image
from code2string import img2code
from wt_xl import write_xls
import re

#数据
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
link="http://bioinformatics.suda.edu.cn/sg/main.php"
cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))


#选择爬取课程及章节
def select(html):
    '''
    选择爬取课程及章节，返回get_question需要的post数据
    '''

    course_select = "http://bioinformatics.suda.edu.cn/sg/course_select.php"
    exam_type_select = "http://bioinformatics.suda.edu.cn/sg/exam_type_select.php"
    COURSE = re.findall("value='(.*?)' style='display:none'/><input type='hidden' name='Course_Name' value='(.*?)' style='display:none'/><input type='hidden' name='Teacher_ID' value='(.*?)'",html)
    n = 0
    for i in COURSE:
        print(str(n)+"."+i[1])
        n += 1
    while True:
        select = input("输入要爬取题目的课程名称：")
        
        try:
            select = int(select)
        except ValueError:
            print("输入有误，重新选择")
            continue
        
        if select >= 0 and select <= len(COURSE)-1:
            break
        else:
            print("输入有误，重新选择")
    Course_ID = COURSE[select][0]
    Course_Name = COURSE[select][1]
    Teacher_ID = COURSE[select][2]
    select_course_data = urlencode({
        'imgbtn.x':'10',
        'imgbtn.y':'60',
        'Course_ID':Course_ID,
        'Course_Name':Course_Name,
        'Teacher_ID':Teacher_ID
    }).encode('utf-8')
    req2 = Request(course_select,select_course_data,header)
    opener.open(req2)
    select_exam_type_data = urlencode({
        'submit':'章节测验',
        'Exam_Type_ID':'3',
        'Exam_Type_Name':'章节测验',
        'NextMode':'exam_mode',
        'URL':'#'
    }).encode('utf-8')
    req3 = Request(exam_type_select,select_exam_type_data,header)
    opener.open(req3)
    print("自动选择，章节测验")
    html = opener.open(link).read().decode('utf-8')
    EXAM_MODE = re.findall("input name='submit' value='(.*?)' type='submit'  title='.*?'/><input name='Exam_Mode_ID' value='(.*?)'",html)
    n = 0
    for i in EXAM_MODE:
        print(str(n)+"."+i[0])
        n += 1
    while True:
        select = input("要爬取的章节：")
        
        try:
            select = int(select)
        except ValueError:
            print("输入有误，重新选择")
            continue
        
        if select >= 0 and select <= len(EXAM_MODE)-1:
            break
        else:
            print("输入有误，重新选择")
    submit = EXAM_MODE[select][0]
    Exam_Mode_ID = EXAM_MODE[select][1]
    select_exam_mode_data = urlencode({
        'submit':submit,
        'Exam_Mode_ID':Exam_Mode_ID
    }).encode('utf-8')
    return select_exam_mode_data

#发出请求，获取题目
def get_questions(select_exam_mode_data):
    '''
    向link发出请求，返回获取的题目，返回的是双重列表
    '''

    exam_mode_select = "http://bioinformatics.suda.edu.cn/sg/exam_mode_select.php"
    Q = list()
    req4 = Request(exam_mode_select,select_exam_mode_data,header)
    opener.open(req4)
    FIELD = re.findall("<fieldset (.*?)</fieldset>",opener.open(link).read().decode('utf-8'))
    for i in FIELD:
        QNAME = re.findall("<td style='word-break:break-all; word-wrap:break-word;'>(.*?)</td>",i)
        QANSER = re.findall("<span class='Options_Label'>(.*?)</span>",i)
        for j in QANSER:
            j = j.replace("&lt;","<")
            j = j.replace("&gt;",">")
            QNAME.append(j)
        Q.append(QNAME)
    return Q

#开始爬取
def start(usrn):
    '''
    主程序调用的函数，依次调用登录，选择课程后重复获取题目，可以自定义重复爬取次数
    '''

    Q = list()
    QTITLE = list() 
    print("正在登录...请稍后")
    while True:
        logdata = login(usrn)
        if re.search("基医生物>>S&G online",logdata):
            print("登录失败，再次尝试登录")
        else:
            print("登录成功")
            select_exam_mode_data = select(logdata)
            break
    for i in range(1000): #选择爬取的次数，如果要全部爬取题库最好设置重复多一些
        QNAME = get_questions(select_exam_mode_data)
        for i in range(len(QNAME)):
            if QNAME[i][0] not in QTITLE:
                print("发现新题，插入表格")
                Q.append(QNAME[i])
                QTITLE.append(QNAME[i][0])
            else:
                print("题目已存在，舍弃")
    write_xls(Q)
    print("写入表格完成")

#登录进入SG
def login(usrn):
    '''
    从testcode页面获取验证码，登录SG系统，提交登录请求，返回获取登陆后的第一个页面
    '''
    vcode = "http://bioinformatics.suda.edu.cn/sg/TestCode.php"
    login_url = "http://bioinformatics.suda.edu.cn/sg/checklogin.php"
    imgb = opener.open(vcode)
    local = open('vv.jpg','wb')
    local.write(imgb.read())
    local.close()
    image = Image.open('vv.jpg')
    vv = "123456"
    try:
        vv = img2code(image)
    except UnicodeError:
        vv = "123456"
    
    login_data = urlencode({
    'UserName':usrn,
    'Password':'123456',
    'TestCode2':''+vv,
    'submit':'登录=>'
    }).encode('utf-8')
    
    req = Request(login_url,login_data,header)
    opener.open(req)
    
    return opener.open(link).read().decode('utf-8')

#程序入口
if __name__ == "__main__":
    start("1430414037") #选择一个登录使用的学号，如果使用测试次数用完的学号会报错