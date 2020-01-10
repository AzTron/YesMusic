# -*- coding: UTF-8 -*-
from urllib import request
from http import cookiejar
import urllib.parse
import urllib.request, json
import pymysql  
import types
import time
import datetime
import requests
from tkinter import *


if __name__ == '__main__':

    #连接数据库
    db=pymysql.connect("192.168.2.61","root","123456","piano_teaching");  
    cursor=db.cursor()
    sql = """select week_ordinal,weekday,nickname,date_format(time_start, '%H:%i:%s'),date_format(time_end, '%H:%i:%s'),point_start_per,point_lenght_per,course_type from piano_teaching.v_timetable_excel order by week_ordinal,weekday,time_start;"""
    cursor.execute(sql)
    results = cursor.fetchall()
    course_list=[]
    g_height = 700
    g_width = 200
    root = Tk()
    i = 0
    fms=[]
    timestamp = time.time()
    timestruct = time.localtime(timestamp)
    print (time.strftime('%Y-%m-%d %H:%M:%S', timestruct))
    
    for result in results:
        #获取当前时间
        #now = time.strftime("%Y-%m-%d %H:%M:%S")
        #URL参数
        g_week_ordinal = result[0]
        g_weekday = result[1]
        g_nickname = result[2]
        g_time_start = result[3]
        g_time_end = result[4]
        g_point_start_per = result[5]
        g_point_lenght_per = result[6]
        g_course_type = result[7]
       
        str_print = g_nickname+'\n'+g_time_start+'--'+g_time_end
        print(str_print)
        if g_course_type == 3:
           g_color = 'green'
        elif g_course_type == 2:
            g_color = 'yellow'
        else:
           g_color = 'red'

        #print(g_weekday,int(g_point_lenght_per*g_height),g_point_lenght_per )
        
        #Frame(height = int(g_point_lenght_per*g_height),width = g_width,bg = 'green').place(x=(g_weekday - 1)* g_width, y= int(g_point_start_per*g_height), anchor=NW)
        fm = Frame(height = int(g_point_lenght_per*g_height),width = g_width,bg = g_color,borderwidth = 0)
        fm.pack_propagate(0)
        fm.place(x=(int(g_weekday) - 1)* (g_width+10), y= int(g_point_start_per*g_height), anchor=NW)
        if int(g_point_lenght_per*g_height) >= 35:
           Label(fm,text=str_print,borderwidth=1).pack()

    
