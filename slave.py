from tkinter import *
import socket
import time
import struct
import sys
import threading

num_reloj = int(sys.argv[1])

root = Tk()
root.geometry("350x150")
root.title("client")

## Etiquetas para mostrar los relojes
clock = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock.grid(row = 0, column = 0, pady = 25, padx = 25)
current_time = [11,11,11]
delay = 1000
strtime = "11:11:11"

def update_clock():
    global current_time
    global strtime
    current_time[2] += 1
    if current_time[2] > 59:
        current_time[2] = 0
        current_time[1] += 1
        if current_time[1] > 59:
            current_time[1] = 0
            current_time[0] += 1
            if current_time[0] > 23:
                current_time[0] = 0
    strh = str(current_time[0]) if current_time[0] > 9 else "0" + str(current_time[0])
    strm = str(current_time[1]) if current_time[1] > 9 else "0" + str(current_time[1])
    strs = str(current_time[2]) if current_time[2] > 9 else "0" + str(current_time[2])
    strtime = strh + ":" + strm + ":" + strs

def time():
    global delay
    update_clock()
    clock.config(text = strtime, bg = "black", fg = "green", font = "Arial 50 bold")
    clock.after(delay, time)

time()

multicast_group = '224.3.29.71'
server_address = ('', 10000 + num_reloj)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

def change_hour(data):
	global current_time
	global delay
	h, m, s, d = data.split(":")
	print(data.split())
	h = int(h)
	m = int(m)
	s = int(s)
	d = int(d)
	current_time[0] = h
	current_time[1] = m
	current_time[2] = s
	delay = d
	print("updated")

def listen():
	while True:
	    print('\nwaiting to receive new hour')
	    data, address = sock.recvfrom(1024)

	    print('received {} bytes from {}'.format(
	        len(data), address))
	    print(type(data))
	    change_hour(data.decode("utf-8"))
listening = threading.Thread(target = listen)
listening.start()
root.mainloop()