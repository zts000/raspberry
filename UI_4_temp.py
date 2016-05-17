#!/usr/bin/python
#coding=utf-8

'''
1 提取加热温控	raspi直接控制 端口按顺序如pin所示
2 提取药液温控	
3 浓缩加热温控	
4 浓缩药液温控	
5 提取加热 
6 凝缩加热 
7 真空泵启动 
input signal: sss111222333444eee arduino
'''

from Tkinter import *
import serial
import tkMessageBox
from os import system
import time
import threading
import ttk
import RPi.GPIO as GPIO

root = Tk()
isOpened = threading.Event()

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
flag5 = 0
flag6 = 0
flag7 = 0
cfg_file = "/home/workspace/cfg"

pin = [17, 18, 27, 22, 23, 24, 25]
GPIO.setmode(GPIO.BCM)
for pin1 in pin:
	GPIO.setup(pin1, GPIO.OUT)
	GPIO.setup(pin1, GPIO.LOW)

temperature1 = "100"
temperature2 = "100"
temperature3 = "100"
temperature4 = "100"
file_handler = open(cfg_file, "r")
try:
	temperature1 = file_handler.readline()[0:3]
	temperature2 = file_handler.readline()[0:3]
	temperature3 = file_handler.readline()[0:3]
	temperature4 = file_handler.readline()[0:3]
finally:
	file_handler.close()

def UI_reboot():
	system('sudo reboot')

def UI_shutdown():
	system('sudo shutdown -h now')

def UI_entry():
	global ser, mutex
	global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15
	global l1, l2, l3, l4
	global light1, light2, light3, light4

	ser = serial.Serial('/dev/ttyACM0', 9600)
	#isOpened.clear()

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
	Label(f1, height=1, bg=UI_bg).grid(row=4, column=1)
	
	light1 = Label(f1, text='。', font=("圆体", 40, "bold"), fg=light_red, bg=UI_bg)
	light1.grid(row=5, column=0, columnspan=5)
	light2 = Label(f1, text='。', font=("圆体", 40, "bold"), fg=light_red, bg=UI_bg)
	light2.grid(row=5, column=5, columnspan=5)
	light3 = Label(f1, text='。', font=("圆体", 40, "bold"), fg=light_red, bg=UI_bg)
	light3.grid(row=5, column=10, columnspan=5)
	light4 = Label(f1, text='。', font=("圆体", 40, "bold"), fg=light_red, bg=UI_bg)
	light4.grid(row=5, column=15, columnspan=5)
	
	Label(f1, height=1, bg=UI_bg).grid(row=6, column=1)
	l1 = Button(f1, text='0',font=("黑体", 15, "bold"), bd=0, state='disabled', width=7, height=1, bg=bt_bg)
        l1.grid(row=7, column=0, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=3)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=4)
	l2 = Button(f1, text='0',font=("黑体", 15, "bold"), bd=0, state='disabled', width=7, height=1, bg=bt_bg)
        l2.grid(row=7, column=5, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=8)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=9)
	l3 = Button(f1, text='0',font=("黑体", 15, "bold"), bd=0, state='disabled', width=7, height=1, bg=bt_bg)
        l3.grid(row=7, column=10, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=13)
	Label(f1, width=2, bg=UI_bg).grid(row=7, column=14)
	l4 = Button(f1, text='0',font=("黑体", 15, "bold"), bd=0, state='disabled', width=7, height=1, bg=bt_bg)
        l4.grid(row=7, column=15, columnspan=3)
	Label(f1, text='度', bg=UI_bg).grid(row=7, column=18)
	Label(f1, height=1, bg=UI_bg).grid(row=8, column=1)	

	b1 = Button(f1, text=temperature1[0], font=("黑体", 15, "bold"), command=write_arduino_b1, width=1, height=1, bg=bt_bg)
	b1.grid(row=9, column=0)
	b2 = Button(f1, text=temperature1[1], font=("黑体", 15, "bold"), command=write_arduino_b2, width=1, height=1, bg=bt_bg)
	b2.grid(row=9, column=1)
	b3 = Button(f1, text=temperature1[2], font=("黑体", 15, "bold"), command=write_arduino_b3, width=1, height=1, bg=bt_bg)
	b3.grid(row=9, column=2)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=3)

	b4 = Button(f1, text=temperature2[0], font=("黑体", 15, "bold"), command=write_arduino_b4, width=1, height=1, bg=bt_bg)
	b4.grid(row=9, column=5)
	b5 = Button(f1, text=temperature2[1], font=("黑体", 15, "bold"), command=write_arduino_b5, width=1, height=1, bg=bt_bg)
	b5.grid(row=9, column=6)
	b6 = Button(f1, text=temperature2[2], font=("黑体", 15, "bold"), command=write_arduino_b6, width=1, height=1, bg=bt_bg)
	b6.grid(row=9, column=7)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=8)

	b7 = Button(f1, text=temperature3[0], font=("黑体", 15, "bold"), command=write_arduino_b7, width=1, height=1, bg=bt_bg)
	b7.grid(row=9, column=10)
	b8 = Button(f1, text=temperature3[1], font=("黑体", 15, "bold"), command=write_arduino_b8, width=1, height=1, bg=bt_bg)
	b8.grid(row=9, column=11)
	b9 = Button(f1, text=temperature3[2], font=("黑体", 15, "bold"), command=write_arduino_b9, width=1, height=1, bg=bt_bg)
	b9.grid(row=9, column=12)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=13)

	b10 = Button(f1, text=temperature4[0], font=("黑体", 15, "bold"), command=write_arduino_b10, width=1, height=1, bg=bt_bg)
	b10.grid(row=9, column=15)
	b11 = Button(f1, text=temperature4[1], font=("黑体", 15, "bold"), command=write_arduino_b11, width=1, height=1, bg=bt_bg)
	b11.grid(row=9, column=16)
	b12 = Button(f1, text=temperature4[2], font=("黑体", 15, "bold"), command=write_arduino_b12, width=1, height=1, bg=bt_bg)
	b12.grid(row=9, column=17)
	Label(f1, text='度', bg=UI_bg).grid(row=9, column=18)

	Label(f1, height=1, bg=UI_bg).grid(row=10, column=1)
	Label(f1, text='提取加热温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=0, columnspan=4)
	Label(f1, text='提取药液温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=5, columnspan=4)
	Label(f1, text='浓缩加热温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=10, columnspan=4)
	Label(f1, text='浓缩药液温控', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=11, column=15, columnspan=4)

	Label(f1, height=2, bg=UI_bg).grid(row=12, column=1)
	b13 = Button(f1, text='提取加热', font=("圆体", 10, "bold"), command=write_arduino_b13, width=6, height=2, bg=bt_bg)
	b13.grid(row=13, column=2, columnspan=4)
	b14 = Button(f1, text='凝缩加热', font=("圆体", 10, "bold"), command=write_arduino_b14, width=6, height=2, bg=bt_bg)
	b14.grid(row=13, column=7, columnspan=4)
	b15 = Button(f1, text='真空泵启动', font=("圆体", 10, "bold"), command=write_arduino_b15, width=6, height=2, bg=bt_bg)
	b15.grid(row=13, column=12, columnspan=4)
	Label(f1, height=1, bg=UI_bg).grid(row=14, column=1)

	b16 = Button(f1, text='重启', command=UI_reboot, height=2, bg=bt_bg)
	b16.grid(row=15, column=5, columnspan=4)
	b17 = Button(f1, text='关机', command=UI_shutdown, height=2, bg=bt_bg)
	b17.grid(row=15, column=9, columnspan=4)
	Label(f1, height=2, bg=UI_bg).grid(row=16, column=1)
	

	Label(f1, text='山东  泰安市阳光亮化工程有限公司', font=("黑体", 10, "bold"), bg=UI_bg).grid(row=17, columnspan=18)
	Label(f1, height=1, bg=UI_bg).grid(row=18, column=1)
	Label(f1, text='www.talhgc.com   0538-3076228', font=("黑体", 8, "bold"), bg=UI_bg).grid(row=19, columnspan=18)
	Label(f1, height=2, bg=UI_bg).grid(row=20, column=1)

        com_thread = threading.Thread(target=COMTrce)
	com_thread.setDaemon(True)
	com_thread.start()
	mutex = threading.Lock()	

def write_arduino_b1():
	global b1, mutex
	global flag1
	if int(b1["text"]) >= 3:
		b1["text"] = "0"
	else:
		b1["text"] = str(int(b1["text"]) + 1)
	if mutex.acquire(1):
		flag1 = 1
		mutex.release()

def write_arduino_b2():
	global b2, mutex
	global flag1 
	if int(b2["text"]) >= 9:
		b2["text"] = "0"
	else:
                b2["text"] = str(int(b2["text"]) + 1)
        if mutex.acquire(1):
                flag1 = 1
                mutex.release()

def write_arduino_b3():
        global b3, mutex
        global flag1 
        if int(b3["text"]) >= 9:
                b3["text"] = "0"
        else:
                b3["text"] = str(int(b3["text"]) + 1)
        if mutex.acquire(1):
                flag1 = 1
                mutex.release()

def write_arduino_b4():
        global b4, mutex
        global flag2 
        if int(b4["text"]) >= 3:
                b4["text"] = "0"
        else:
                b4["text"] = str(int(b4["text"]) + 1)
        if mutex.acquire(1):
                flag2 = 1
                mutex.release()

def write_arduino_b5():
        global b5, mutex
        global flag2 
        if int(b5["text"]) >= 9:
                b5["text"] = "0"
        else:
                b5["text"] = str(int(b5["text"]) + 1)
        if mutex.acquire(1):
                flag2 = 1
                mutex.release()

def write_arduino_b6():
        global b6, mutex
        global flag2
        if int(b6["text"]) >= 9:
                b6["text"] = "0"
        else:
                b6["text"] = str(int(b6["text"]) + 1)
        if mutex.acquire(1):
                flag2 = 1
                mutex.release()

def write_arduino_b7():
        global b7, mutex
        global flag3
        if int(b7["text"]) >= 3:
                b7["text"] = "0"
        else:
                b7["text"] = str(int(b7["text"]) + 1)
        if mutex.acquire(1):
                flag3 = 1
                mutex.release()

def write_arduino_b8():
        global b8, mutex
        global flag3
        if int(b8["text"]) >= 9:
                b8["text"] = "0"
        else:
                b8["text"] = str(int(b8["text"]) + 1)
        if mutex.acquire(1):
                flag3 = 1
                mutex.release()

def write_arduino_b9():
        global b9, mutex
        global flag3
        if int(b9["text"]) >= 9:
                b9["text"] = "0"
        else:
                b9["text"] = str(int(b9["text"]) + 1)
        if mutex.acquire(1):
                flag3 = 1
                mutex.release()

def write_arduino_b10():
        global b10, mutex
        global flag4
        if int(b10["text"]) >= 3:
                b10["text"] = "0"
        else:
                b10["text"] = str(int(b10["text"]) + 1)
        if mutex.acquire(1):
                flag4 = 1
                mutex.release()

def write_arduino_b11():
        global b11, mutex
        global flag4
        if int(b11["text"]) >= 9:
                b11["text"] = "0"
        else:
                b11["text"] = str(int(b11["text"]) + 1)
        if mutex.acquire(1):
                flag4 = 1
                mutex.release()

def write_arduino_b12():
        global b12, mutex
        global flag4
        if int(b12["text"]) >= 9:
                b12["text"] = "0"
        else:
                b12["text"] = str(int(b12["text"]) + 1)
        if mutex.acquire(1):
                flag4 = 1
                mutex.release()

def write_arduino_b13():
        global b13
        if b13["bg"] == bt_pressed:
                b13["bg"] = bt_bg
		GPIO.output(pin[4], GPIO.LOW)
        	time.sleep(0.1)
	else:
                b13["bg"] = bt_pressed
		GPIO.output(pin[4], GPIO.HIGH)
		time.sleep(0.1)
        #print(ser.readline())

def write_arduino_b14():
        global b14
        if b14["bg"] == bt_pressed:
                b14["bg"] = bt_bg
                GPIO.output(pin[5], GPIO.LOW)
		time.sleep(0.1)
        else:
                b14["bg"] = bt_pressed
                GPIO.output(pin[5], GPIO.HIGH)
		time.sleep(0.1)
        #print(ser.readline())

def write_arduino_b15():
        global b15
        if b15["bg"] == bt_pressed:
                b15["bg"] = bt_bg
                GPIO.output(pin[6], GPIO.LOW)
		time.sleep(0.1)
        else:
                b15["bg"] = bt_pressed
		GPIO.output(pin[6], GPIO.HIGH)
		time.sleep(0.1)
        #print(ser.readline())

def write_label_l1(label_str):
        global l1
	l1["text"] = label_str

def write_label_l2(label_str):
        global l2
        l2["text"] = label_str

def write_label_l3(label_str):
        global l3
        l3["text"] = label_str

def write_label_l4(label_str):
        global l4
        l4["text"] = label_str

def change_temp_1():
	global b1, b2, b3, temperature1, flag1, mutex
	if (flag1==1):
		file_handler = open(cfg_file, "r+")
		try:
			flist = file_handler.readlines()
			temperature1 = "%s%s%s"%(b1["text"], b2["text"], b3["text"])
			flist[0] = "%s\n"%(temperature1)
			file_handler.close()
			file_handler = open(cfg_file, "w+")
			file_handler.writelines(flist)
			if mutex.acquire(1):
                		flag1 = 1
                		mutex.release()
		finally:
        		file_handler.close()
	
def change_temp_2():
        global b4, b5, b6, temperature2, flag2, mutex
        if (flag2==1):
                file_handler = open(cfg_file, "r+")
                try:
                        flist = file_handler.readlines()
			temperature2 = "%s%s%s"%(b4["text"], b5["text"], b6["text"])
                        flist[1] = "%s\n"%(temperature2)
                        file_handler.close()
                        file_handler = open(cfg_file, "w+")
                        file_handler.writelines(flist)
			if mutex.acquire(1):
                		flag2 = 1
                		mutex.release()
                finally:
                        file_handler.close()

def change_temp_3():
        global b7, b8, b9, temperature3, flag3, mutex
        if (flag3==1):
                file_handler = open(cfg_file, "r+")
                try:
                        flist = file_handler.readlines()
			temperature3 = "%s%s%s"%(b7["text"], b8["text"], b9["text"])
                        flist[2] = "%s\n"%(temperature3)
                        file_handler.close()
                        file_handler = open(cfg_file, "w+")
                        file_handler.writelines(flist)
			if mutex.acquire(1):
                		flag3 = 1
                		mutex.release()
                finally:
                        file_handler.close()

def change_temp_4():
        global b10, b11, b12, temperature4, flag4, mutex
        if (flag4==1):
                file_handler = open(cfg_file, "r+")
                try:
                        flist = file_handler.readlines()
			temperature4 = "%s%s%s"%(b10["text"], b11["text"], b12["text"])
                        flist[3] = "%s\n"%(temperature4)
                        file_handler.close()
                        file_handler = open(cfg_file, "w+")
                        file_handler.writelines(flist)
			if mutex.acquire(1):
                		flag4 = 1
                		mutex.release()
                finally:
                        file_handler.close()	

def change_light():
	global light1, light2, light3, light4, l1, l2, l3, l4, temperature1, temperature2, temperature3, temperature4
	if (int(temperature1)>int(l1["text"])):
		light1["fg"] = light_red
		GPIO.output(pin[0], GPIO.HIGH)
		time.sleep(0.1)
	else:
		light1["fg"] = light_green
		GPIO.output(pin[0], GPIO.LOW)
		time.sleep(0.1)
	if (int(temperature2)>int(l2["text"])):
                light2["fg"] = light_red
		GPIO.output(pin[1], GPIO.HIGH)
		time.sleep(0.1)
        else:
                light2["fg"] = light_green
		GPIO.output(pin[1], GPIO.LOW)
		time.sleep(0.1)
	if (int(temperature3)>int(l3["text"])):
                light3["fg"] = light_red
		GPIO.output(pin[2], GPIO.HIGH)
		time.sleep(0.1)
        else:
                light3["fg"] = light_green
		GPIO.output(pin[2], GPIO.LOW)
		time.sleep(0.1)
	if (int(temperature4)>int(l4["text"])):
                light4["fg"] = light_red
		GPIO.output(pin[3], GPIO.HIGH)
		time.sleep(0.1)
        else:
                light4["fg"] = light_green
		GPIO.output(pin[3], GPIO.LOW)
		time.sleep(0.1)

def COMTrce():
	global l1, l2, l3, l4, b1, ser
	time.sleep(5)
	while True:
        	#if isOpened.isSet():
        	SerialTmp = ser.readline()
		if ((len(SerialTmp)>=5) and (SerialTmp[0]=='s') and (SerialTmp[-3]=='e')):
			ch1 = filter(lambda ch: ch in '0123456789', SerialTmp)
			if ((ch1[0:3].isdigit()) and (ch1[3:6].isdigit()) and (ch1[6:9].isdigit()) and (ch1[9:12].isdigit())):
				write_label_l1(ch1[0:3])
				write_label_l2(ch1[3:6])
				write_label_l3(ch1[6:9])
				write_label_l4(ch1[9:12])

		ser.flushInput()
		
		change_temp_1()
		change_temp_2()
		change_temp_3()
		change_temp_4()

		change_light()
		#print time.strftime('%H:%M:%S')
		time.sleep(3)

frame = Frame(root)
frame.pack()
Label(frame, height=35).grid(rowspan=9,columnspan=5)

button = Button(frame, text='重启', font=("黑体", 10, "bold"), command=UI_reboot, width=7, height=3, bg=bt_bg)
button.grid(row=10, column=0)
Label(frame, width=7).grid(row=10, column=1)
button1 = Button(frame, text='关机', font=("黑体", 10, "bold"), command=UI_shutdown, width=7, height=3, bg=bt_bg)
button1.grid(row=10, column=2)
Label(frame, width=7).grid(row=10, column=3)
button2 = Button(frame, text='进入系统', font=("黑体", 10, "bold"), command=UI_entry, width=7, height=3, bg=bt_bg)
button2.grid(row=10, column=4)

root.geometry('{}x{}+{}+{}'.format(w, h, 0, 0))
#root.attributes("-topmost", 1)
root.resizable(False, False)
root.title("Controller")
root.attributes("-fullscreen", 1)

root.mainloop()
