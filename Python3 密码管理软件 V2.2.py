
#_*_ coding:utf8 _*_

## Python3 密码管理 V2.2
## 2020-06-05
## 需要安装第三方模块 pycryptodome
## 安装方式 pip install pycryptodome
## 1 生成密钥对，设置要保存的用户名和密码
## 2 对【明文密码】使用公钥进行加密后存入本地SQLite3数据库
## 3 提取数据库中【密文密码】使用私钥解密为【明文密码】直接复制到粘贴板中

import os               # 操作Windows文件用
import time
import random

## pycryptodome
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

## 数据库
import sqlite3

## 图形化模块
from tkinter import *
from tkinter import filedialog  # 选择文件用
import tkinter.messagebox       # 弹出提示对话框
from tkinter import ttk         # 下拉菜单控件在ttk中

top = Tk()                          # 初始化Tk()
top.title('Python3 密码管理 V2.2')  # 设置标题
width = 820                      # 设置窗口宽
height = 700                        # 设置窗口高
# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = top.winfo_screenwidth()  
screenheight = top.winfo_screenheight() 
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)   
top.geometry(alignstr)
top.resizable(width=True, height=True)  # 设置窗口是否可变长、宽，True：可变，False：不可变



######## Sqlite3 SQL 语句函数
##
## 数据库操作：执行SQL查询语句，返回执行状态和执行结果（数据列表）
def DEF_SQL_查询和返回(SQL_CMD):
    数据库连接对象 = sqlite3.connect('PWD.DB')     # 尝试打开数据库文件
    print("打开连接")
    try:
        游标对象 = 数据库连接对象.cursor()     # 创建一个游标
    except Exception as e:
        ERROR = '创建游标失败' + str(e)
        return(1, ERROR)
    else:
        print("创建游标")
        try:
            游标对象.execute(SQL_CMD)
        except Exception as e:
            ERROR = f'执行SQL语句 {SQL_CMD} 失败 {e}'
            游标对象.close()
            print("关闭游标")
            return(1, ERROR)
        else:
            全部记录 = 游标对象.fetchall()
            游标对象.close()
            print("关闭游标")
            return(0, 全部记录)

## 执行一条SQL语句
def DEF_SQL_执行(SQL_CMD):
    数据库连接对象 = sqlite3.connect('PWD.DB')     # 尝试打开数据库文件
    print("打开连接")
    try:
        游标对象 = 数据库连接对象.cursor()         # 创建一个游标
    except Exception as e:
        ERROR = '创建游标失败' + str(e)
        return(1, ERROR)
    else:
        print("创建游标")
        try:
            游标对象.execute(SQL_CMD)
        except Exception as e:
            游标对象.close()
            print("关闭游标")
            ERROR = str(e)
            return(1, ERROR)
        else:
            数据库连接对象.commit()           # 提交更改
            游标对象.close()
            print("关闭游标")
            数据库连接对象.close()
            print("关闭连接")
            return(0,)

## 执行SQL脚本
def DEF_SQL_执行脚本(SQL_SCRIPT):
    数据库连接对象 = sqlite3.connect('PWD.DB')     # 尝试打开数据库文件
    print("打开连接")
    try:
        游标对象 = 数据库连接对象.cursor()
    except Exception as e:
        ERROR = str(e)
        return(1, ERROR)
    else:
        print("创建游标")
        try:
            游标对象.executescript(SQL_SCRIPT)      # 执行SQL脚本
        except Exception as e:
            游标对象.close()
            print("关闭游标")
            ERROR = str(e)
            return(1, ERROR)
        else:
            数据库连接对象.commit()                 # 提交更改
            游标对象.close()
            print("关闭游标")
            数据库连接对象.close()
            print("关闭连接")
            return(0,)

## 初始化数据库：PWD表不存在则新建表
def 初始化数据库():
    ## 如果数据表 PWD 不存在则新建
    SQL_CMD = '''CREATE TABLE IF NOT EXISTS PWD(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    PS TEXT,
    USER TEXT,
    PASS TEXT);'''
    R = DEF_SQL_执行(SQL_CMD)
    if R[0] == 0:
        print("初始化数据表 PWD 成功")
    else:
        ERROR = f'初始化数据表 PWD 失败:{R[1]}'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)

## 打开/刷新数据表
def 打开数据库():
    ## 打开数据库，读取数据库密码表内容
    SQL_CMD = 'SELECT * FROM PWD'
    R = DEF_SQL_查询和返回(SQL_CMD)
    if R[0] == 0:
        print("数据库表 PWD 读取成功")
        数据列表 = R[1]
        #print("数据列表", 数据列表)
        ## 显示在界面
        字段列表 = ['ID', 'PS', 'USER', 'PASS']
        字段和数据的存储和展示(字段列表, 数据列表)
    else:
        ERROR = f'数据库表 PWD 读取失败:{R[1]}'
        print(ERROR)
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
##
########


######## 新密钥对操作框
##
def 生成密钥对_明文私钥():
    当前设置密钥长度 = IV_密钥长度.get()
    随机数生成器 = Random.new().read
    密钥对 = RSA.generate(当前设置密钥长度, 随机数生成器)
    
    时间 = time.strftime('%Y%m%d_%H%M%S')
    
    ## 保存公钥
    公钥 = 密钥对.publickey().exportKey()                        # 导出公钥
    新公钥文件名 = f'Python3_Crypto_RSA_{当前设置密钥长度}_PUBLIC_{时间}.pem'
    with open(新公钥文件名, 'wb') as f:
        f.write(公钥)
    print("新公钥文件名", 新公钥文件名)
    
    ## 保存私钥
    私钥 = 密钥对.exportKey()                                    # 导出明文私钥
    新私钥文件名 = f'Python3_Crypto_RSA_{当前设置密钥长度}_PRIVATE_{时间}.pem'
    with open(新私钥文件名, 'wb') as f:
        f.write(私钥)
    print("新私钥文件名（明文私钥）", 新私钥文件名)
    
    INFO = '生成新密钥对完成，长度为：' + str(当前设置密钥长度)
    SV_新密钥对提示信息.set(INFO)
    ## 自动替换为新生成密钥对
    SV_选择公钥文件.set(新公钥文件名)
    Label_公钥提示信息['fg'] = 'green'
    SV_公钥提示信息.set('自动替换为新生成的公钥文件')
    SV_选择私钥文件.set(新私钥文件名)
    Label_私钥提示信息['fg'] = 'green'
    SV_私钥提示信息.set('自动替换为新生成的私钥文件')

def 生成密钥对_密文私钥():
    当前设置密钥长度 = IV_密钥长度.get()
    私钥密码 = SV_新私钥密码.get().strip()
    if 私钥密码 == '':
        print("密文私钥需要设置密码")
        Label_新密钥对提示信息['fg'] = 'red'
        SV_新密钥对提示信息.set('密文私钥需要设置密码')
    else:
        随机数生成器 = Random.new().read
        密钥对 = RSA.generate(当前设置密钥长度, 随机数生成器)
        
        时间 = time.strftime('%Y%m%d_%H%M%S')
        
        ## 保存公钥
        公钥 = 密钥对.publickey().exportKey()                        # 导出公钥
        新公钥文件名 = f'Python3_Crypto_RSA_{当前设置密钥长度}_PUBLIC_{时间}.pem'
        with open(新公钥文件名, 'wb') as f:
            f.write(公钥)
        print("新公钥文件名", 新公钥文件名)
        
        ## 保存私钥
        私钥 = 密钥对.exportKey(passphrase=私钥密码, pkcs=8, protection='scryptAndAES128-CBC')   # 导出密文私钥
        新私钥文件名 = f'Python3_Crypto_RSA_{当前设置密钥长度}_PRIVATE_{时间}.pem'
        with open(新私钥文件名, 'wb') as f:
            f.write(私钥)
        print("新私钥文件名（密文私钥）", 新私钥文件名)
        
        SV_新私钥密码.set('')    # 清空私钥密码输入框
        
        INFO = '生成新密钥对完成，长度为：' + str(当前设置密钥长度)
        SV_新密钥对提示信息.set(INFO)
        ## 自动替换为新生成密钥对
        SV_选择公钥文件.set(新公钥文件名)
        Label_公钥提示信息['fg'] = 'green'
        SV_公钥提示信息.set('自动替换为新生成的公钥文件')
        SV_选择私钥文件.set(新私钥文件名)
        Label_私钥提示信息['fg'] = 'green'
        SV_私钥提示信息.set('自动替换为新生成的私钥文件')

def 生成新密钥对():
    if 私钥是否加密.get():
        print("密文私钥")
        生成密钥对_密文私钥()
    else:
        print("文明私钥")
        生成密钥对_明文私钥()

新密钥对操作框 = LabelFrame(top, text='新密钥对操作框')
IV_密钥长度 = IntVar()
IV_密钥长度.set(1024)               # 设置默认值 1024
SV_新私钥密码 = StringVar()
SV_新密钥对提示信息 = StringVar()
SV_新密钥对提示信息.set('生成密钥需要等待数秒时间')

Label(新密钥对操作框, text='设置新密钥长度').grid(row=0, column=0, sticky='E')                # 新密钥对操作框 0-0
Combobox_密钥长度 = ttk.Combobox(新密钥对操作框, width=5)
Combobox_密钥长度['value'] = (1024, 2048, 3072, 4096)
Combobox_密钥长度.current(0)                            # 默认值中的内容为索引，从0开始
Combobox_密钥长度.grid(row=0, column=1, sticky='E')                                           # 新密钥对操作框 0-1
def 选择后执行函数(event):
    设置新密钥长度 = Combobox_密钥长度.get()
    IV_密钥长度.set(设置新密钥长度)
    print("设置新密钥长度", 设置新密钥长度)
Combobox_密钥长度.bind('<<ComboboxSelected>>', 选择后执行函数)
Label_新密钥对提示信息 = Label(新密钥对操作框, textvariable=SV_新密钥对提示信息)
Label_新密钥对提示信息['fg'] = '#FF6600'
Label_新密钥对提示信息.grid(row=0, column=2)                                                  # 新密钥对操作框 0-2

## 私钥是否加密
def DEF_选择按钮():
    print(私钥是否加密.get())
    if 私钥是否加密.get():
        print("密文私钥")
    else:
        print("文明私钥")
私钥是否加密 = BooleanVar()
选择按钮 = Checkbutton(新密钥对操作框, text='加密私钥', variable=私钥是否加密, command=DEF_选择按钮)
选择按钮.grid(row=1, column=0)                                                                         # 新密钥对操作框 1-0

Label(新密钥对操作框, text='设置新私钥密码').grid(row=1, column=1, sticky='W')                         # 新密钥对操作框 1-1
Entry(新密钥对操作框, textvariable=SV_新私钥密码, width=20, show='*').grid(row=1, column=2)            # 新密钥对操作框 1-2
Button(新密钥对操作框, text='生成新密钥对', command=生成新密钥对).grid(row=1, column=3, sticky='NW')   # 新密钥对操作框 1-3

新密钥对操作框.grid(row=0, column=0, sticky='NW')      ## top 0-0
##
########


######## 公钥文件框
##
SV_选择公钥文件 = StringVar()       ## TK全局变量:可以实时更新显示
SV_公钥提示信息 = StringVar()       ## 显示公钥文件的情况

def DEF_按钮_选择公钥文件():
    选择文件 = filedialog.askopenfilename()
    SV_选择公钥文件.set(选择文件)
    print("SV_选择公钥文件", SV_选择公钥文件)
    ## 选择文件后更新一下提示信息
    Label_公钥提示信息['fg'] = 'green'
    SV_公钥提示信息.set('使用手动选择公钥文件')

公钥操作框 = LabelFrame(top, text='公钥')
Button(公钥操作框, text='选择公钥文件', command=DEF_按钮_选择公钥文件).grid(row=0, column=0, sticky='NW')
Entry(公钥操作框, textvariable=SV_选择公钥文件, width=55).grid(row=0, column=1)
Label_公钥提示信息 = Label(公钥操作框, textvariable=SV_公钥提示信息)
Label_公钥提示信息.grid(row=0, column=2)

默认公钥文件 = '公钥.pem'
if os.path.isfile(默认公钥文件):
    SV_选择公钥文件.set(默认公钥文件)           ## 设置公钥默认存放位置为程序同目录下，方便使用
    Label_公钥提示信息['fg'] = 'green'
    SV_公钥提示信息.set('自动选择默认公钥文件')
else:
    Label_公钥提示信息['fg'] = '#FF6600'
    SV_公钥提示信息.set('加密需要先选择公钥')

公钥操作框.grid(row=1, column=0, sticky='NW')        ## top 1-0
##
########


######## 私钥文件框
##
SV_选择私钥文件 = StringVar()
SV_私钥提示信息 = StringVar()

def DEF_按钮_选择私钥文件():
    选择文件 = filedialog.askopenfilename()
    SV_选择私钥文件.set(选择文件)              # 实时更新显示
    print("SV_选择私钥文件", SV_选择私钥文件)
    Label_私钥提示信息['fg'] = 'green'
    SV_私钥提示信息.set('使用手动选择私钥文件')

私钥操作框 = LabelFrame(top, text='私钥')
Button(私钥操作框, text='选择私钥文件', command=DEF_按钮_选择私钥文件).grid(row=0, column=0, sticky='NW')
Entry(私钥操作框, textvariable=SV_选择私钥文件, width=55).grid(row=0, column=1)
Label_私钥提示信息 = Label(私钥操作框, textvariable=SV_私钥提示信息)
Label_私钥提示信息.grid(row=0, column=2)

默认私钥文件 = '私钥.pem'
if os.path.isfile(默认私钥文件):
    SV_选择私钥文件.set(默认私钥文件)           ## 设置私钥默认存放位置为程序同目录下，方便使用（不安全，私钥加密后可以提高安全性）
    Label_私钥提示信息['fg'] = 'green'
    SV_私钥提示信息.set('自动选择默认私钥文件')
else:
    Label_私钥提示信息['fg'] = '#FF6600'
    SV_私钥提示信息.set('解密需要先选择私钥')

私钥操作框.grid(row=2, column=0, sticky='NW')        ## top 2-0
##
########



######## 私钥密码框
##
私钥密码框 = LabelFrame(top, text='私钥密码框')
Entry_私钥密码 = Entry(私钥密码框, width=15, show='*')
Entry_私钥密码.grid(row=0, column=0)
私钥密码框.grid(row=2, column=1, sticky='W')        ## top 2-1
##
########



######## 存储操作框
##
def 明文存入():
    print("明文存入")
    备注 = Entry_备注.get().strip()
    帐号 = Entry_帐号.get().strip()
    密码 = Entry_密码.get().strip()
    if 备注 == '' or 帐号 == '' or 密码 == '':
        ERROR = '备注/帐号/密码 中有空内容'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        #print(备注,帐号,密码)
        ## 存入数据库
        SQL_插入数据 = f'INSERT INTO PWD (PS, USER, PASS) VALUES ("{备注}", "{帐号}", "{密码}");'
        R_INSERT = DEF_SQL_执行(SQL_插入数据)
        if R_INSERT[0] == 0:
            print("插入数据成功")
            Entry_备注.delete(0, END)         # 界面：清空输入框
            Entry_帐号.delete(0, END)         # 界面：清空输入框
            Entry_密码.delete(0, END)         # 界面：清空输入框
            打开数据库()
        else:
            #print("插入数据失败", R_INSERT[1])
            ERROR = f'插入数据失败:{R_INSERT[1]}'
            tkinter.messagebox.showerror(title='ERROR', message=ERROR)

def 密码加密存入():
    print("密码加密存入")
    备注 = Entry_备注.get().strip()
    帐号 = Entry_帐号.get().strip()
    密码 = Entry_密码.get().strip()
    if 备注 == '' or 帐号 == '' or 密码 == '':
        ERROR = '备注/帐号/密码 中有空内容'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        #print(备注,帐号,密码)
        ## 明文密码加密
        公钥文件 = SV_选择公钥文件.get()
        if 公钥文件.rstrip() == '':
            ERROR = '没有选择公钥文件'
            tkinter.messagebox.showerror(title='ERROR', message=ERROR)
        else:
            try:
                f = open(公钥文件,'r')
            except Exception as E1:
                ERROR = f'打开公钥文件失败:{E1}'
                print(ERROR)
                tkinter.messagebox.showerror(title='ERROR', message=ERROR)
            else:
                print("打开公钥文件成功")
                STR_公钥 = f.read()
                f.close()
                try:
                    OJB_公钥 = RSA.importKey(STR_公钥)
                except Exception as E2:
                    ERROR = f'导入公钥失败:{E2}'
                    print(ERROR)
                    tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                else:
                    公钥_PKCS115 = PKCS1_v1_5.new(OJB_公钥)
                    明文字节码 = 密码.encode('utf8')
                    try:
                        密文字节码 = 公钥_PKCS115.encrypt(明文字节码)   # 公钥加密
                    except Exception as E3:
                        ERROR = f'公钥加密失败:{E3}'
                        print(ERROR)
                        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                    else:
                        print("公钥加密成功")
                        #print(密文字节码)
                        ## 字节类型转成16进制字符串存储到数据库
                        STR_HEX = Bytes2HEX_STR(密文字节码)
                        #print(STR_HEX)
                        
                        ## 存入数据库
                        SQL_插入数据 = f'INSERT INTO PWD (PS, USER, PASS) VALUES ("{备注}", "{帐号}", "{STR_HEX}");'
                        R_INSERT = DEF_SQL_执行(SQL_插入数据)
                        if R_INSERT[0] == 0:
                            print("插入数据成功")
                            Entry_备注.delete(0, END)         # 界面：清空输入框
                            Entry_帐号.delete(0, END)         # 界面：清空输入框
                            Entry_密码.delete(0, END)         # 界面：清空输入框
                            打开数据库()                      # 更新数据库显示框
                        else:
                            ERROR = f'插入数据失败:{R_INSERT[1]}'
                            tkinter.messagebox.showerror(title='ERROR', message=ERROR)

def 帐号密码加密存入():
    print("帐号和密码都加密存储")
    账号加密状态 = 0
    密码加密状态 = 0
    备注 = Entry_备注.get().strip()
    帐号 = Entry_帐号.get().strip()
    密码 = Entry_密码.get().strip()
    if 备注 == '' or 帐号 == '' or 密码 == '':
        ERROR = '备注/帐号/密码 中有空内容'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        #print(备注,帐号,密码)
        ## 明文密码加密
        公钥文件 = SV_选择公钥文件.get()
        if 公钥文件.rstrip() == '':
            ERROR = '没有选择公钥文件'
            print(ERROR)
            tkinter.messagebox.showerror(title='ERROR', message=ERROR)
        else:
            try:
                f = open(公钥文件,'r')
            except Exception as E1:
                ERROR = f'打开公钥文件失败:{E1}'
                print(ERROR)
                tkinter.messagebox.showerror(title='ERROR', message=ERROR)
            else:
                print("打开公钥文件成功")
                STR_公钥 = f.read()
                f.close()
                try:
                    OJB_公钥 = RSA.importKey(STR_公钥)
                except Exception as E2:
                    ERROR = f'导入公钥失败:{E2}'
                    print(ERROR)
                    tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                else:
                    公钥_PKCS115 = PKCS1_v1_5.new(OJB_公钥)
                    
                    ## 公钥加密帐号
                    帐号字节码 = 帐号.encode('UTF8')
                    try:
                        密文帐号字节码 = 公钥_PKCS115.encrypt(帐号字节码)   # 公钥加密
                    except Exception as E3:
                        ERROR = f'公钥加密账号失败:{E3}'
                        print(ERROR)
                        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                    else:
                        print("公钥加密账号成功")
                        #print(密文帐号字节码)
                        ## 字节类型转成16进制字符串存储到数据库
                        STR_HEX_帐号 = Bytes2HEX_STR(密文帐号字节码)
                        #print(STR_HEX_帐号)
                        账号加密状态 = 1
                    
                    ## 公钥加密密码
                    密码字节码 = 密码.encode('utf8')
                    try:
                        密文密码字节码 = 公钥_PKCS115.encrypt(密码字节码)   # 公钥加密
                    except Exception as E4:
                        ERROR = f'公钥加密密码失败:{E4}'
                        print(ERROR)
                        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                    else:
                        print("公钥加密密码成功")
                        #print(密文密码字节码)
                        ## 字节类型转成16进制字符串存储到数据库
                        STR_HEX_密码 = Bytes2HEX_STR(密文密码字节码)
                        #print(STR_HEX_密码)
                        密码加密状态 = 1

                    ## 存入数据库
                    if 账号加密状态 == 密码加密状态 == 1:
                        SQL_插入数据 = f'INSERT INTO PWD (PS, USER, PASS) VALUES ("{备注}", "{STR_HEX_帐号}", "{STR_HEX_密码}");'
                        R_INSERT = DEF_SQL_执行(SQL_插入数据)
                        if R_INSERT[0] == 0:
                            print("插入数据成功")
                            Entry_备注.delete(0, END)         # 界面：清空输入框
                            Entry_帐号.delete(0, END)         # 界面：清空输入框
                            Entry_密码.delete(0, END)         # 界面：清空输入框
                            打开数据库()                      # 更新数据库显示框
                        else:
                            ERROR = f'插入数据失败:{R_INSERT[1]}'
                            tkinter.messagebox.showerror(title='ERROR', message=ERROR)

def 搜索备注信息():
    print("搜索备注信息")
    备注 = Entry_备注.get().strip()
    if 备注 == '':
        ERROR = '备注空内容'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        print("搜索备注", 备注)
        SQL_CMD = f'SELECT * FROM PWD WHERE PS LIKE "%{备注}%"'
        print("SQL_CMD", SQL_CMD)
        R = DEF_SQL_查询和返回(SQL_CMD)
        if R[0] == 0:
            print("执行搜索语句成功")
            数据列表 = R[1]
            #print("数据列表", 数据列表)
            字段列表 = ['ID', 'PS', 'USER', 'PASS']
            字段和数据的存储和展示(字段列表, 数据列表)
        else:
            ERROR = f'执行搜索语句失败:{R[1]}'
            tkinter.messagebox.showerror(title='ERROR', message=ERROR)

存储操作框 = LabelFrame(top, text='存储操作框')
存储操作框.grid(row=3, column=0, sticky='NW', columnspan=2)        ## top 3-0

备注框 = Frame(存储操作框)
备注框.grid(row=1, column=0, sticky='NW')                        ## 存储操作框 1-0
Label(备注框, text='备注').grid(row=0, column=0)                                   ## 存储操作框 备注框 0-0
Entry_备注 = Entry(备注框, width=20)
Entry_备注.grid(row=1, column=0)                                                   ## 存储操作框 备注框 1-0
Button(备注框, text='搜索备注信息', command=搜索备注信息).grid(row=2, column=0)    ## 存储操作框 备注框 2-0

帐号框 = Frame(存储操作框)
帐号框.grid(row=1, column=1, sticky='NW')                        ## 存储操作框 1-1
Label(帐号框, text='帐号').grid(row=0, column=0)                                   ## 存储操作框 帐号框 0-0
Entry_帐号 = Entry(帐号框, width=20)
Entry_帐号.grid(row=1, column=0)                                                   ## 存储操作框 帐号框 1-0

密码框 = Frame(存储操作框)
密码框.grid(row=1, column=2, sticky='NW')                        ## 存储操作框 1-2
Label(密码框, text='密码').grid(row=0, column=0)                                   ## 存储操作框 密码框 0-0
Entry_密码 = Entry(密码框, width=30)
Entry_密码.grid(row=1, column=0)                                                   ## 存储操作框 密码框 1-0

数据库写入框 = Frame(存储操作框)
数据库写入框.grid(row=1, column=3, sticky='ESWN')                ## 存储操作框 1-3
Label(数据库写入框, text='密码存入数据库方式').grid(row=0, column=0, columnspan=3)                                ## 存储操作框 数据库写入框 0-0
Button(数据库写入框, text='  明文存入  ', command=明文存入).grid(row=1, column=0, sticky='NW')                    ## 存储操作框 数据库写入框 1-0
Button(数据库写入框, text='  密码加密存入  ', command=密码加密存入).grid(row=1, column=1, sticky='NW')                    ## 存储操作框 数据库写入框 1-1
Button(数据库写入框, text='  帐号和密码都加密  ', command=帐号密码加密存入).grid(row=1, column=2, sticky='NW')    ## 存储操作框 数据库写入框 1-2

SV_剪贴板提示信息 = StringVar()
Label_剪贴板提示信息 = Label(存储操作框, textvariable=SV_剪贴板提示信息)
Label_剪贴板提示信息['fg'] = '#FF6600'
Label_剪贴板提示信息.grid(row=2, column=0, columnspan=3, sticky='ESWN')        ## 存储操作框 2-0
##
########


######## 密码操作框
##
def 生成随机密码():
    密码长度 = IV_密码位数.get()
    数字字符列表 = ['0','1','2','3','4','5','6','7','8','9']
    大写字母列表 = ['A','B','C','D','E','F','G','H','J','K','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']
    小写字母列表 = ['a','b','c','d','e','f','g','h','j','k','m','n','p','q','r','s','t','u','v','w','x','y','z']
    符号字符列表 = ['`','~','!','@','#','$','%','^','&','*','(',')','-','_','=','+','[','{',']','}','|',';',':','<','.','>','/','?']
    组合列表 = 数字字符列表 + 大写字母列表 + 小写字母列表 + 符号字符列表
    if 密码长度 > 84:
        ERROR = '过长，请设置长度 <= 84'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        random.shuffle(组合列表)
        随机密码 = ''
        for i in range(0, 密码长度):
            随机密码 += 组合列表[i]
        #print(随机密码)
        Entry_密码.delete(0, END)         # 界面：清空输入框
        Entry_密码.insert(END, 随机密码)

## 字节码转16进制格式的字符串
def Bytes2HEX_STR(Bytes):
    STR_HEX = ''
    for i in Bytes:
        STR_HEX += hex(i)[2:].zfill(2)      ## '0x50' 取 '50' 部分，如果不足2个字符，填充0
    return(STR_HEX)

IV_密码位数 = IntVar()
IV_密码位数.set(20)         ## 设置默认密码位数
密码操作框 = LabelFrame(存储操作框, text='')
Label(密码操作框, text='设置密码长度').grid(row=0, column=0, sticky='NW')
Entry(密码操作框, textvariable=IV_密码位数, width=5).grid(row=0, column=1)
Button(密码操作框, text='生成随机密码', command=生成随机密码).grid(row=0, column=2, sticky='NW')
Button(密码操作框, text='刷新数据库', bg='#00FFFF', command=打开数据库).grid(row=0, column=3, sticky='NW')
密码操作框.grid(row=0, column=0, sticky='NW', columnspan=8)
##
########



######## 数据库显示/操作框
##
字典_查询字段_坐标_初值 = {}  # KEY=控件坐标 || VAULE=初始值   || {(控件行号,控件列号):初始值}   || { (0,0):123 }
字典_查询结果_坐标_初值 = {}  # KEY=控件坐标 || VAULE=初始值   || {(控件行号,控件列号):初始值}   || { (0,0):123 }

数据框_定位行 = IntVar()
数据框_定位列 = IntVar()

## 信息复制到剪贴板
def DEF_解密后复制到剪贴板(): 
    控件行号 = 数据框_定位行.get()
    控件列号 = 数据框_定位列.get()
    print("控件行号", 控件行号, "控件列号", 控件列号)
    选中单元格内容 = 字典_查询结果_坐标_初值[(控件行号,控件列号)]
    print("选中单元格内容", 选中单元格内容)
    
    ## 读取选中单元格字符串尝试还原字节类型
    try:
        还原字节码 = bytes.fromhex(选中单元格内容)
    except Exception as E1:
        #print("还原字节码失败，格式有误(非16进制字符串形式", E1)
        ERROR = f'还原字节码失败，格式有误(非16进制字符串形式:{E1}'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
    else:
        #print("还原字节码", type(还原字节码))
        #print(还原字节码)
        ## 尝试加载私钥
        私钥文件 = SV_选择私钥文件.get()
        if 私钥文件.rstrip() == '':
            ERROR = '没有选择私钥文件'
            print(ERROR)
            tkinter.messagebox.showerror(title='ERROR', message=ERROR)
        else:
            try:
                f = open(私钥文件,'r')
            except Exception as E2:
                ERROR = f'打开私钥文件失败:{E2}'
                print(ERROR)
                tkinter.messagebox.showerror(title='ERROR', message=ERROR)
            else:
                print("打开私钥文件成功")
                STR_私钥 = f.read()
                f.close()
                
                ## 根据是否私钥是否被加密分别处理
                私钥密码 = Entry_私钥密码.get()
                if 私钥密码 != '':
                    print("私钥被加密，先解密私钥，再导入使用")
                    try:
                        OJB_私钥 = RSA.importKey(STR_私钥, passphrase=私钥密码)
                    except Exception as E3:
                        ERROR = f'导入私钥失败，私钥【密码错误】或【格式错误】:{E3}'
                        print(ERROR)
                        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                    else:
                        print("导入私钥成功")
                        私钥_PKCS115 = PKCS1_v1_5.new(OJB_私钥) 
                        
                        ## 私钥尝试解密
                        随机数生成器 = Random.new().read
                        try:
                            明文字节码 = 私钥_PKCS115.decrypt(还原字节码, 随机数生成器)
                        except Exception as E4:
                            ERROR = f'私钥解密失败:{E4}'
                            print(ERROR)
                            tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                        else:
                            print("私钥解密成功")
                            明文字符串 = 明文字节码.decode('utf8')
                            top.clipboard_clear()
                            top.clipboard_append(明文字符串)
                            ## 提示哪个数据被复制到剪贴板
                            选中行ID = 字典_查询结果_坐标_初值[(控件行号,0)]
                            选中行列名 = 字典_查询字段_坐标_初值[(0,控件列号)]
                            INFO = f'ID【{选中行ID}】的【{选中行列名}】【解密后内容】 已经复制到剪贴板'
                            #tkinter.messagebox.showinfo(title='INFO', message=INFO)
                            SV_剪贴板提示信息.set(INFO)
                else:
                    print("私钥无加密，直接导入使用")
                    try:
                        OJB_私钥 = RSA.importKey(STR_私钥)
                    except Exception as E3:
                        ERROR = f'导入私钥失败，私钥【被加密】或【格式错误】:{E3}'
                        print(ERROR)
                        tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                    else:
                        print("导入私钥成功")
                        私钥_PKCS115 = PKCS1_v1_5.new(OJB_私钥) 
                        
                        ## 私钥尝试解密
                        随机数生成器 = Random.new().read
                        try:
                            明文字节码 = 私钥_PKCS115.decrypt(还原字节码, 随机数生成器)
                        except Exception as E4:
                            ERROR = f'私钥解密失败:{E4}'
                            print(ERROR)
                            tkinter.messagebox.showerror(title='ERROR', message=ERROR)
                        else:
                            print("私钥解密成功")
                            明文字符串 = 明文字节码.decode('utf8')
                            top.clipboard_clear()
                            top.clipboard_append(明文字符串)
                            ## 提示哪个数据被复制到剪贴板
                            选中行ID = 字典_查询结果_坐标_初值[(控件行号,0)]
                            选中行列名 = 字典_查询字段_坐标_初值[(0,控件列号)]
                            INFO = f'ID【{选中行ID}】的【{选中行列名}】【解密后内容】 已经复制到剪贴板'
                            #tkinter.messagebox.showinfo(title='INFO', message=INFO)
                            SV_剪贴板提示信息.set(INFO)


def DEF_保留原值复制到剪贴板(): 
    控件行号 = 数据框_定位行.get()
    控件列号 = 数据框_定位列.get()
    print("控件行号", 控件行号, "控件列号", 控件列号)
    选中单元格内容 = 字典_查询结果_坐标_初值[(控件行号,控件列号)]
    print("选中单元格内容", 选中单元格内容)
    top.clipboard_clear()
    top.clipboard_append(选中单元格内容)
    
    ## 提示哪个数据被复制到剪贴板
    选中行ID = 字典_查询结果_坐标_初值[(控件行号,0)]
    选中行列名 = 字典_查询字段_坐标_初值[(0,控件列号)]
    INFO = f'ID【{选中行ID}】的【{选中行列名}】【原值】 已经复制到剪贴板'
    #tkinter.messagebox.showinfo(title='INFO', message=INFO)
    SV_剪贴板提示信息.set(INFO)



## 菜单按钮函数：删除整行（提取控件行号信息）
def DEL_ROW():
    控件行号 = 数据框_定位行.get()
    DEF_删除记录(控件行号)
    ## 删除成功后的行列号和当前行列号有差别，立刻设置为无效行列号，防止后面误删
    数据框_定位行.set(-1)
    数据框_定位列.set(-1)

## 菜单按钮函数：删除整行（根据控件行号删除）
def DEF_删除记录(控件行号):
    ID = 字典_查询结果_坐标_初值[(控件行号, 0)]
    print("DELETE ID", ID)
    SQL_CMD = f'DELETE FROM PWD WHERE ID = "{ID}"'
    print("SQL_CMD", SQL_CMD)
    ## 删除记录
    R = DEF_SQL_执行(SQL_CMD)
    if R[0] == 0:
        打开数据库()
    else:
        ERROR = f'删除记录失败:{R[1]}'
        tkinter.messagebox.showerror(title='ERROR', message=ERROR)

## 事件函数：右键菜单
def DEF_弹出_数据框_右键菜单(event):
    # 取值控制坐标
    选中控件 = event.widget
    行 = 选中控件.grid_info()['row']
    列 = 选中控件.grid_info()['column']
    # 赋值控制坐标变量
    数据框_定位行.set(行)
    数据框_定位列.set(列)
    ## 弹出菜单
    光标X轴 = event.x_root
    光标Y轴 = event.y_root
    数据框_右键菜单.post(光标X轴, 光标Y轴)    # 光标位置显示菜单

## 创建数据框右键菜单
数据框_右键菜单 = Menu()
数据框_右键菜单.add_command(label='解密 到 剪贴板', command=DEF_解密后复制到剪贴板)
数据框_右键菜单.add_separator()                                                        # 分隔线
数据框_右键菜单.add_separator()
数据框_右键菜单.add_command(label='原值 到 剪贴板', command=DEF_保留原值复制到剪贴板)
数据框_右键菜单.add_separator()
数据框_右键菜单.add_separator()
数据框_右键菜单.add_command(label='删除此行', command=DEL_ROW)

## 清空框内控件
def FRAME_CLEAR(FRAME_NAME):
    for X in FRAME_NAME.winfo_children():
        X.destroy()

## 在显编框展示结果，保存结果到全局变量
def 字段和数据的存储和展示(L, LL):
    ID宽 = 3
    PS宽 = 55
    USER宽 = 30
    PASS宽 = 20

    行数 = len(LL)
    
    FRAME_CLEAR(LabelFrame_显编框)                    # 清空框内控件
    ## 创建画布
    画布 = Canvas(LabelFrame_显编框, bg='#00CED1')    # 创建画布
    画布.grid(row=0,column=0)                         # 显示画布
    ## 在画布里创建 Frame
    画布Frame框 = Frame(画布)
    字段框 = Frame(画布Frame框)
    字段框.grid(row=0,column=0,sticky='NW')
    数据框 = Frame(画布Frame框)
    数据框.grid(row=1,column=0,sticky='NW')
    
    ## 动态设置画布窗口宽高：根据主主窗口的参数设置限宽限高
    主窗口大小和位置 = top.geometry()
    print("主窗口大小和位置", 主窗口大小和位置)
    主窗口宽, 主窗口高, 主窗口X, 主窗口Y = re.findall('[0-9]+', 主窗口大小和位置)
    print("主窗口宽", 主窗口宽)
    print("主窗口高", 主窗口高)
    if int(主窗口宽) < 500:
        主窗口宽 = width
    else:
        主窗口宽 = int(主窗口宽)
    画布限宽 = 主窗口宽
    print("画布限宽(想和主框同宽)", 画布限宽)

    if int(主窗口高) < 700:
        主窗口高 = height
    else:
        主窗口高 = int(主窗口高)
    画布限高 = int(主窗口高) -500       # 减去显示框上边的内容
    print("画布限高(预计)", 画布限高)
    if 画布限高 < 200:
        画布限高 = 200                  # 保障最小高度
        print("画布限高需要保障最小高度", 画布限高)
    print("画布限宽(实际)", 画布限宽)
    print("画布限高(实际)", 画布限高)
    
    ## 设置画布参数
    
    ## 画布可滚动显示的最大宽和高（要刚好能放下画布里的Frame里的全部控件）
    画布滚动最右边 = (ID宽+PS宽+USER宽+PASS宽)*7 + 19   ## Enter默认宽20==140像素（7像素/每宽）
    画布滚动最下边 = (行数+1)*21 + 3                    ## (数据行数+字段行数)*(每行20高+间隔1像素) + (留空) 
    print("画布包含元素需宽", 画布滚动最右边)
    print("画布包含元素需高", 画布滚动最下边)
    
    ## 动态设置显示画布固定显示宽和高（要和主显示框的大小匹配）
    if 画布限宽 > 画布滚动最右边:
        画布['width'] = 画布滚动最右边
        print("画布限宽>画布包含元素最大宽度，画布宽采用实际需要的宽度", 画布滚动最右边)
    else:
        画布['width'] = 画布限宽 - 30
        print("画布限宽<=画布包含元素最大宽度，画布宽度采用（画布限宽-30）留出右边滚动条的显示位置", 画布限宽-30)
    
    if 画布限高 > 画布滚动最下边:
        画布['height'] = 画布滚动最下边
        print("画布限高>画布包含元素最大高度，画布高采用实际需要的高度", 画布滚动最下边)
    else:
        画布['height'] = 画布限高
        print("画布限高<=画布包含元素最大高度，画布高度采用（画布限高）", 画布限高)
    
    画布['scrollregion'] = (0,0,画布滚动最右边,画布滚动最下边)   # 一个元组 tuple (w, n, e, s) ，定义了画布可滚动的最大区域，w 为左边，n 为头部，e 为右边，s 为底部
    
    # 竖滚动条
    Scrollbar_画布_竖 = Scrollbar(LabelFrame_显编框, command=画布.yview)
    Scrollbar_画布_竖.grid(row=0,column=1,sticky=S+W+E+N)
    
    # 横滚动条
    Scrollbar_画布_横 = Scrollbar(LabelFrame_显编框, command=画布.xview, orient=HORIZONTAL)
    Scrollbar_画布_横.grid(row=1,column=0,sticky=S+W+E+N)

    画布.config(xscrollcommand=Scrollbar_画布_横.set, yscrollcommand=Scrollbar_画布_竖.set) # 自动设置滚动幅度
    画布.create_window((0,0), window=画布Frame框, anchor='nw')

    ## 在 画布里的Frame里创建控件
    # 清除全局字典的内容
    字典_查询字段_坐标_初值.clear()
    字典_查询结果_坐标_初值.clear()
    
    ## 字段名
    ## 固定行：0
    ## 固定列：ID PS USER PASS
    ## ID
    初始值 = str(L[0])                                 # 转成字符串
    字典_查询字段_坐标_初值[(0,0)] = 初始值            # 保存初始值
    输入框对象 = Entry(字段框, width=ID宽, bg='#00BFFF')
    输入框对象.insert(0, 初始值)
    输入框对象.grid(row=0,column=0,sticky='W')
    
    ## PS
    初始值 = str(L[1])
    字典_查询字段_坐标_初值[(0,1)] = 初始值
    输入框对象 = Entry(字段框, width=PS宽, bg='#00BFFF')
    输入框对象.insert(0, 初始值)
    输入框对象.grid(row=0,column=1,sticky='W')
    
    ## USER
    初始值 = str(L[2])
    字典_查询字段_坐标_初值[(0,2)] = 初始值
    输入框对象 = Entry(字段框, width=USER宽, bg='#00BFFF')
    输入框对象.insert(0, 初始值)
    输入框对象.grid(row=0,column=2,sticky='W')
    
    ## PASS
    初始值 = str(L[3])
    字典_查询字段_坐标_初值[(0,3)] = 初始值
    输入框对象 = Entry(字段框, width=PASS宽, bg='#00BFFF')
    输入框对象.insert(0, 初始值)
    输入框对象.grid(row=0,column=3,sticky='W')
    
    ## 数据值
    for 行 in range(0, 行数):
        ## 固定列：ID PS USER PASS
        ## ID
        初始值 = str(LL[行][0])                  # 转成字符串
        字典_查询结果_坐标_初值[(行,0)] = 初始值 # 保存初始值
        输入框对象 = Entry(数据框, width=ID宽)
        输入框对象.insert(0, 初始值)
        输入框对象.grid(row=行,column=0,sticky='W')
        输入框对象.bind("<Button-3>", DEF_弹出_数据框_右键菜单) # 每个控件对象都绑定右键菜单事件
        
        ## PS
        初始值 = str(LL[行][1])                  # 转成字符串
        字典_查询结果_坐标_初值[(行,1)] = 初始值 # 保存初始值
        输入框对象 = Entry(数据框, width=PS宽)
        输入框对象.insert(0, 初始值)
        输入框对象.grid(row=行,column=1,sticky='W')
        输入框对象.bind("<Button-3>", DEF_弹出_数据框_右键菜单) # 每个控件对象都绑定右键菜单事件
        
        ## USER
        初始值 = str(LL[行][2])                  # 转成字符串
        字典_查询结果_坐标_初值[(行,2)] = 初始值 # 保存初始值
        输入框对象 = Entry(数据框, width=USER宽)
        输入框对象.insert(0, 初始值)
        输入框对象.grid(row=行,column=2,sticky='W')
        输入框对象.bind("<Button-3>", DEF_弹出_数据框_右键菜单) # 每个控件对象都绑定右键菜单事件
        
        ## PASS
        初始值 = str(LL[行][3])                  # 转成字符串
        字典_查询结果_坐标_初值[(行,3)] = 初始值 # 保存初始值
        输入框对象 = Entry(数据框, width=PASS宽)
        输入框对象.insert(0, 初始值)
        输入框对象.grid(row=行,column=3,sticky='W')
        输入框对象.bind("<Button-3>", DEF_弹出_数据框_右键菜单) # 每个控件对象都绑定右键菜单事件

LabelFrame_显编框 = LabelFrame(top, text='显示/编辑框', bg='#FFD700')
LabelFrame_显编框.grid(row=4,column=0,sticky='NW',columnspan=2)                         ## top 4-0
##
########



######## SQL命令框
##
## 执行用户输入的SQL语句
def DEF_按钮_执行SQL语句():
    SQL_CMD = 文本框_命令行.get(1.0, END).rstrip('\n')     # 获取编写的SQL语句，去掉后面的回车符号
    if SQL_CMD.strip() != '':
        R = DEF_SQL_执行(SQL_CMD)                      # 调用非查询语句函数
        if R[0] == 0:
            INFO = f'数据库执行SQL语句 {SQL_CMD} 成功'
            打开数据库()     ## 更新一下数据库显示
            tkinter.messagebox.showinfo(title='成功', message=INFO)
        else:
            ERROR = f'数据库执行SQL语句 {SQL_CMD} 失败 {R[1]}'
            tkinter.messagebox.showerror(title='失败', message=ERROR)
    else:
        ERROR = '没有输入SQL语句'
        tkinter.messagebox.showerror(title='错误', message=ERROR)

## 执行用户输入的SQL脚本
def DEF_按钮_执行SQL脚本():
    SQL_CMD = 文本框_命令行.get(1.0, END).rstrip('\n')     # 获取编写的SQL语句，去掉后面的回车符号
    if SQL_CMD.strip() != '':
        R = DEF_SQL_执行脚本(SQL_CMD)                      # 调用非查询语句函数
        if R[0] == 0:
            INFO = f'数据库执行SQL脚本 {SQL_CMD} 成功'
            打开数据库()     ## 更新一下数据库显示
            tkinter.messagebox.showinfo(title='成功', message=INFO)
        else:
            ERROR = f'数据库执行SQL脚本 {SQL_CMD} 失败 {R[1]}'
            tkinter.messagebox.showerror(title='失败', message=ERROR)
    else:
        ERROR = 'SQL脚本无内容'
        tkinter.messagebox.showerror(title='错误', message=ERROR)

## 清除命令框里的内容
def DEF_按钮_清屏():
    文本框_命令行.delete(0.0, END)
    文本框_命令行.focus_set()


命令框 = LabelFrame(top, text='SQL语句/SQL脚本')
命令框.grid(row=5,column=0,sticky='NW',columnspan=2)                                    ## top 5-0

命令行_按钮框 = Text(命令框)
命令行_按钮框.grid(row=1,column=0)
Button(命令行_按钮框, text='执行SQL语句', command=DEF_按钮_执行SQL语句).grid(row=0, column=0)
Button(命令行_按钮框, text='执行SQL脚本', command=DEF_按钮_执行SQL脚本).grid(row=0, column=1)
Button(命令行_按钮框, text='清屏', command=DEF_按钮_清屏).grid(row=0, column=2)

文本框_命令行 = Text(命令框, height=3, wrap='none')
文本框_命令行.grid(row=2,column=0,sticky='NESW')
Scrollbar_命令框_竖 = Scrollbar(命令框) 
Scrollbar_命令框_竖['command'] = 文本框_命令行.yview
Scrollbar_命令框_横 = Scrollbar(命令框) 
Scrollbar_命令框_横['command'] = 文本框_命令行.xview
Scrollbar_命令框_横['orient'] = HORIZONTAL
Scrollbar_命令框_竖.grid(row=2, column=1, sticky=S+W+E+N)
Scrollbar_命令框_横.grid(row=3, column=0, sticky=S+W+E+N)
文本框_命令行.config(xscrollcommand=Scrollbar_命令框_横.set, yscrollcommand=Scrollbar_命令框_竖.set)  # 自动设置滚动条滑动幅度



## 开软件后先执行数据库的初始化和打开
初始化数据库()
打开数据库()



# 进入消息循环
top.mainloop()