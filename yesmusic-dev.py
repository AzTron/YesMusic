#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
import os, sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
import time
import pymysql
import Date_Choice
import calendar
import datetime

def Connect_DB():
    db_connect = Get_DB_connect()
    print(db_connect)
    db         = pymysql.connect(db_connect[0],db_connect[1],db_connect[2],db_connect[3]);
    #db         = pymysql.connect("192.168.2.146","root","123456","yesmusic-test");
    cursor     = db.cursor()
    return db,cursor

def Fetch_Data(cursor,sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def Get_DB_connect():
    dict_apikey = {}
    f     = open(r'db_connect.txt', 'r')
    for line in f:
        if ',' in line:
            db_ip, db_username,db_password,db_schema = line.split(',', 3)
    f.close()
    return [db_ip,db_username,db_password,db_schema]




class Application_ui(Frame):
    
    date_selection = 'asc'

    def Get_Timetable(self):
    
        ## 获取学员姓名
##        member_nn    = self.TabStrip1__Tab5Cox3.get()
##
##        if len(member_nn) <> 0:
##           index        = member_nn.find('/')
##           member_name  = member_nn[:index]

        ## 获取学期周
        term_start_end = self.TabStrip1__Tab5Cox2.get()
        
        if len(term_start_end) != 0:
           term_start = term_start_end[:10]
           term_end   = term_start_end[11:]
        
        #print(datetime.date(*map(int, term_start.split('-'))))
        term_start_date= datetime.date(*map(int, term_start.split('-')))
        ##cursor.callproc('p_timetable_addblank',(term_start))

        sql_proc = """call p_timetable_addblank('%s') """%(term_start)
        #print(sql_proc)
        cursor.execute(sql_proc)
        db.commit


        sql_p1 = """select weekday,nickname,date_format(time_start, '%H:%i'), \
                 date_format(time_end, '%H:%i'),point_start_per,point_lenght_per,print_type \
                 from v_timetable_excel """

        sql_p2 = """ where course_date >= '%s'\
                 and course_date <= '%s'\
                 order by course_date,time_start;"""%(term_start,term_end)

        sql = sql_p1 + sql_p2

        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        course_list=[]
        g_height = 600
        g_width = 160
        i = 0
        fms=[]
        timestamp = time.time()
        timestruct = time.localtime(timestamp)
        top = Toplevel()
        top.geometry('1920x1080')
        #print (time.strftime('%Y-%m-%d %H:%M:%S', timestruct))

        
        style = Style()
        style_dict = {'Timetable1.TFrame':'#70c1b3','Timetable2.TFrame':'#e2dbbe','Timetable3.TFrame':'#f45b69','Timetable4.TFrame':'#247ba0'}
        style.configure('Timetable1.TFrame',background = style_dict['Timetable1.TFrame'])
        style.configure('Timetable2.TFrame',background = style_dict['Timetable2.TFrame'])
        style.configure('Timetable3.TFrame',background = style_dict['Timetable3.TFrame'])
        style.configure('Timetable4.TFrame',background = style_dict['Timetable4.TFrame'])
        
        g_height_last = 0
        g_y_last = 0

        days_1          = datetime.timedelta(days=1)

        weekday_dict = {'0':'Mon','1':'Tues','2':'Wed','3':'Thur','4':'Fri','5':'Sat','6':'Sun'}
        weekday_list = ['Mon','Tues','Wed','Thur','Fri','Sat','Sun']
        for i in range(7):
            fm_weekday = Frame(top,height = 50,width = g_width,borderwidth = 0)
            fm_weekday.place(x=(int(i) * (g_width+10)), y = 0, anchor=NW)
            fm_weekday.pack_propagate(0)
            ## -- 周日设置为红色
            if i in (5,6):
               l1 = Label(fm_weekday,text=weekday_list[i],borderwidth=0,font=("微软雅黑", 12,"bold"),foreground="#f45b69").pack()
            else:
               l1 = Label(fm_weekday,text=weekday_list[i],borderwidth=0,font=("微软雅黑", 12,"bold"),foreground="#292929").pack()
            l2 = Label(fm_weekday,text=str(term_start_date+(days_1*i)),borderwidth=0,font=("微软雅黑", 10),foreground="#595959").pack()

        ## -- 为了消除图形缝隙设置的参数
        height_last = 0
        width_last  = 0
        x_last      = 0
        y_last      = 0    
        ## -- -- 
        for result in results:
            #获取当前时间
            #now = time.strftime("%Y-%m-%d %H:%M:%S")
            #URL参数
            g_weekday = result[0]

            g_nickname = result[1]
            g_time_start = result[2]
            g_time_end = result[3]
            g_point_start_per = result[4]
            g_point_lenght_per = result[5]
            g_print_type = result[6]
           
            str_print_1 = g_nickname
            str_print_2 = g_time_start+'-'+g_time_end
            #print(str_print)
            #print(g_print_type)
            
            if g_print_type == 3:
               g_style = "Timetable4.TFrame"
               g_color = style_dict["Timetable4.TFrame"]
            elif g_print_type == 2:
               g_style = 'Timetable2.TFrame'
               g_color = style_dict["Timetable2.TFrame"]
            elif g_print_type == 99:
               g_style = 'Timetable1.TFrame'
               g_color = style_dict["Timetable1.TFrame"]
            else:
               g_style = 'Timetable3.TFrame'
               g_color = style_dict["Timetable3.TFrame"]


            ## -- 设置图形（图形之间有缝隙，需要完善）

            if g_point_start_per == 0:
               height_current = int(g_point_lenght_per*g_height)
               y_current      = int(g_point_start_per*g_height)+50
            else:
               height_current = int(g_point_lenght_per*g_height) + (int(g_point_start_per*g_height)+50) - (height_last + y_last) 
               y_current      = height_last + y_last

            fm = Frame(top,height = height_current,width = g_width,borderwidth = 0,style = g_style)
            fm.pack_propagate(0)
            fm.place(x=(int(g_weekday) - 1)* (g_width+10), y= y_current, anchor=NW)

            #print('height ='+str(int(g_point_lenght_per*g_height)),'width ='+str(g_width),'x ='+str((int(g_weekday) - 1)* (g_width+10)),'y ='+str(int(g_point_start_per*g_height)+50))

            

            height_last = int(g_point_lenght_per*g_height)
            width_last  = g_width
            x_last      = (int(g_weekday) - 1)* (g_width+10)
            y_last      = int(g_point_start_per*g_height)+50
            ## -- --  'y ='+str(int(g_point_start_per*g_height)+50)
        
            #如果地方够大，就写上名字和上课时间
            lenTxt = len(str_print_1) 
            lenTxt_utf8 = len(str_print_1.encode('utf-8'))
            size = int((lenTxt_utf8 - lenTxt)/2 + lenTxt)       
            
            if float(g_point_lenght_per*g_height) >= 30:
               if str_print_1 == '空闲' or str_print_1 == '休息':
                  l3 = Label(fm,text=str_print_1,relief = "flat",borderwidth=1,font=("微软雅黑", 12,"bold"),anchor="center",foreground="#FFFFFF",background = g_color).pack(side="left",fill="both",anchor="center",expand="yes")
               else:
                  if size <= 4:
                     font_size = 14
                  else:
                     font_size = 11 
                  l3 = Label(fm,text=str_print_1,relief = "flat",borderwidth=1,font=("微软雅黑", font_size,"bold"),anchor="center",foreground="#292929",background = g_color).pack(side="left",fill="both",anchor="center",expand="yes")
               l4 = Label(fm,text=str_print_2,relief = "flat",borderwidth=1,font=("微软雅黑", 12,"bold"),anchor="center",foreground="#FFFFFF",background = g_color).pack(side="right",fill="both",anchor="center",expand="yes")
    
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('叶子音乐屋')
        self.master.geometry('1000x500')
        self.createWidgets()
        #

    def submit_member_info(self):
        name         = self.TabStrip1__Tab1frame_top_Eny1.get()
        nickname     = self.TabStrip1__Tab1frame_top_Eny2.get()
        birthday     = self.TabStrip1__Tab1frame_top_Eny3.get()
        course_price = self.TabStrip1__Tab1frame_top_Eny4.get()
        reg_date     = self.TabStrip1__Tab1frame_top_Eny5.get()
        coach        = self.TabStrip1__Tab1frame_top_Eny6.get()
        coach_phone  = self.TabStrip1__Tab1frame_top_Eny7.get()
        coach2       = self.TabStrip1__Tab1frame_top_Eny8.get()
        coach2_phone = self.TabStrip1__Tab1frame_top_Eny9.get()
        
        member_id = Fetch_Data(cursor,'select max(member_id)+1 from member_info where member_id < 900;')[0][0]

        if len(reg_date) == 0:
           reg_date = 'null'

           sql = """INSERT INTO `member_info`(`member_id`,`member_name`,`member_birth`,`valid`,`member_nickname`,`course_price60`,`registration_date`,`coach`,`coach_phone`,`coach2`,`coach2_phone`)
                    VALUES(%s,'%s','%s',%s,'%s',%s,%s,'%s','%s','%s','%s');"""%(member_id,name,birthday,1,nickname,course_price,reg_date,coach,coach_phone,coach2,coach2_phone)
        else:
           sql = """INSERT INTO `member_info`(`member_id`,`member_name`,`member_birth`,`valid`,`member_nickname`,`course_price60`,`registration_date`,`coach`,`coach_phone`,`coach2`,`coach2_phone`)
                    VALUES(%s,'%s','%s',%s,'%s',%s,'%s','%s','%s','%s','%s');"""%(member_id,name,birthday,1,nickname,course_price,reg_date,coach,coach_phone,coach2,coach2_phone)


        print(sql)

        cursor.execute(sql)
        db.commit()

    def submit_plan_add(self):
        member_name  = self.TabStrip1__Tab2Eny1.get()
        term_start   = self.TabStrip1__Tab2Eny2.get()
        weekday      = self.TabStrip1__Tab2Eny3.get()
        time_start   = self.TabStrip1__Tab2Eny4.get()
        time_end     = self.TabStrip1__Tab2Eny5.get()

        member_id    = Fetch_Data(cursor,"""select member_id from member_info where member_name = '%s';"""%(member_name))[0][0]
        
        sql = ("""INSERT INTO `piano_teaching`.`member_plan`(`member_id`,`term_start`,`term_end`,`course_type`,`weekday`,`time_start`,`time_end`)VALUESVALUES(%s,'%s',null,%s,%s,'%s','%s');"""
               %(member_id,term_start,1,weekday,time_start,time_end))
        #print(sql)
    


    def submit_course_plan(self):
    
        member_nn    = self.TabStrip1__Tab3Cox1.get()
        date         = self.TabStrip1__Tab3Eny2.get()
        ##date         = self.TabStrip1__Tab3Eny3.get()
        time_start   = self.TabStrip1__Tab3Cox4.get()
        time_end     = self.TabStrip1__Tab3Eny5.get()

        index        = member_nn.find('/')
        member_name  = member_nn[:index]

        course_price60 = Fetch_Data(cursor,"""select course_price60 from member_info where member_name = '%s';"""%(member_name))[0][0]
        course_price   = course_price60/60*45
        ##member_id    = Fetch_Data(cursor,"""select member_id from member_info where member_name = '%s';"""%(member_name))[0][0]
        ##course_tpye  = Fetch_Data(cursor,"""select course_type from member_plan where member_id = %s;"""%(member_id))[0][0]

        

        #print(member_name,str(date),str(time_start),str(time_end),'45','1')
        sql = ("""INSERT INTO `timetable`(`member_name`,`course_date`,`time_start`,`time_end`,`course_type`,`course_price`,`status`)VALUES('%s','%s','%s','%s','%s',%s,'%s');"""
               %(member_name,str(date),str(time_start),str(time_end),'45',course_price,'1'))
        #print(sql)
        cursor.execute(sql)
        db.commit()

        self.TabStrip1__Tab3Lbl6.config(text=member_name+" "+str(date)+" "+'正常排课成功！', foreground = "red")
        #print('OK')

    def submit_course_adjust_intime(self):
    
        member_nn    = self.TabStrip1__Tab3Cox1.get()
        date         = self.TabStrip1__Tab3Eny2.get()
        ##date         = self.TabStrip1__Tab3Eny3.get()
        time_start   = self.TabStrip1__Tab3Cox4.get()
        time_end     = self.TabStrip1__Tab3Eny5.get()

        index        = member_nn.find('/')
        member_name  = member_nn[:index]

        course_price60 = Fetch_Data(cursor,"""select course_price60 from member_info where member_name = '%s';"""%(member_name))[0][0]
        course_price   = course_price60/60*45
        ##member_id    = Fetch_Data(cursor,"""select member_id from member_info where member_name = '%s';"""%(member_name))[0][0]
        ##course_tpye  = Fetch_Data(cursor,"""select course_type from member_plan where member_id = %s;"""%(member_id))[0][0]

        

        #print(member_name,str(date),str(time_start),str(time_end),'45','1')
        sql = ("""INSERT INTO `timetable`(`member_name`,`course_date`,`time_start`,`time_end`,`course_type`,`course_price`,`status`)VALUES('%s','%s','%s','%s','%s',%s,'%s');"""
               %(member_name,str(date),str(time_start),str(time_end),'45',course_price,'3'))
        #print(sql)
        cursor.execute(sql)
        db.commit()

        self.TabStrip1__Tab3Lbl6.config(text=member_name+" "+str(date)+" "+'调整加课成功！', foreground = "red")
        #print('OK')

    def submit_course_add(self):
    
        member_nn    = self.TabStrip1__Tab3Cox1.get()
        date         = self.TabStrip1__Tab3Eny2.get()
        ##date         = self.TabStrip1__Tab3Eny3.get()
        time_start   = self.TabStrip1__Tab3Cox4.get()
        time_end     = self.TabStrip1__Tab3Eny5.get()

        index        = member_nn.find('/')
        member_name  = member_nn[:index]

        course_price60 = Fetch_Data(cursor,"""select course_price60 from member_info where member_name = '%s';"""%(member_name))[0][0]
        course_price   = course_price60/60*45
        ##member_id    = Fetch_Data(cursor,"""select member_id from member_info where member_name = '%s';"""%(member_name))[0][0]
        ##course_tpye  = Fetch_Data(cursor,"""select course_type from member_plan where member_id = %s;"""%(member_id))[0][0]

        

        #print(member_name,str(date),str(time_start),str(time_end),'45','1')
        sql = ("""INSERT INTO `timetable`(`member_name`,`course_date`,`time_start`,`time_end`,`course_type`,`course_price`,`status`)VALUES('%s','%s','%s','%s','%s',%s,'%s');"""
               %(member_name,str(date),str(time_start),str(time_end),'45',course_price,'4'))
        #print(sql)
        cursor.execute(sql)
        db.commit()

        self.TabStrip1__Tab3Lbl6.config(text=member_name+" "+str(date)+" "+'加课成功！', foreground = "red")
        #print('OK')

    def submit_course_add_adjust(self):
        
        member_nn    = self.TabStrip1__Tab3Cox1.get()
        date         = self.TabStrip1__Tab3Eny2.get()
        ##date         = self.TabStrip1__Tab3Eny3.get()
        time_start   = self.TabStrip1__Tab3Eny4.get()
        time_end     = self.TabStrip1__Tab3Eny5.get()

        index        = member_nn.find('/')
        member_name  = member_nn[:index]
        
        member_id    = Fetch_Data(cursor,"""select member_id from member_info where member_name = '%s';"""%(member_name))[0][0]
        course_tpye  = Fetch_Data(cursor,"""select course_type from member_plan where member_id = %s;"""%(member_id))[0][0]

        

        
        sql = ("""INSERT INTO `timetable_addition`(`member_id`,`course_type`,`time_start`,`time_end`,`weekday`,`week_ordinal`,`adjust`)VALUES(%s,%s,'%s','%s',(case DAYOFWEEK('%s')-1 when 0 then 7 else DAYOFWEEK('%s')-1 end),week('%s',1),'%s');"""
               %(member_id,course_tpye,time_start,time_end,date,date,date,'3'))
        #print(sql)
        cursor.execute(sql)
        db.commit()

        
        #print('OK')

        

    
    def cancle_class(self):

        f_note    = self.TabStrip1__Tab4frame_right_Eny1.get()

        for item in self.TabStrip1__Tab4frame_center_tree.selection():
            item_text      = self.TabStrip1__Tab4frame_center_tree.item(item,"values")
            f_member_name = item_text[0]
            f_date      = item_text[1]
            f_time_start    = item_text[3]
            
            sql = """update timetable set status = 0,note = '%s' where member_name = '%s' and course_date = '%s' and time_start =  '%s';"""%(f_note,f_member_name,f_date,f_time_start)

            #print(sql)
            cursor.execute(sql)
            db.commit()
        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()

    def cancle_class_adjust(self):

        f_note    = self.TabStrip1__Tab4frame_right_Eny1.get()

        for item in self.TabStrip1__Tab4frame_center_tree.selection():
            item_text      = self.TabStrip1__Tab4frame_center_tree.item(item,"values")
            f_member_name = item_text[0]
            f_date      = item_text[1]
            f_time_start    = item_text[3]

            sql = """update timetable set status = 2,note = '%s' where member_name = '%s' and course_date = '%s' and time_start =  '%s';"""%(f_note,f_member_name,f_date,f_time_start)
        #print(sql)
            cursor.execute(sql)
            db.commit()
        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()

    def delete_row(self):

        for item in self.TabStrip1__Tab4frame_center_tree.selection():
            item_text      = self.TabStrip1__Tab4frame_center_tree.item(item,"values")
            f_member_name = item_text[0]
            f_date      = item_text[1]
            f_time_start    = item_text[3]

            sql = """delete from timetable where member_name = '%s' and course_date = '%s' and time_start =  '%s';"""%(f_member_name,f_date,f_time_start)
        #print(sql)
            cursor.execute(sql)
            db.commit()
        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()
        
    def restore_class(self):

        for item in self.TabStrip1__Tab4frame_center_tree.selection():
            item_text      = self.TabStrip1__Tab4frame_center_tree.item(item,"values")
            f_member_name = item_text[0]
            f_date      = item_text[1]
            f_time_start    = item_text[3]

            sql = """update timetable set status = 1,note = null where member_name = '%s' and course_date = '%s' and time_start =  '%s';"""%(f_member_name,f_date,f_time_start)
        #print(sql)
            cursor.execute(sql)
            db.commit()
        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()

    def reflesh_class(self):

        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()

    def reflesh_course (self,*arg):

        self.delTree(self.TabStrip1__Tab4frame_center_tree)
        self.load_v_timetable_show()
       





    def handler_adaptor(self, fun,  **kwds):
        """事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

##    def handler(self, event, sub_widget):
##        """事件处理函数"""
##        content = lb.get(lb.curselection())
##        return messagebox.showinfo(title="Hey, you got me!", message="I am {0}".format(content), parent=top)

    def _Enter(self,event,sub_widget):
        #print(sub_widget.selection)
        date_pression.set(sub_widget.selection)

    def _ButtonRelease(self,event,sub_widget,date_show):
        #print(sub_widget.selection)
        date_show.set(sub_widget.selection)
        
        
    def date_selection(self,event,date_input):
        top = Toplevel(self)
        top.title('选择日期')
        ##top.geometry('230x180')
        ttkcal = Date_Choice.Calendar(top,firstweekday=calendar.SUNDAY)
        ttkcal.pack(expand=1, fill='both')
        ttkcal._calendar.bind('<ButtonPress-1>',ttkcal._pressed)
        ttkcal._calendar.bind(sequence='<ButtonRelease-1>',func=self.handler_adaptor(self._ButtonRelease, sub_widget=ttkcal,date_show=date_input))

    def load_v_timetable_show(self):

        term_start = ''
        term_end   = ''

         ## 获取学员姓名
        member_nn    = self.TabStrip1__Tab4frame_right_Cox3.get()

        if len(member_nn) != 0:
           index        = member_nn.find('/')
           member_name  = member_nn[:index]

        ## -- 20190921 获取学期周日期
        term_name    = self.TabStrip1__Tab4frame_right_Cox1.get()

        if len(term_name) != 0:
           sql_term     = """select term_start,term_end from term_info where term_name = '%s'; """%(term_name)
           cursor.execute(sql_term)
           term_results = cursor.fetchone()
           term_start   = str(term_results[0])
           term_end     = str(term_results[1])
        ## -- -- 

        ## 获取学期周
        term_start_end = self.TabStrip1__Tab4frame_right_Cox2.get()
        
        
        if len(term_start_end) != 0:
           term_start = term_start_end[:10]
           term_end   = term_start_end[11:]

        
        
        if len(term_start) == 0:
            term_start = '1970-01-01'
        if len(term_end) == 0:
            term_end   = '2999-12-31'
            
        sql_p1 = """select * from v_timetable_show where course_date >= '%s' and course_date <= '%s' """%(term_start,term_end)

        sql_p2 = ''

        sql_order = """order by course_date,time_start"""

        if len(member_nn) != 0:
           sql_p2 = """and member_name = '%s'"""%(member_name)

        sql = sql_p1 + sql_p2 + sql_order

        cursor.execute(sql)
        results = cursor.fetchall()

        ## 只有学期周信息时可以核定
        if len(term_start_end) != 0 and len(member_nn) == 0:
           self.TabStrip1__Tab4frame_right_bun5.configure(state='enabled')
        else:
           self.TabStrip1__Tab4frame_right_bun5.configure(state='disabled')

        for result in results:
            #获取当前时间
            #now = time.strftime("%Y-%m-%d %H:%M:%S")
            #URL参数
            g_member_name = result[0]
            g_course_date = result[1]
            g_weekday = result[2]
            g_time_start = result[3]
            g_time_end = result[4]
            g_course_type = result[5]
            g_status = result[6]
            g_note   = result[7]

            g_time_start_end = g_time_start+' - '+g_time_end

            self.TabStrip1__Tab4frame_center_tree.insert("", "end", values=(g_member_name,g_course_date,g_weekday,g_time_start,g_time_end,g_course_type,g_status,g_note))

    def delTree(self,tree):
        results = tree.get_children()
        for item in results:
            tree.delete(item)

    def create_time_list(self,tree):
        results = tree.get_children()
        for item in results:
            tree.delete(item)

    def set_time_end(self,*arg):

        mins_get          = datetime.timedelta(minutes=int(self.TabStrip1__Tab3Cox3.get()))
        time_start_time   = datetime.datetime.strptime(self.TabStrip1__Tab3Cox4.get(),"%H:%M:%S")
        time_end_time     = time_start_time + mins_get

        time_end_time_str = time_end_time.strftime('%H:%M:%S')
        time_end.set(time_end_time_str)
        

    def set_term_order(self,*arg):
        
        term_name = self.TabStrip1__Tab5Cox1.get()
       
        self.TabStrip1__Tab5Cox2['values'] = term_dict[term_name]


    def set_term_order2(self,*arg):
        
        term_name = self.TabStrip1__Tab4frame_right_Cox1.get()
       
        self.TabStrip1__Tab4frame_right_Cox2['values'] = term_dict[term_name]

    def approval_timetable(self,*arg):
        
        term_start_end = self.TabStrip1__Tab4frame_right_Cox2.get()
        if len(term_start_end) == 0:
           self.TabStrip1__Tab4frame_right_Lbl4.config(text='没有学期周信息，无法核定！', foreground = "red")
           return
        else:
           term_start = term_start_end[:10]
           term_end   = term_start_end[11:]

        today_now      = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        

        ## 正常记录和加课、调课记录进入history
        sql_approval_1 = """insert into timetable_history
                            SELECT `timetable`.`member_name`,
                                   `timetable`.`course_date`,
                                   `timetable`.`time_start`,
                                   `timetable`.`time_end`,
                                   `timetable`.`course_type`,
                                   `timetable`.`course_price`,
                                   `timetable`.`status`,
                                   '%s',
                                   `timetable`.`note`
                              FROM `timetable` where status in ('1','3','4') and course_date >= '%s' and course_date <= '%s'; """%(today_now,term_start,term_end)
        ## 请假记录进入leaving
        sql_approval_2 = """insert into timetable_leaving
                            SELECT `timetable`.`member_name`,
                                   `timetable`.`course_date`,
                                   `timetable`.`time_start`,
                                   `timetable`.`time_end`,
                                   `timetable`.`course_type`,
                                   `timetable`.`course_price`,
                                   `timetable`.`status`,
                                   '%s',
                                   `timetable`.`note`
                              FROM `timetable` where status in ('0','2') and course_date >= '%s' and course_date <= '%s'; """%(today_now,term_start,term_end)
        ## 删除timetable 
        sql_approval_3 = """delete from timetable where status in ('0','1','2','3','4') and course_date >= '%s' and course_date <= '%s'; """%(term_start,term_end)

        #print(sql_approval_1)
        #print(sql_approval_2)
        #print(sql_approval_3)
        
        cursor.execute(sql_approval_1)
        cursor.execute(sql_approval_2)
        cursor.execute(sql_approval_3)

        db.commit()

        self.TabStrip1__Tab4frame_right_Lbl4.config(text=str(term_start)+" - "+str(term_end)+'核定成功！', foreground = "red")

    def select_payment_balance(self,*arg):

        self.delTree(self.TabStrip1__Tab6frame_center_tree)
         ## 获取学员姓名
        member_nn    = self.TabStrip1__Tab6frame_right_Cox2.get()

        if len(member_nn) != 0:
           index        = member_nn.find('/')
           member_name  = member_nn[:index]

        ## 获取学期
        term_name = self.TabStrip1__Tab6frame_right_Cox1.get()
        

            
        sql_p0 = """select * from v_payment_balance where """
        sql_p1 = ''
        sql_p2 = ''

        sql_order = """order by payment_term,payment_balance"""

        if len(term_name) != 0:
           sql_p1 = """payment_term = '%s'"""%(term_name)
        
        if len(member_nn) != 0:
           sql_p2 = """member_name = '%s'"""%(member_name)

        if len(sql_p1) != 0 and len(sql_p2) != 0:
           sql = sql_p0 + sql_p1 +" and "+ sql_p2 + sql_order
        else:
           sql = sql_p0 + sql_p1 + sql_p2 + sql_order
        
        
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()


        for result in results:
            #获取当前时间
            #now = time.strftime("%Y-%m-%d %H:%M:%S")
            #URL参数
            g_member_name     = result[0]
            g_payment_term    = result[1]
            g_payment_total   = result[2]
            g_price_total     = result[3]
            g_payment_balance = result[4]
            g_course_balance  = result[5]
            

            self.TabStrip1__Tab6frame_center_tree.insert("", "end", values=(g_member_name,g_payment_term,g_payment_total,g_price_total,g_payment_balance,g_course_balance))

    def select_member_info(self):

        self.delTree(self.TabStrip1__Tab1frame_bottom_tree)
        
        sql = """select * from member_info where member_id < 900"""
        
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        for result in results:
            #获取当前时间
            #now = time.strftime("%Y-%m-%d %H:%M:%S")
            #URL参数
            g_member_id       = result[0]
            g_member_name     = result[1]
            g_member_birth    = result[2]
            g_valid           = result[3]
            g_member_nickname = result[4]
            g_course_price60  = result[5]
            g_reg_date        = result[6]
            g_coach           = result[7]
            g_coach_phone     = result[8]
            g_coach2          = result[9]
            g_coach2_phone    = result[10]
        
            

            self.TabStrip1__Tab1frame_bottom_tree.insert("", "end", values=(g_member_id,g_valid,g_member_name,g_member_nickname,g_member_birth,g_course_price60,g_reg_date,g_coach,g_coach_phone,g_coach2,g_coach2_phone))   

    def set_member_info(self,*arg):

        curItem  = self.TabStrip1__Tab1frame_bottom_tree.focus()
        dictItem = self.TabStrip1__Tab1frame_bottom_tree.item(curItem)
        #print(dictItem['values'][2])

        member_vaild_dict = {'1':'是','0':'否'}
        
        global g_set_member_id

        g_set_member_id = dictItem['values'][0]
        print(g_set_member_id)

        self.member_name.set(dictItem['values'][2])
        self.member_nickname.set(dictItem['values'][3])
        self.member_birthday.set(dictItem['values'][4])
        self.member_course_price60.set(dictItem['values'][5])
        self.member_registration_date.set(dictItem['values'][6])
        self.member_coach.set(dictItem['values'][7])
        self.member_coach_phone.set(dictItem['values'][8])
        self.member_coach2.set(dictItem['values'][9])
        self.member_coach2_phone.set(dictItem['values'][10])

        self.member_vaild.set(member_vaild_dict[str(dictItem['values'][1])])
        
        ##member_id = Fetch_Data(cursor,'select max(member_id)+1 from member_info where member_id < 900;')[0][0]

    def update_member_info(self,*arg):
        
        name         = self.TabStrip1__Tab1frame_top_Eny1.get()
        nickname     = self.TabStrip1__Tab1frame_top_Eny2.get()
        birthday     = self.TabStrip1__Tab1frame_top_Eny3.get()
        course_price = self.TabStrip1__Tab1frame_top_Eny4.get()
        reg_date     = self.TabStrip1__Tab1frame_top_Eny5.get()
        coach        = self.TabStrip1__Tab1frame_top_Eny6.get()
        coach_phone  = self.TabStrip1__Tab1frame_top_Eny7.get()
        coach2       = self.TabStrip1__Tab1frame_top_Eny8.get()
        coach2_phone = self.TabStrip1__Tab1frame_top_Eny9.get()
        valid        = self.TabStrip1__Tab1frame_top_Cox10.get()
        
        #member_id = Fetch_Data(cursor,"select member_id from member_info where member_name = '%s';"%(name))[0][0]

        if len(reg_date) == 0:
           reg_date = 'null'

        member_valid_dict2 = {'是':1,'否':0}

        
        if reg_date == 'None' or len(reg_date) == 0:
           sql = """update `member_info` set `member_id`=%s,`member_name`='%s',`member_birth`='%s',`valid`=%s,`member_nickname`='%s',`course_price60`=%s,
                 `registration_date`= null,`coach`='%s',`coach_phone`='%s',`coach2`='%s',`coach2_phone`='%s' where member_id = %s;"""%(g_set_member_id,name,birthday,member_valid_dict2[valid],nickname,course_price,coach,coach_phone,coach2,coach2_phone,g_set_member_id) 
        else:
           sql = """update `member_info` set `member_id`=%s,`member_name`='%s',`member_birth`='%s',`valid`=%s,`member_nickname`='%s',`course_price60`=%s,
                 `registration_date`='%s',`coach`='%s',`coach_phone`='%s',`coach2`='%s',`coach2_phone`='%s' where member_id = %s;"""%(g_set_member_id,name,birthday,member_valid_dict2[valid],nickname,course_price,reg_date,coach,coach_phone,coach2,coach2_phone,g_set_member_id) 

        print(sql)

        cursor.execute(sql)
        db.commit()

        ##获取学员列表
        global member_list
        member_list = []
        member_form = Fetch_Data(cursor,"""select member_name,member_nickname from member_info where member_id <> 999 and valid = '1' ;""")
        for member in member_form:
            member_list.append(member[0]+'/'+member[1])
        print(member_list)
        ##-------------

    def submit_payment_add(self):
        member_nn      = self.TabStrip1__Tab7frame_topCox1.get()
        term_name      = self.TabStrip1__Tab7frame_topCox2.get()
        payment_date   = self.TabStrip1__Tab7frame_topEny3.get()
        payment        = self.TabStrip1__Tab7frame_topEny4.get()
        p_to_c         = self.TabStrip1__Tab7frame_topEny5.get()
        payment_way    = self.TabStrip1__Tab7frame_topCox6.get()

        index          = member_nn.find('/')
        member_name    = member_nn[:index]
        
        sql = ("""INSERT INTO `member_payment`(`member_name`,`payment`,`payment_date`,`payment_way`,`payment_term`)VALUES('%s',%s,'%s','%s','%s');"""
               %(member_name,payment,payment_date,payment_way,term_name))
        cursor.execute(sql)
        db.commit()

    def select_payment_info(self,*arg):

        self.delTree(self.TabStrip1__Tab7frame_bottom_tree)
        
         ## 获取学员姓名
        member_nn    = self.TabStrip1__Tab7frame_topCox1.get()

        if len(member_nn) != 0:
           index        = member_nn.find('/')
           member_name  = member_nn[:index]

        ## 获取学期
        term_name = self.TabStrip1__Tab7frame_topCox2.get()
        

            
        sql_p0 = """select * from member_payment where """
        sql_p1 = ''
        sql_p2 = ''

        sql_order = """order by payment_term,member_name"""

        if len(term_name) != 0:
           sql_p1 = """payment_term = '%s'"""%(term_name)
        
        if len(member_nn) != 0:
           sql_p2 = """member_name = '%s'"""%(member_name)

        if len(sql_p1) != 0 and len(sql_p2) != 0:
           sql = sql_p0 + sql_p1 +" and "+ sql_p2 + sql_order
        else:
           sql = sql_p0 + sql_p1 + sql_p2 + sql_order
        
        
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()


        for result in results:
            #获取当前时间
            #now = time.strftime("%Y-%m-%d %H:%M:%S")
            #URL参数
            member_name     = result[0]
            payment         = result[1]
            payment_date    = result[2]
            payment_way     = result[3]
            payment_term    = result[4]
          
            

            self.TabStrip1__Tab7frame_bottom_tree.insert("", "end", values=(member_name,payment,payment_date,payment_way,payment_term))

    def createWidgets(self):

        self.top = self.winfo_toplevel()
        self.style = Style()
 
        self.TabStrip1 = Notebook(self.top)
        self.TabStrip1.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.876)


        ## 第一页，学员信息登记，文本框
        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='学员信息登记')
        self.TabStrip1__Tab1frame_top     = Frame(self.TabStrip1__Tab1,width=700, height=100)
        self.TabStrip1__Tab1frame_bottom  = Frame(self.TabStrip1__Tab1,width=700, height=200)
        self.TabStrip1__Tab1frame_top.pack(side = TOP)
        self.TabStrip1__Tab1frame_bottom.pack(side = BOTTOM,fill=BOTH,expand='yes')

        self.TabStrip1__Tab1frame_top_Lbl1 = Label(self.TabStrip1__Tab1frame_top, text='姓名')
        self.TabStrip1__Tab1frame_top_Lbl2 = Label(self.TabStrip1__Tab1frame_top, text='小名')
        self.TabStrip1__Tab1frame_top_Lbl3 = Label(self.TabStrip1__Tab1frame_top, text='生日')
        self.TabStrip1__Tab1frame_top_Lbl4 = Label(self.TabStrip1__Tab1frame_top, text="课费标准(60')")
        self.TabStrip1__Tab1frame_top_Lbl5 = Label(self.TabStrip1__Tab1frame_top, text='转正日期')
        self.TabStrip1__Tab1frame_top_Lbl6 = Label(self.TabStrip1__Tab1frame_top, text='主陪练')
        self.TabStrip1__Tab1frame_top_Lbl7 = Label(self.TabStrip1__Tab1frame_top, text='主陪练电话')
        self.TabStrip1__Tab1frame_top_Lbl8 = Label(self.TabStrip1__Tab1frame_top, text='副陪练')
        self.TabStrip1__Tab1frame_top_Lbl9 = Label(self.TabStrip1__Tab1frame_top, text='副陪练电话')

        self.TabStrip1__Tab1frame_top_Lbl10 = Label(self.TabStrip1__Tab1frame_top, text='活跃学员')

        ## -- 设置绑定值 20190906
        self.member_name              = StringVar()
        self.member_nickname          = StringVar()
        self.member_birthday          = StringVar()
        self.member_course_price60    = StringVar()
        self.member_registration_date = StringVar()
        self.member_coach             = StringVar()
        self.member_coach_phone       = StringVar()
        self.member_coach2            = StringVar()
        self.member_coach2_phone      = StringVar()
        self.member_vaild             = StringVar()

        self.member_birthday.set('2012-01-01')
        print(self.member_birthday.get())
        ## -- -- 
        self.TabStrip1__Tab1frame_top_Eny1 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_name)
        self.TabStrip1__Tab1frame_top_Eny2 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_nickname)
        self.TabStrip1__Tab1frame_top_Eny3 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_birthday)

        self.TabStrip1__Tab1frame_top_Eny4 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_course_price60)
        self.TabStrip1__Tab1frame_top_Eny5 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_registration_date)
        self.TabStrip1__Tab1frame_top_Eny6 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_coach)
        self.TabStrip1__Tab1frame_top_Eny7 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_coach_phone)
        self.TabStrip1__Tab1frame_top_Eny8 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_coach2)
        self.TabStrip1__Tab1frame_top_Eny9 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_coach2_phone)

        ##self.TabStrip1__Tab1frame_top_Eny10 = Entry(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_vaild)

        self.TabStrip1__Tab1frame_top_Cox10 = Combobox(self.TabStrip1__Tab1frame_top,width = 15,textvariable = self.member_vaild)
        self.TabStrip1__Tab1frame_top_Cox10['values'] = member_valid_list

        ## 确认和取消
        self.TabStrip1__Tab1frame_top_Bun1 = Button(self.TabStrip1__Tab1frame_top,text='注册',command = self.submit_member_info)
        self.TabStrip1__Tab1frame_top_Bun2 = Button(self.TabStrip1__Tab1frame_top,text='更新',command = self.update_member_info)

        self.TabStrip1__Tab1frame_bottom_tree = Treeview(self.TabStrip1__Tab1frame_bottom, show="headings", height=7, columns=("a", "b", "c", "d", "e","f","g","h","i","j","k"))
        self.TabStrip1__Tab1frame_bottom_vbar1 = Scrollbar(self.TabStrip1__Tab1frame_bottom, orient=VERTICAL, command=self.TabStrip1__Tab1frame_bottom_tree.yview)
        self.TabStrip1__Tab1frame_bottom_vbar2 = Scrollbar(self.TabStrip1__Tab1frame_bottom, orient=HORIZONTAL, command=self.TabStrip1__Tab1frame_bottom_tree.xview)

        self.TabStrip1__Tab1frame_bottom_tree.configure(yscrollcommand=self.TabStrip1__Tab1frame_bottom_vbar1.set)
        self.TabStrip1__Tab1frame_bottom_tree.configure(xscrollcommand=self.TabStrip1__Tab1frame_bottom_vbar2.set)

        ##标题长度
        self.TabStrip1__Tab1frame_bottom_tree.column("a", minwidth=80,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("b", minwidth=80,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("c", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("d", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("e", minwidth=100,width=100,anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("f", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("g", minwidth=80,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("h", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("i", minwidth=100,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("j", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab1frame_bottom_tree.column("k", minwidth=100,width=60, anchor="center",stretch = 'yes')
        
        ##标题名称 
        self.TabStrip1__Tab1frame_bottom_tree.heading("a", text="学员编号")
        self.TabStrip1__Tab1frame_bottom_tree.heading("b", text="活跃学员")
        self.TabStrip1__Tab1frame_bottom_tree.heading("c", text="学员姓名")
        self.TabStrip1__Tab1frame_bottom_tree.heading("d", text="小名")
        self.TabStrip1__Tab1frame_bottom_tree.heading("e", text="学员生日")
        self.TabStrip1__Tab1frame_bottom_tree.heading("f", text="课费标准（60'）")
        self.TabStrip1__Tab1frame_bottom_tree.heading("g", text="转正日期")
        self.TabStrip1__Tab1frame_bottom_tree.heading("h", text="主教练")
        self.TabStrip1__Tab1frame_bottom_tree.heading("i", text="主教练电话")
        self.TabStrip1__Tab1frame_bottom_tree.heading("j", text="副教练")
        self.TabStrip1__Tab1frame_bottom_tree.heading("k", text="副教练电话")
       

        self.TabStrip1__Tab1frame_bottom_tree.grid(row=0, column=0, sticky=NSEW)
        self.TabStrip1__Tab1frame_bottom_vbar1.grid(row=0, column=1, sticky=NS)
        self.TabStrip1__Tab1frame_bottom_vbar2.grid(row=1, column=0, sticky=EW)

        self.TabStrip1__Tab1frame_bottom_tree.bind("<Double-Button-1>",self.set_member_info)

        self.TabStrip1__Tab1frame_bottom_Bun1 = Button(self.TabStrip1__Tab1frame_bottom,text='刷新',command = self.select_member_info)
        self.TabStrip1__Tab1frame_bottom_Bun1.grid(row=2, column=0, sticky=E)

        ## 设置行列占比权重
        self.TabStrip1__Tab1frame_bottom.rowconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.rowconfigure(1, weight=1)
        self.TabStrip1__Tab1frame_bottom.columnconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.columnconfigure(1, weight=1)
        
        ## 第一页，布局
        ## top 第一行
        self.TabStrip1__Tab1frame_top_Lbl1.grid(row=0,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny1.grid(row=0,column =1,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl2.grid(row=0,column =2,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny2.grid(row=0,column =3,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl3.grid(row=0,column =4,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny3.grid(row=0,column =5,padx = 3,pady = 10,sticky = W)
        ##
        self.TabStrip1__Tab1frame_top_Lbl4.grid(row=1,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny4.grid(row=1,column =1,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl5.grid(row=1,column =2,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny5.grid(row=1,column =3,padx = 3,pady = 10,sticky = W)
        ##
        
        self.TabStrip1__Tab1frame_top_Lbl6.grid(row=2,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny6.grid(row=2,column =1,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl7.grid(row=2,column =2,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny7.grid(row=2,column =3,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl8.grid(row=2,column =4,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny8.grid(row=2,column =5,padx = 3,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Lbl9.grid(row=2,column =6,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Eny9.grid(row=2,column =7,padx = 3,pady = 10,sticky = W)

        self.TabStrip1__Tab1frame_top_Lbl10.grid(row=1,column =4,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab1frame_top_Cox10.grid(row=1,column =5,padx = 3,pady = 10,sticky = W)
        
        ## 
        self.TabStrip1__Tab1frame_top_Bun1.grid(row=3,column =6,padx = 0,pady = 10,sticky = W)
        self.TabStrip1__Tab1frame_top_Bun2.grid(row=3,column =7,padx = 0,pady = 10,sticky = E)

        ## bottom



        ##numberChosen = ttk.Combobox(win, width=12, textvariable=number)
        ##numberChosen['values'] = (1, 2, 4, 42, 100)
        ## 第二页，学员计划安排
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='学员计划安排')
        self.TabStrip1__Tab2Lbl1 = Label(self.TabStrip1__Tab2, text='姓名')
        self.TabStrip1__Tab2Lbl2 = Label(self.TabStrip1__Tab2, text='学期')
        self.TabStrip1__Tab2Lbl3 = Label(self.TabStrip1__Tab2, text='周几上课')
        self.TabStrip1__Tab2Lbl4 = Label(self.TabStrip1__Tab2, text='上课时间')
        self.TabStrip1__Tab2Lbl5 = Label(self.TabStrip1__Tab2, text='下课时间')
        #改成下拉列表
        self.TabStrip1__Tab2Cox1 = Combobox(self.TabStrip1__Tab2)
        self.TabStrip1__Tab2Cox1['values'] = member_list
        ##
        self.TabStrip1__Tab2Cox2 = Combobox(self.TabStrip1__Tab2)
        self.TabStrip1__Tab2Cox2['values'] = term_list
        ##self.TabStrip1__Tab2Eny2 = Entry(self.TabStrip1__Tab2,textvariable=date_pression_1)
        ##self.TabStrip1__Tab2Eny2.bind("<Button-1>",func=self.handler_adaptor(self.date_selection, date_input=date_pression_1))
        #改成下拉列表
        self.TabStrip1__Tab2Cox3 = Combobox(self.TabStrip1__Tab2)
        self.TabStrip1__Tab2Cox3['values'] = weekday_list
        ##
        self.TabStrip1__Tab2Eny4 = Entry(self.TabStrip1__Tab2)
        self.TabStrip1__Tab2Eny5 = Entry(self.TabStrip1__Tab2)
        ## 确认和取消
        self.TabStrip1__Tab2Bun1 = Button(self.TabStrip1__Tab2,text='提交',command = self.submit_plan_add)
        self.TabStrip1__Tab2Bun2 = Button(self.TabStrip1__Tab2,text='取消')
        ## 第二页，布局
        ## 第一行
        self.TabStrip1__Tab2Lbl1.grid(row=0,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab2Cox1.grid(row=0,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab2Lbl2.grid(row=0,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab2Cox2.grid(row=0,column =3,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab2Lbl3.grid(row=1,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab2Cox3.grid(row=1,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab2Lbl4.grid(row=1,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab2Eny4.grid(row=1,column =3,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab2Lbl5.grid(row=1,column =4,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab2Eny5.grid(row=1,column =5,padx = 10,pady = 10,sticky = W)
        ## 第二行
        self.TabStrip1__Tab2Bun1.grid(row=2,column =4,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab2Bun2.grid(row=2,column =5,padx = 10,pady = 10,sticky = W)
        
        ## 第三页，学员补课登记，文本框
        self.TabStrip1__Tab3 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab3, text='学员排课登记')
        self.TabStrip1__Tab3Lbl1 = Label(self.TabStrip1__Tab3, text='姓名')
        self.TabStrip1__Tab3Lbl2 = Label(self.TabStrip1__Tab3, text='排课日期')
        self.TabStrip1__Tab3Lbl3 = Label(self.TabStrip1__Tab3, text='加课时长',)
        #self.TabStrip1__Tab3Lbl3 = Label(self.TabStrip1__Tab3, text='周序')

        self.TabStrip1__Tab3Lbl4 = Label(self.TabStrip1__Tab3, text='上课时间')
        self.TabStrip1__Tab3Lbl5 = Label(self.TabStrip1__Tab3, text='下课时间')
        #改成下拉列表
        self.TabStrip1__Tab3Cox1 = Combobox(self.TabStrip1__Tab3)
        self.TabStrip1__Tab3Cox1['values'] = member_list
        ##
        self.TabStrip1__Tab3Eny2 = Entry(self.TabStrip1__Tab3,textvariable=date_pression_2)
        self.TabStrip1__Tab3Eny2.bind("<Button-1>",func=self.handler_adaptor(self.date_selection, date_input=date_pression_2))

        self.TabStrip1__Tab3Cox3 = Combobox(self.TabStrip1__Tab3,width = 22)
        self.TabStrip1__Tab3Cox3['values'] = [45,60]
        
        #self.TabStrip1__Tab3Eny4 = Entry(self.TabStrip1__Tab3)
        self.TabStrip1__Tab3Cox4 = Combobox(self.TabStrip1__Tab3)
        self.TabStrip1__Tab3Cox4['values'] = time_axis_list
        #self.TabStrip1__Tab3Cox4.bind("<<ComboboxSelected>>",self.set_time_end)
        self.TabStrip1__Tab3Cox4.bind("<Double-Button-1>",self.set_time_end)
        #print(time_end)
        self.TabStrip1__Tab3Eny5 = Entry(self.TabStrip1__Tab3,textvariable = time_end)
        self.TabStrip1__Tab3Eny5['state'] = 'readonly'
        ## 确认和取消
        self.TabStrip1__Tab3Bun1 = Button(self.TabStrip1__Tab3,text='正常排课',command = self.submit_course_plan)
        self.TabStrip1__Tab3Bun2 = Button(self.TabStrip1__Tab3,text='加课 (调整)',command = self.submit_course_adjust_intime)
        self.TabStrip1__Tab3Bun3 = Button(self.TabStrip1__Tab3,text='加课',command = self.submit_course_add)

        ##提示框
        self.TabStrip1__Tab3Lbl6 = Label(self.TabStrip1__Tab3, text=' ')
        ##self.TabStrip1__Tab3Bun2 = Button(self.TabStrip1__Tab3,text='周内补课',command = self.submit_course_add_adjust)
        ## 第三页，布局
        ## 第一行
        self.TabStrip1__Tab3Lbl1.grid(row=0,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab3Cox1.grid(row=0,column =1,padx = 1,pady = 10,sticky = W)
        self.TabStrip1__Tab3Lbl2.grid(row=0,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab3Eny2.grid(row=0,column =3,padx = 1,pady = 10,sticky = W)

        self.TabStrip1__Tab3Lbl3.grid(row=0,column =4,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab3Cox3.grid(row=0,column =5,padx = 1,pady = 10,sticky = W)

        self.TabStrip1__Tab3Lbl4.grid(row=1,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab3Cox4.grid(row=1,column =1,padx = 1,pady = 10,sticky = W)
        self.TabStrip1__Tab3Lbl5.grid(row=1,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab3Eny5.grid(row=1,column =3,padx = 1,pady = 10,sticky = W)
        ## 第三行
        self.TabStrip1__Tab3Bun1.grid(row=2,column =4,padx = 1,pady = 10,sticky = E)
        self.TabStrip1__Tab3Bun2.grid(row=2,column =5,padx = 1,pady = 10,sticky = E)
        self.TabStrip1__Tab3Bun3.grid(row=2,column =5,padx = 1,pady = 10,sticky = W)
        ##self.TabStrip1__Tab3Bun2.grid(row=2,column =5,padx = 10,pady = 10,sticky = W)
        ## 第四行
        self.TabStrip1__Tab3Lbl6.grid(row=4,column =0,padx = 10,pady = 10,columnspan = 4,sticky = W)


        ## 第四页，课程调整
        self.TabStrip1__Tab4 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab4, text='课程总览')
        self.TabStrip1__Tab4frame_center = Frame(self.TabStrip1__Tab4,width=500, height=300)
        self.TabStrip1__Tab4frame_right  = Frame(self.TabStrip1__Tab4,width=100, height=300)

        
        self.TabStrip1__Tab4frame_center.pack(side = LEFT,fill=BOTH,expand='yes')
        self.TabStrip1__Tab4frame_right.pack(side = RIGHT)
        
        self.TabStrip1__Tab4frame_center.pack_propagate(0)
        self.TabStrip1__Tab4frame_right.pack_propagate(0)
        
        self.TabStrip1__Tab4frame_center_tree = Treeview(self.TabStrip1__Tab4frame_center, show="headings", height=18, columns=("a", "b", "c", "d", "e","f","g","h"))
        self.TabStrip1__Tab4frame_center_vbar1 = Scrollbar(self.TabStrip1__Tab4frame_center, orient=VERTICAL, command=self.TabStrip1__Tab4frame_center_tree.yview)
        self.TabStrip1__Tab4frame_center_vbar2 = Scrollbar(self.TabStrip1__Tab4frame_center, orient=HORIZONTAL, command=self.TabStrip1__Tab4frame_center_tree.xview)
        
        self.TabStrip1__Tab4frame_center_tree.configure(yscrollcommand=self.TabStrip1__Tab4frame_center_vbar1.set)
        self.TabStrip1__Tab4frame_center_tree.configure(xscrollcommand=self.TabStrip1__Tab4frame_center_vbar2.set)
        ## 设置行列占比权重
        self.TabStrip1__Tab4frame_center.rowconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.rowconfigure(1, weight=1)
        self.TabStrip1__Tab4frame_center.columnconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.columnconfigure(1, weight=1)

        ##标题长度
        self.TabStrip1__Tab4frame_center_tree.column("a", minwidth=80,width=70,anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("b", minwidth=80,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("c", minwidth=60,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("d", minwidth=60,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("e", minwidth=60,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("f", minwidth=60,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("g", minwidth=100,width=70, anchor="center",stretch = True)
        self.TabStrip1__Tab4frame_center_tree.column("h", minwidth=200,width=10, anchor="center",stretch = True)

        ##标题名称
        self.TabStrip1__Tab4frame_center_tree.heading("a", text="学员姓名")
        self.TabStrip1__Tab4frame_center_tree.heading("b", text="上课日期")
        self.TabStrip1__Tab4frame_center_tree.heading("c", text="星期几")
        self.TabStrip1__Tab4frame_center_tree.heading("d", text="上课时间")
        self.TabStrip1__Tab4frame_center_tree.heading("e", text="下课时间")
        self.TabStrip1__Tab4frame_center_tree.heading("f", text="课程时长")
        self.TabStrip1__Tab4frame_center_tree.heading("g", text="课程状态")
        self.TabStrip1__Tab4frame_center_tree.heading("h", text="原因")

        self.TabStrip1__Tab4frame_center_tree.grid(row=0, column=0, sticky=NSEW )
        self.TabStrip1__Tab4frame_center_vbar1.grid(row=0, column=1, sticky=NSEW)
        self.TabStrip1__Tab4frame_center_vbar2.grid(row=1, column=0, sticky=NSEW)

        

        ## 创建右侧按钮
        self.TabStrip1__Tab4frame_right_Lbl1 = Label(self.TabStrip1__Tab4frame_right, text='学期')
        self.TabStrip1__Tab4frame_right_Lbl2 = Label(self.TabStrip1__Tab4frame_right, text='学期周')
        self.TabStrip1__Tab4frame_right_Lbl3 = Label(self.TabStrip1__Tab4frame_right, text='学员姓名')
        
        self.TabStrip1__Tab4frame_right_Cox1 = Combobox(self.TabStrip1__Tab4frame_right)
        self.TabStrip1__Tab4frame_right_Cox1['values'] = term_list
        self.TabStrip1__Tab4frame_right_Cox1.bind("<<ComboboxSelected>>",self.set_term_order2)
        self.TabStrip1__Tab4frame_right_Cox2 = Combobox(self.TabStrip1__Tab4frame_right)
        self.TabStrip1__Tab4frame_right_Cox2.bind("<<ComboboxSelected>>",self.reflesh_course)

        self.TabStrip1__Tab4frame_right_Cox3 = Combobox(self.TabStrip1__Tab4frame_right)
        self.TabStrip1__Tab4frame_right_Cox3['values'] = member_list
        self.TabStrip1__Tab4frame_right_Cox3.bind("<<ComboboxSelected>>",self.reflesh_course)
        
        self.TabStrip1__Tab4frame_right_bun1 = Button(self.TabStrip1__Tab4frame_right,width=10,text='主动请假',command = self.cancle_class)
        self.TabStrip1__Tab4frame_right_bun2 = Button(self.TabStrip1__Tab4frame_right,width=10,text='恢复正常',command = self.restore_class)
        self.TabStrip1__Tab4frame_right_bun3 = Button(self.TabStrip1__Tab4frame_right,width=10,text='请假 (调整)',command = self.cancle_class_adjust)
        self.TabStrip1__Tab4frame_right_bun4 = Button(self.TabStrip1__Tab4frame_right,width=10,text='刷新',command = self.reflesh_class)
        self.TabStrip1__Tab4frame_right_bun5 = Button(self.TabStrip1__Tab4frame_right,width=10,text='核定',command = self.approval_timetable)
        self.TabStrip1__Tab4frame_right_bun5.configure(state='disabled')
        self.TabStrip1__Tab4frame_right_bun6 = Button(self.TabStrip1__Tab4frame_right,width=10,text='删除记录',command = self.delete_row)

        self.TabStrip1__Tab4frame_right_Lbl4 = Label(self.TabStrip1__Tab4frame_right, text=' ')

        self.TabStrip1__Tab4frame_right_Lbl5 = Label(self.TabStrip1__Tab4frame_right, text='请假原因')
        self.TabStrip1__Tab4frame_right_Eny1 = Entry(self.TabStrip1__Tab4frame_right)
        ## 第四页，布局
        ## 
        ## 第一行
        self.TabStrip1__Tab4frame_right_Lbl1.grid(row=0,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab4frame_right_Cox1.grid(row=0,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab4frame_right_Lbl2.grid(row=1,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab4frame_right_Cox2.grid(row=1,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab4frame_right_Lbl3.grid(row=2,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab4frame_right_Cox3.grid(row=2,column =1,padx = 10,pady = 10,sticky = W)

        self.TabStrip1__Tab4frame_right_bun1.grid(row=3, column=1, sticky=NSEW)
        self.TabStrip1__Tab4frame_right_bun2.grid(row=4, column=1, sticky=NSEW)
        self.TabStrip1__Tab4frame_right_bun3.grid(row=5, column=1, sticky=NSEW)
        self.TabStrip1__Tab4frame_right_bun4.grid(row=6, column=1, sticky=NSEW)
        self.TabStrip1__Tab4frame_right_bun5.grid(row=3, column=2, sticky=NSEW)
        self.TabStrip1__Tab4frame_right_bun6.grid(row=4, column=2, sticky=NSEW)

        
        self.TabStrip1__Tab4frame_right_Lbl5.grid(row=7,column =0,padx = 3,pady =10,sticky = W)
        self.TabStrip1__Tab4frame_right_Eny1.grid(row=7,column =1,padx = 10,columnspan = 2,pady =10,sticky = NSEW)


        self.TabStrip1__Tab4frame_right_Lbl4.grid(row=8,column =0,padx = 10,pady =10,columnspan = 2,sticky = W)

        ##加载数据
        self.load_v_timetable_show()
        

        
        ## 第五页，课表打印
        self.TabStrip1__Tab5 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab5, text='课表打印')
        
        ## 第一行
        self.TabStrip1__Tab5Lbl1 = Label(self.TabStrip1__Tab5, text='学期')
        self.TabStrip1__Tab5Lbl2 = Label(self.TabStrip1__Tab5, text='学期周')
        self.TabStrip1__Tab5Cox1 = Combobox(self.TabStrip1__Tab5)
        self.TabStrip1__Tab5Cox1['values'] = term_list
        self.TabStrip1__Tab5Cox1.bind("<<ComboboxSelected>>",self.set_term_order)
        
        self.TabStrip1__Tab5Cox2 = Combobox(self.TabStrip1__Tab5)
        ##self.TabStrip1__Tab5Cox2['values'] = term_dict['2019B']
        
        self.TabStrip1__Tab5Bun1 = Button(self.TabStrip1__Tab5,text='打印',command = self.Get_Timetable)
        ## 第五页，布局
        ## 第一行
        self.TabStrip1__Tab5Lbl1.grid(row=0,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab5Cox1.grid(row=0,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab5Lbl2.grid(row=0,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab5Cox2.grid(row=0,column =3,padx = 10,pady = 10,sticky = W)

        self.TabStrip1__Tab5Bun1.grid(row=1,column =3,padx = 10,pady = 10,sticky = E)

        ## 第六页，课费平衡情况
        self.TabStrip1__Tab6 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab6, text='课费平衡')
        self.TabStrip1__Tab6frame_center = Frame(self.TabStrip1__Tab6,width=500, height=300)
        self.TabStrip1__Tab6frame_right  = Frame(self.TabStrip1__Tab6,width=200, height=300)

        self.TabStrip1__Tab6frame_center.pack(side = LEFT)
        self.TabStrip1__Tab6frame_right.pack(side = LEFT)
        
        self.TabStrip1__Tab6frame_center_tree = Treeview(self.TabStrip1__Tab6frame_center, show="headings", height=18, columns=("a", "b", "c", "d", "e","f"))
        self.TabStrip1__Tab6frame_center_vbar1 = Scrollbar(self.TabStrip1__Tab6frame_center, orient=VERTICAL, command=self.TabStrip1__Tab6frame_center_tree.yview)
        self.TabStrip1__Tab6frame_center_vbar2 = Scrollbar(self.TabStrip1__Tab6frame_center, orient=HORIZONTAL, command=self.TabStrip1__Tab6frame_center_tree.xview)
        
        self.TabStrip1__Tab6frame_center_tree.configure(yscrollcommand=self.TabStrip1__Tab6frame_center_vbar1.set)
        self.TabStrip1__Tab6frame_center_tree.configure(xscrollcommand=self.TabStrip1__Tab6frame_center_vbar2.set)
        

        ##标题长度
        self.TabStrip1__Tab6frame_center_tree.column("a", minwidth=80,width=100,anchor="center",stretch = 'yes')
        self.TabStrip1__Tab6frame_center_tree.column("b", minwidth=80,width=100, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab6frame_center_tree.column("c", minwidth=60,width=100, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab6frame_center_tree.column("d", minwidth=60,width=100, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab6frame_center_tree.column("e", minwidth=60,width=100, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab6frame_center_tree.column("f", minwidth=60,width=100, anchor="center",stretch = 'yes')
        
        ##标题名称
        self.TabStrip1__Tab6frame_center_tree.heading("a", text="学员姓名")
        self.TabStrip1__Tab6frame_center_tree.heading("b", text="学期")
        self.TabStrip1__Tab6frame_center_tree.heading("c", text="已缴课费")
        self.TabStrip1__Tab6frame_center_tree.heading("d", text="预计课费")
        self.TabStrip1__Tab6frame_center_tree.heading("e", text="课费平衡")
        self.TabStrip1__Tab6frame_center_tree.heading("f", text="课时平衡/45'")
       

        self.TabStrip1__Tab6frame_center_tree.grid(row=0, column=0, sticky=NSEW)
        self.TabStrip1__Tab6frame_center_vbar1.grid(row=0, column=1, sticky=NS)
        self.TabStrip1__Tab6frame_center_vbar2.grid(row=1, column=0, sticky=EW)

        

        ## 创建右侧按钮
        self.TabStrip1__Tab6frame_right_Lbl1 = Label(self.TabStrip1__Tab6frame_right, text='学期')
        self.TabStrip1__Tab6frame_right_Lbl2 = Label(self.TabStrip1__Tab6frame_right, text='学员姓名')

        self.TabStrip1__Tab6frame_right_Cox1 = Combobox(self.TabStrip1__Tab6frame_right)
        self.TabStrip1__Tab6frame_right_Cox1['values'] = term_list
        self.TabStrip1__Tab6frame_right_Cox1.bind("<<ComboboxSelected>>",self.select_payment_balance)

        self.TabStrip1__Tab6frame_right_Cox2 = Combobox(self.TabStrip1__Tab6frame_right)
        self.TabStrip1__Tab6frame_right_Cox2['values'] = member_list
        self.TabStrip1__Tab6frame_right_Cox2.bind("<<ComboboxSelected>>",self.select_payment_balance)

        ## 布局
        self.TabStrip1__Tab6frame_right_Lbl1.grid(row=0,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab6frame_right_Cox1.grid(row=0,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab6frame_right_Lbl2.grid(row=1,column =0,padx = 3,pady = 10,sticky = E)
        self.TabStrip1__Tab6frame_right_Cox2.grid(row=1,column =1,padx = 10,pady = 10,sticky = W)

        ## 第七页，缴费登记
        
        self.TabStrip1__Tab7 = Frame(self.TabStrip1)
        self.TabStrip1.add(self.TabStrip1__Tab7, text='缴费登记')

        self.TabStrip1__Tab7frame_top     = Frame(self.TabStrip1__Tab7,width=700, height=100)
        self.TabStrip1__Tab7frame_bottom  = Frame(self.TabStrip1__Tab7,width=700, height=200)

        self.TabStrip1__Tab7frame_top.pack(side = TOP)
        self.TabStrip1__Tab7frame_bottom.pack(side = BOTTOM,fill=BOTH,expand='yes')
        
        self.TabStrip1__Tab7frame_topLbl1 = Label(self.TabStrip1__Tab7frame_top, text='学员姓名')
        self.TabStrip1__Tab7frame_topLbl2 = Label(self.TabStrip1__Tab7frame_top, text='缴费学期')
        self.TabStrip1__Tab7frame_topLbl3 = Label(self.TabStrip1__Tab7frame_top, text='缴费日期')

        self.TabStrip1__Tab7frame_topLbl4 = Label(self.TabStrip1__Tab7frame_top, text='缴费金额')
        self.TabStrip1__Tab7frame_topLbl5 = Label(self.TabStrip1__Tab7frame_top, text='对应课时')
        
        self.TabStrip1__Tab7frame_topLbl6 = Label(self.TabStrip1__Tab7frame_top, text='缴费途径')
        #改成下拉列表
        self.TabStrip1__Tab7frame_topCox1 = Combobox(self.TabStrip1__Tab7frame_top)
        self.TabStrip1__Tab7frame_topCox1['values'] = member_list
        self.TabStrip1__Tab7frame_topCox1.bind("<<ComboboxSelected>>",self.select_payment_info)

        self.TabStrip1__Tab7frame_topCox2 = Combobox(self.TabStrip1__Tab7frame_top)
        self.TabStrip1__Tab7frame_topCox2['values'] = term_list
        self.TabStrip1__Tab7frame_topCox2.bind("<<ComboboxSelected>>",self.select_payment_info)
        
        self.TabStrip1__Tab7frame_topEny3 = Entry(self.TabStrip1__Tab7frame_top,textvariable=date_pression_2)
        self.TabStrip1__Tab7frame_topEny3.bind("<Button-1>",func=self.handler_adaptor(self.date_selection, date_input=date_pression_2))

        self.TabStrip1__Tab7frame_topEny4 = Entry(self.TabStrip1__Tab7frame_top)
        self.TabStrip1__Tab7frame_topEny5 = Entry(self.TabStrip1__Tab7frame_top)
        self.TabStrip1__Tab7frame_topEny5['state'] = 'readonly'
        self.TabStrip1__Tab7frame_topCox6 = Combobox(self.TabStrip1__Tab7frame_top)
        self.TabStrip1__Tab7frame_topCox6['values'] = payment_way_list
        
        ## 确认和取消
        self.TabStrip1__Tab7frame_topBun1 = Button(self.TabStrip1__Tab7frame_top,text='提交',command = self.submit_payment_add)
        self.TabStrip1__Tab7frame_topBun2 = Button(self.TabStrip1__Tab7frame_top,text='取消')
        ## 第七页，布局
        ## 第一行
        self.TabStrip1__Tab7frame_topLbl1.grid(row=0,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topCox1.grid(row=0,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topLbl2.grid(row=0,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topCox2.grid(row=0,column =3,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topLbl3.grid(row=0,column =4,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topEny3.grid(row=0,column =5,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topLbl4.grid(row=1,column =0,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topEny4.grid(row=1,column =1,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topLbl5.grid(row=1,column =2,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topEny5.grid(row=1,column =3,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topLbl6.grid(row=1,column =4,padx = 10,pady = 10,sticky = E)
        self.TabStrip1__Tab7frame_topCox6.grid(row=1,column =5,padx = 10,pady = 10,sticky = W)
        ## 第二行
        self.TabStrip1__Tab7frame_topBun1.grid(row=2,column =4,padx = 10,pady = 10,sticky = W)
        self.TabStrip1__Tab7frame_topBun2.grid(row=2,column =5,padx = 10,pady = 10,sticky = W)


        ## 第七页底部列表布局
        self.TabStrip1__Tab7frame_bottom_tree = Treeview(self.TabStrip1__Tab7frame_bottom, show="headings", height=7, columns=("a", "b", "c", "d", "e"))
        self.TabStrip1__Tab7frame_bottom_vbar1 = Scrollbar(self.TabStrip1__Tab7frame_bottom, orient=VERTICAL, command=self.TabStrip1__Tab7frame_bottom_tree.yview)
        self.TabStrip1__Tab7frame_bottom_vbar2 = Scrollbar(self.TabStrip1__Tab7frame_bottom, orient=HORIZONTAL, command=self.TabStrip1__Tab7frame_bottom_tree.xview)

        self.TabStrip1__Tab7frame_bottom_tree.configure(yscrollcommand=self.TabStrip1__Tab7frame_bottom_vbar1.set)
        self.TabStrip1__Tab7frame_bottom_tree.configure(xscrollcommand=self.TabStrip1__Tab7frame_bottom_vbar2.set)

        

        ##标题长度
        self.TabStrip1__Tab7frame_bottom_tree.column("a", minwidth=80,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab7frame_bottom_tree.column("b", minwidth=80,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab7frame_bottom_tree.column("c", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab7frame_bottom_tree.column("d", minwidth=60,width=60, anchor="center",stretch = 'yes')
        self.TabStrip1__Tab7frame_bottom_tree.column("e", minwidth=100,width=100,anchor="center",stretch = 'yes')
        
        
        ##标题名称 
        self.TabStrip1__Tab7frame_bottom_tree.heading("a", text="学员姓名")
        self.TabStrip1__Tab7frame_bottom_tree.heading("b", text="缴费金额")
        self.TabStrip1__Tab7frame_bottom_tree.heading("c", text="缴费日期")
        self.TabStrip1__Tab7frame_bottom_tree.heading("d", text="缴费途径")
        self.TabStrip1__Tab7frame_bottom_tree.heading("e", text="学期")
        

        self.TabStrip1__Tab7frame_bottom_tree.grid(row=0, column=0, sticky=NSEW)
        self.TabStrip1__Tab7frame_bottom_vbar1.grid(row=0, column=1, sticky=NS)
        self.TabStrip1__Tab7frame_bottom_vbar2.grid(row=1, column=0, sticky=EW)

        ## 设置行列占比权重
        self.TabStrip1__Tab7frame_bottom.rowconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.rowconfigure(1, weight=1)
        self.TabStrip1__Tab7frame_bottom.columnconfigure(0, weight=1)
        #self.TabStrip1__Tab4frame_center.columnconfigure(1, weight=1)

        
        
 
class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
 
if __name__ == "__main__":
    top = Tk()
    db,cursor = Connect_DB()

    ##获取学员列表
    member_form = []
    member_list = []
    member_form = Fetch_Data(cursor,"""select member_name,member_nickname from member_info where member_id <> 999 and valid = '1' ;""")
    for member in member_form:
        member_list.append(member[0]+'/'+member[1])
    #print(member_list)
    ##-------------
    ##获取学期和学期周列表
    term_form       = []
    term_list       = []
    term_form       = Fetch_Data(cursor,"""select term_name,term_nickname,term_start,term_end from term_info;""")
    days_7          = datetime.timedelta(days=7)
    term_dict       = {}
    term_order_list = []

    for term in term_form:
        term_name     = term[0]
        term_nickname = term[1]
        term_start    = term[2]
        term_end      = term[3]
        term_last     = term_start
        term_list.append(term_name)
        term_order_list = []
        
        while term_last <= term_end:
              term_order_list.append([term_start,term_start+datetime.timedelta(days=6)])
              term_start     = term_start + datetime.timedelta(days=7)
              term_last      = term_start + datetime.timedelta(days=6)
        
        term_dict[term_name] = term_order_list

    #print(term_dict)

    #print(term_dict)
        ##-------------   
    
    
    time_axis_list = ['08:30:00','09:15:00','10:15:00','11:00:00',
                      '13:00:00','13:45:00','14:45:00','15:30:00',
                      '16:30:00','17:15:00','18:45:00','19:30:00',
                      '20:15:00']
    
    ##-------------

    weekday_list=['1','2','3','4','5','6','7']
    
    global time_end
    time_end = StringVar()
    time_end.set(' ')

    member_valid_list = ['是','否']

    payment_way_list = ['alipay','wechat']
    
    default_date = StringVar()
    date_pression_1 = StringVar()
    date_pression_2 = StringVar()
    default_date.set('2012-01-01')
    Application(top).mainloop()
