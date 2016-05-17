#!/usr/bin/python
#coding=utf-8

'''
1 提取加热温控
2 提取药液温控
3 浓缩加热温控
4 浓缩药液温控
5 提取加热
6 凝缩加热
7 真空泵启动
'''

from Tkinter import *
import serial
import tkMessageBox
from os import system
import time

root = Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
UI_bg = '#2CC55F'
bt_bg = '#F3FFD6'
bt_pressed = '#FF222A'
light_red = '#FF222A'
light_green = '#71FF00'
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
flag4 = 0
flag6 = 0
flag7 = 0

def UI_reboot():
	system('sudo reboot')

def UI_shutdown():
	system('sudo shutdown -h now')

def UI_entry():
	global ser
	global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15
	
	#ser = serial.Serial('/dev/ttyACM0', 9600)
	t1 = Toplevel(height=h, width=w)
	t1.attributes("-fullscreen", 1)
	t1.resizable = (False, False)
	t1.configure(background = UI_bg)

	f1 = Frame(t1)
	f1.pack(expand=YES)
	f1.configure(background = UI_bg)
	
	Label(f1, height=2, bg=UI_bg).grid(row=0, column=1)
	Label(f1, text='小型中药提取浓缩回收系统', font=("黑体", 20, "bold"), bg=UI_bg).grid(row=1, columnspan=18)
	Label(f1, height=1, bg=UI_bg).grid(row=2, column=1)
	Label(f1, text='型号   TNH-30', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=3, columnspan=18)
	Label(f1, height=2, bg=UI_bg).grid(row=4, column=1)
	
	Label(f1, text='。', font=("圆体", 30, "bold"), fg=light_red, bg=UI_bg).grid(row=5, column=0, columnspan=4)
	Label(f1, text='。', font=("圆体", 30, "bold"), fg=light_red, bg=UI_bg).grid(row=5, column=5, columnspan=4)
	Label(f1, text='。', font=("圆体", 30, "bold"), fg=light_red, bg=UI_bg).grid(row=5, column=10, columnspan=4)
	Label(f1, text='。', font=("圆体", 30, "bold"), fg=light_red, bg=UI_bg).grid(row=5, column=15, columnspan=4)
	
	Label(f1, height=1, bg=UI_bg).grid(row=6, column=1)
	l1 = Label(f1, text='0', bg=UI_bg).grid(row=7, column=0, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=3)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=4)
	l2 = Label(f1, text='0', bg=UI_bg).grid(row=7, column=5, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=8)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=9)
	l3 = Label(f1, text='0', bg=UI_bg).grid(row=7, column=10, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=13)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=14)
	l4 = Label(f1, text='0', bg=UI_bg).grid(row=7, column=15, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=18)
	Label(f1, height=1, bg=UI_bg).grid(row=8, column=1)	

	b1 = Button(f1, text='0', command=write_arduino_b1, width=2, height=2, bg=bt_bg)
	b1.grid(row=9, column=0)
	b2 = Button(f1, text='0', command=write_arduino_b2, width=2, height=2, bg=bt_bg)
	b2.grid(row=9, column=1)
	b3 = Button(f1, text='0', command=write_arduino_b3, width=2, height=2, bg=bt_bg)
	b3.grid(row=9, column=2)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=3)

	b4 = Button(f1, text='0', command=write_arduino_b4, width=2, height=2, bg=bt_bg)
	b4.grid(row=9, column=5)
	b5 = Button(f1, text='0', command=write_arduino_b5, width=2, height=2, bg=bt_bg)
	b5.grid(row=9, column=6)
	b6 = Button(f1, text='0', command=write_arduino_b6, width=2, height=2, bg=bt_bg)
	b6.grid(row=9, column=7)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=8)

	b7 = Button(f1, text='0', command=write_arduino_b7, width=2, height=2, bg=bt_bg)
	b7.grid(row=9, column=10)
	b8 = Button(f1, text='0', command=write_arduino_b8, width=2, height=2, bg=bt_bg)
	b8.grid(row=9, column=11)
	b9 = Button(f1, text='0', command=write_arduino_b9, width=2, height=2, bg=bt_bg)
	b9.grid(row=9, column=12)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=13)

	b10 = Button(f1, text='0', command=write_arduino_b10, width=2, height=2, bg=bt_bg)
	b10.grid(row=9, column=15)
	b11 = Button(f1, text='0', command=write_arduino_b11, width=2, height=2, bg=bt_bg)
	b11.grid(row=9, column=16)
	b12 = Button(f1, text='0', command=write_arduino_b12, width=2, height=2, bg=bt_bg)
	b12.grid(row=9, column=17)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=18)

	Label(f1, height=1, bg=UI_bg).grid(row=10, column=1)
	Label(f1, text='提取加热温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=0, columnspan=4)
	Label(f1, text='提取药液温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=5, columnspan=4)
	Label(f1, text='浓缩加热温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=10, columnspan=4)
	Label(f1, text='浓缩药液温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=15, columnspan=4)

	Label(f1, height=4, bg=UI_bg).grid(row=12, column=1)
	b13 = Button(f1, text='提取加热', command=write_arduino_b13, height=2, bg=bt_bg)
	b13.grid(row=13, column=2, columnspan=4)
	b14 = Button(f1, text='凝缩加热', command=write_arduino_b14, height=2, bg=bt_bg)
	b14.grid(row=13, column=7, columnspan=4)
	b15 = Button(f1, text='真空泵启动', command=write_arduino_b15, height=2, bg=bt_bg)
	b15.grid(row=13, column=12, columnspan=4)
	Label(f1, height=5, bg=UI_bg).grid(row=14, column=1)

	Label(f1, text='山东  泰安市阳光亮化工程有限公司', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=15, columnspan=18)
	Label(f1, height=1, bg=UI_bg).grid(row=16, column=1)
	Label(f1, text='www.talhgc.com   0538-3076228', font=("黑体", 8, "bold"), bg=UI_bg).grid(row=17, columnspan=18)
	Label(f1, height=2, bg=UI_bg).grid(row=18, column=1)

def write_arduino_b1():
	global ser
	global b1
	global flag1
	if int(b1["text"]) == 3:
		b1["text"] = "0"
	else:
		b1["text"] = str(int(b1["text"]) + 1)
	flag1 = 1

def write_arduino_b2():
	global ser
	global b2
	global flag1 
	if int(b2["text"]) == 9:
		b2["text"] = "0"
	else:
                b2["text"] = str(int(b2["text"]) + 1)
        flag1 = 1

def write_arduino_b3():
        global ser
        global b3
        global flag1 
        if int(b3["text"]) == 9:
                b3["text"] = "0"
        else:
                b3["text"] = str(int(b3["text"]) + 1)
        flag1 = 1

def write_arduino_b4():
        global ser
        global b4
        global flag2 
        if int(b4["text"]) == 3:
                b4["text"] = "0"
        else:
                b4["text"] = str(int(b4["text"]) + 1)
        flag2 = 1

def write_arduino_b5():
        global ser
        global b5
        global flag2 
        if int(b5["text"]) == 9:
                b5["text"] = "0"
        else:
                b5["text"] = str(int(b5["text"]) + 1)
        flag2 = 1

def write_arduino_b6():
        global ser
        global b6
        global flag2
        if int(b6["text"]) == 9:
                b6["text"] = "0"
        else:
                b6["text"] = str(int(b6["text"]) + 1)
        flag2 = 1

def write_arduino_b7():
        global ser
        global b7
        global flag3
        if int(b7["text"]) == 3:
                b7["text"] = "0"
        else:
                b7["text"] = str(int(b7["text"]) + 1)
        flag3 = 1

def write_arduino_b8():
        global ser
        global b8
        global flag3
        if int(b8["text"]) == 9:
                b8["text"] = "0"
        else:
                b8["text"] = str(int(b8["text"]) + 1)
        flag3 = 1

def write_arduino_b9():
        global ser
        global b9
        global flag3
        if int(b9["text"]) == 9:
                b9["text"] = "0"
        else:
                b9["text"] = str(int(b9["text"]) + 1)
        flag3 = 1

def write_arduino_b10():
        global ser
        global b10
        global flag4
        if int(b10["text"]) == 3:
                b10["text"] = "0"
        else:
                b10["text"] = str(int(b10["text"]) + 1)
        flag4 = 1

def write_arduino_b11():
        global ser
        global b11
        global flag4
        if int(b11["text"]) == 9:
                b11["text"] = "0"
        else:
                b11["text"] = str(int(b11["text"]) + 1)
        flag4 = 1

def write_arduino_b12():
        global ser
        global b12
        global flag4
        if int(b12["text"]) == 9:
                b12["text"] = "0"
        else:
                b12["text"] = str(int(b12["text"]) + 1)
        flag4 = 1

def write_arduino_b13():
        global ser
        global b13
        if b13["bg"] == bt_pressed:
                b13["bg"] = bt_bg
		#ser.write('51')
        	time.sleep(0.1)
	else:
                b13["bg"] = bt_pressed
		#ser.write('50')
		time.sleep(0.1)
        #print(ser.readline())

def write_arduino_b14():
        global ser
        global b14
        if b14["bg"] == bt_pressed:
                b14["bg"] = bt_bg
                #ser.write('61')
		time.sleep(0.1)
        else:
                b14["bg"] = bt_pressed
                #ser.write('60')
		time.sleep(0.1)
        #print(ser.readline())

def write_arduino_b15():
        global ser
        global b15
        if b15["bg"] == bt_pressed:
                b15["bg"] = bt_bg
                #ser.write('71')
		time.sleep(0.1)
        else:
                b15["bg"] = bt_pressed
                #ser.write('70')
		time.sleep(0.1)
        #print(ser.readline())


frame = Frame(root)
frame.pack()
Label(frame, height=35).grid(rowspan=9,columnspan=5)

button = Button(frame, text='重启', command=UI_reboot, width=7, height=3, bg=bt_bg)
button.grid(row=10, column=0)
Label(frame, width=7).grid(row=10, column=1)
button1 = Button(frame, text='关机', command=UI_shutdown, width=7, height=3, bg=bt_bg)
button1.grid(row=10, column=2)
Label(frame, width=7).grid(row=10, column=3)
button2 = Button(frame, text='进入', command=UI_entry, width=7, height=3, bg=bt_bg)
button2.grid(row=10, column=4)

root.geometry('{}x{}+{}+{}'.format(w, h, 0, 0))
#root.attributes("-topmost", 1)
root.resizable(False, False)
root.title("Controller")
root.attributes("-fullscreen", 1)
#root.configure(backgound = 'blue')

root.mainloop()
