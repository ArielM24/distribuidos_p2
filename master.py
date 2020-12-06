import threading
from tkinter import *
import socket
import time

root = Tk()
root.geometry("1150x600")
root.title("master")

clock0 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock0.grid(row = 0, column = 0, pady = 25, padx = 25)

clock1 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock1.grid(row = 0, column = 1, pady = 25, padx = 25)

clock2 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock2.grid(row = 0, column = 2, pady = 25, padx = 25)

current_times = [[22,12,1], [11,11,11], [5,5,5]]
delays = [1000, 1000, 1000]
strtimes = ["22:12:1","11:11:11","5:5:5"]

def update_clock(i):
	global current_times

	#print(h, m, s)
	current_times[i][2] += 1
	if current_times[i][2] > 59:
		current_times[i][2] = 0
		current_times[i][1] += 1
		if current_times[i][1] > 59:
			current_times[i][1] = 0
			current_times[i][0] += 1
			if current_times[i][0] > 24:
				current_times[i][0] = 0

	strh = str(current_times[i][0]) if current_times[i][0] > 9 else "0" + str(current_times[i][0])
	strm = str(current_times[i][1]) if current_times[i][1] > 9 else "0" + str(current_times[i][1])
	strs = str(current_times[i][2]) if current_times[i][2] > 9 else "0" + str(current_times[i][2])
	strtimes[i] = strh + ":" + strm + ":" + strs

def time0():
	global delays
	global strtimes
	update_clock(0)
	clock0.config(text = strtimes[0], bg = "black", fg = "green", font = "Arial 50 bold")
	clock0.after(delays[0], time0)

def time1():
	global delays
	global strtimes
	update_clock(1)
	clock1.config(text = strtimes[1], bg = "black", fg = "green", font = "Arial 50 bold")
	clock1.after(delays[1], time1)

def time2():
	global delays
	global strtimes
	update_clock(2)
	clock2.config(text = strtimes[2], bg = "black", fg = "green", font = "Arial 50 bold")
	clock2.after(delays[2], time2)

time0()
time1()
time2()

def getHour0():
	h, m, s = str_hour0.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[0] = [h,m,s]


lbl0 = Label(root, text = "New hour for 0")
lbl0.grid(row = 1, column = 0)
str_hour0 = StringVar()
entry_hour0 = Entry(root, textvariable = str_hour0)
entry_hour0.grid(row = 2, column = 0)
btnChange0 = Button(root, text = "Change 0", command = lambda: getHour0())
btnChange0.grid(row = 3, column = 0)

def getHour1():
	h, m, s = str_hour1.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[1] = [h,m,s]

lbl1 = Label(root, text = "New hour for 1")
lbl1.grid(row = 1, column = 1)
str_hour1 = StringVar()
entry_hour1 = Entry(root, textvariable = str_hour1)
entry_hour1.grid(row = 2, column = 1)
btnChange1 = Button(root, text = "Change 1", command = lambda: getHour1())
btnChange1.grid(row = 3, column = 1)

def getHour2():
	h, m, s = str_hour2.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[2] = [h,m,s]

lbl2 = Label(root, text = "New hour for 2")
lbl2.grid(row = 1, column = 2)
str_hour2 = StringVar()
entry_hour2 = Entry(root, textvariable = str_hour2)
entry_hour2.grid(row = 2, column = 2)
btnChange2 = Button(root, text = "Change 2", command = lambda: getHour2())
btnChange2.grid(row = 3, column = 2)

root.mainloop()