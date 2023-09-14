import json
import os
import time
#import cv2
#import numpy as np

#try:
 #   import PIL.Image as Image
#except ImportError:
#    import Image
#import pytesseract
from urllib import parse    
import requests
from pyquery import PyQuery as py

url ='https://www.luogu.com.cn/problem/list'
response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})


#print('状态码：',response.status_code)
#print('请求头：',response.headers)
#print('cookie：',response.cookies)

if response.status_code == 200:
    print('请求成功')
   # print(response.text)
    
else:
    print('请求失败')
    print(response.status_code)
    print(response.text)

doc = py(response.text)

print(doc('title').text())

#验证码url转图片
# def url_to_image(url):
#     response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
#     if response.status_code==200:
#         with open("./demo.jpg","wb") as f:
#             f.write(response.content)
#         p = cv2.imread("./demo.jpg")
#         h,w = p.shape[:2]
#         h,w = h*3,w*3
#         p=cv2.resize(p,(w,h))
#         p = cv2.cvtColor(p,cv2.COLOR_BGR2RGB)
#         thresh,p = cv2.threshold(p,170,255,cv2.THRESH_BINARY)
#         dilate = cv2.dilate(p,np.ones(shape=(6,6)))
#         p = cv2.erode(dilate,np.ones(shape=(5,5)))
#     return Image.open("./demo.jpg")



#模拟用户登录(直接摆烂 验证码识别不出来)
# def login():
#     url = 'https://www.luogu.com.cn/auth/login'
#     loginurl = "https://www.luogu.com.cn/api/auth/userPassLogin"
#     response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
#     print(response.status_code)
#     # print(response.text)

#     data = {
#         'username':'1079396196@qq.com',
#         'password':'qpalzm123789456',
#         #  'captcha': pytesseract.image_to_string('https://www.luogu.com.cn/api/verify/captcha?)
#     }
#     #print(pytesseract.image_to_string(url_to_image('https://www.luogu.com.cn/api/verify/captcha')))
    
#     session = requests.session()
#     response = session.post(loginurl,data=data,headers={'User-Agent':'Mozilla/5.0'})
#     print(response.cookies)
#     return response


#利用tkinter库制作 筛选题目 的gui页面
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from pyquery import PyQuery as py


window = tk.Tk()
window.title('洛谷题目筛选')
window.geometry('800x600')
frame1 = tk.Frame(window,width=300,height=600,relief='sunken',padx=10,pady=10,borderwidth=5,highlightbackground='black',highlightthickness=5)
frame2 = tk.Frame(window,width=500,height=600,relief='sunken',borderwidth=5,highlightbackground='black',highlightthickness=5)
frame3 = tk.Frame(frame2,width=400,height=500,relief='sunken',borderwidth=5,highlightbackground='black',highlightthickness=5)
frame1.pack(side='left',padx=10,pady=10)
frame2.pack(side='right',padx=10,pady=10)
frame3.pack(side='top',padx=50,pady=50,ipadx=0,ipady=0)



#筛选条件有题目难度/算法/来源/标题/题目编号
#筛选条件-题目难度
label = tk.Label(frame1,text='题目难度',font=('Arial',12),width=30,height=2)
label.pack()
label.place(x=0,y=0)
problem_difficulty = tk.StringVar()
#用下拉菜单控件做一个 题目难度包括入门，普及-，普及/提高-，普及+/提高，提高+/省选-，省选/NOI-，NOI/NOI+/CTSC 的筛选
def problem_difficulty_select():
    global problem_difficulty
    print(problem_difficulty.get())

cmb = ttk.Combobox(frame1,textvariable=problem_difficulty,state='readonly')
cmb.pack()
cmb.place(x=50,y=50)
cmb['value'] = ('全部','入门','普及-','普及/提高-','普及+/提高','提高+/省选-','省选/NOI-','NOI/NOI+/CTSC')
cmb.current(0)
cmb.bind("<<ComboboxSelected>>",problem_difficulty_select)
def translate():
    if(problem_difficulty.get()==('入门')):
        return '1'
    if(problem_difficulty.get()==('普及-')):
        return '2'
    if(problem_difficulty.get()==('普及/提高-')):
        return '3'
    if(problem_difficulty.get()==('普及+/提高')):
        return '4'
    if(problem_difficulty.get()==('提高+/省选-')):
        return '5'
    if(problem_difficulty.get()==('省选/NOI-')):
        return '6'
    if(problem_difficulty.get()==('NOI/NOI+/CTSC')):
        return '7'
    else:
        return '0'


#筛选条件-算法、来源、时间、状态

label = tk.Label(frame1,text='类型',font=('Arial',12),width=30,height=2)
label.pack()
label.place(x=0,y=100)

problem_algorithm = tk.StringVar()

def problem_algorithm_select():
    global problem_algorithm
    print(problem_algorithm.get())

cmp0 = ttk.Combobox(frame1,textvariable=problem_algorithm,state='readonly')
cmp0.pack()
cmp0.place(x=50,y=150)
cmp0['value'] = ('不是这个也有点太多了','语言入门(请选择[入门与面试题库])','顺序结构','分支结构','循环结构','数组','字符串(入门)','结构体','函数与递归')
cmp0.current(0)
cmp0.bind("<<ComboboxSelected>>",problem_algorithm_select)



#筛选条件-来源
label = tk.Label(frame1,text='关键词',font=('Arial',12),width=30,height=2)
label.pack()
label.place(x=0,y=200)

problem_key = tk.StringVar()

def problem_key_select():
    global problem_key
    print(problem_key.get())

entry = tk.Entry(frame1,textvariable=problem_key)
entry.pack()
entry.place(x=50,y=250)




#搜索按钮
def button_click():
    if(translate()!='0'):
        url = 'https://www.luogu.com.cn/problem/list?' +'keyword='+problem_key.get() + '&difficulty='+translate()
    else:
        url = 'https://www.luogu.com.cn/problem/list?' +'keyword='+problem_key.get()
    response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
    print(url)
    doc=py(response.text)
    problem_title_show.set(doc('.lg-container>ul').text().split('\n'))

                
paqv = tk.Button(frame1,text='搜索',font=('Arial',12),width=10,height=2,command=button_click)
paqv.pack()
paqv.place(x=75,y=450)




#展示爬取的标题
label = tk.Label(frame2,text='爬取的标题',font=('Arial',12),width=30,height=2)
label.pack()
label.place(x=50,y=0)

problem_title_show = tk.StringVar()
def problem_title_show_select():
    global problem_title_show
    print(problem_title_show.get())

listbox = tk.Listbox(frame3,font=('Arial',12),width=30,height=20,listvariable=problem_title_show)
#以回车为分隔符分割标题
problem_title_show.set(doc('.lg-container>ul').text().split('\n'))

listbox.pack()



#下载题目题解按钮
def download_click():
    #对于每一道题，以markdown格式存储在本地
    #获取每一道题的url
    if(translate()!='0'):
        url = 'https://www.luogu.com.cn/problem/list?' +'keyword='+problem_key.get() + '&difficulty='+translate()
    else:
        url = 'https://www.luogu.com.cn/problem/list?' +'keyword='+problem_key.get()
    response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
    doc=py(response.text)
    items = doc('.lg-container>ul>li>a')
    url2 = 'https://www.luogu.com.cn/problem/P1000'
    response2 = requests.get(url2,timeout=3,headers={'User-Agent':'Mozilla/5.0'},cookies={'__client_id':'2b48ff961a82eb567359c84f8491b9efa241a354','_uid':'1093533','login_referer':'https%3A%2F%2Fwww.luogu.com.cn%2Fuser%2F1093533','C3VK':'77f282'})
    # doc2 = py(response2.text)
    # print(doc2('article').text())

    
    
    for item in items:
        #print(py(item).attr('href'))
        url = 'https://www.luogu.com.cn/problem/'+py(item).attr('href')
        url2 = 'https://www.luogu.com.cn/problem/solution/'+py(item).attr('href')
        response = requests.get(url,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
        response2 = requests.get(url2,timeout=3,headers={'User-Agent':'Mozilla/5.0'})
        doc = py(response.text)
        title = doc('title').text()
        print(title)
        if(os.path.exists('../'+problem_difficulty.get()+'/'+title+'_'+py(item).attr('href'))):
            print('已经爬取过了')
            continue
        else:   
            os.makedirs('../'+problem_difficulty.get()+'/'+title+'_'+py(item).attr('href')+'/')
            with open('../'+problem_difficulty.get()+'/'+title+'_'+py(item).attr('href')+'/'+title+'_'+py(item).attr('href')+'.md','w',encoding='utf-8') as f:
               f.write(doc('article').text())
               print('爬取成功') 
download = tk.Button(frame2,text='下载题目',font=('Arial',12),width=15,height=2,command=download_click)
download.pack()
download.place(x=125,y=457)




    




window.mainloop()





