from threading import Thread
from tkinter import *
import socket
import time
import struct
import sys

##interface del maestro

root = Tk()
root.geometry("1000x400")
root.title("server")

## Etiquetas para mostrar los relojes
clock0 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock0.grid(row = 0, column = 0, pady = 25, padx = 25)

clock1 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock1.grid(row = 0, column = 1, pady = 25, padx = 25)

clock2 = Label(root, text = "hh:mm:ss", font = ("Arial", 50, "bold"))
clock2.grid(row = 0, column = 2, pady = 25, padx = 25)

##Guarda la hora de cada reloj como lista de enteros H, M, S
current_times = [[22,12,1], [11,11,11], [5,5,5]]
##Guarda el delay para actualizar cada reloj (milisegundos)
delays = [1000, 1000, 1000]
##Guarda la hora de cada reloj como cadena (para poner en la Label de cada reloj)
strtimes = ["22:12:1","11:11:11","5:5:5"]

#actualiza los valores de cada reloj
def update_clock(i):
	global current_times
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

#cambia el texto del reloj 0 de acuerdo al delay
def time0():
	global delays
	global strtimes
	update_clock(0)
	clock0.config(text = strtimes[0], bg = "black", fg = "green", font = "Arial 50 bold")
	clock0.after(delays[0], time0)

#cambia el texto del reloj 1 de acuerdo al delay
def time1():
	global delays
	global strtimes
	update_clock(1)
	clock1.config(text = strtimes[1], bg = "black", fg = "green", font = "Arial 50 bold")
	clock1.after(delays[1], time1)

#cambia el texto del reloj 2 de acuerdo al delay
def time2():
	global delays
	global strtimes
	update_clock(2)
	clock2.config(text = strtimes[2], bg = "black", fg = "green", font = "Arial 50 bold")
	clock2.after(delays[2], time2)

##Se debe llamar a las funciones que actualizan los relojes 
time0()
time1()
time2()


class Client(Thread):
	def __init__(self, addr):
		Thread.__init__(self)
		self.addr = addr
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.conn.settimeout(2)
		ttl = struct.pack('b', 1)
		self.conn.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	
	def enviar_datos(self,dato):
		print('sending {!r}'.format(dato))
		sent = self.conn.sendto(dato, self.addr)

	def run(self):
		pass

# Conectarse con los 3 clientes

c0 = Client(('224.3.29.71', 10001))
c0.start()

c1 = Client(('224.3.29.71', 10002))
c1.start()

c2 = Client(('224.3.29.71', 10003))
c2.start()

def formatToSend(hour):
	res = ""
	h, m, s, d = hour.split(":")
	if h[0] == "0":
		h = h[1:]
	if m[0] == "0":
		m = m[1:]
	if s[0] == "0":
		s = s[1:]
	res += h + ":" + m + ":" + s + ":" + d
	return res

#Obtiene la hora como cadena (H:M:S) para el reloj 0
def getHour0():
	h, m, s = str_hour0.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[0] = [h,m,s]

#Esto debe enviar la hora y el delay del reloj 0 por el socket con hilos y udp
def sendHour0():
	c0.enviar_datos(str.encode(formatToSend(strtimes[0] +":"+ str(delays[0]))))

#Obtiene el delay para actualizar el reloj 0 en milisegundos
def getDelay0():
	delays[0] = int(str_delay0.get())

##Componentes graficos del reloj 0
lblNew0 = Label(root, text = "New hour for clock 1 (H:M:S)", pady = 10)
lblNew0.grid(row = 1, column = 0)
str_hour0 = StringVar()
entry_hour0 = Entry(root, textvariable = str_hour0)
entry_hour0.grid(row = 2, column = 0)
btnChange0 = Button(root, text = "Change hour", command = lambda: getHour0())
btnChange0.grid(row = 3, column = 0)

lblDelay0 = Label(root, text = "New delay for clock 1 (milliseconds)", pady = 10)
lblDelay0.grid(row = 4, column = 0)
str_delay0 = StringVar()
entry_delay0 = Entry(root, textvariable = str_delay0)
entry_delay0.grid(row = 5, column = 0)
btnDelay0 = Button(root, text = "Change delay", command = lambda: getDelay0())
btnDelay0.grid(row = 6, column = 0)

lblSend0 = Label(root, text = "Send hour for clock 1", pady = 10)
lblSend0.grid(row = 7, column = 0)
btnSend0 = Button(root, text = "Send", command = lambda: sendHour0())
btnSend0.grid(row = 8, column = 0)

#Obtiene la hora como cadena (H:M:S) para el reloj 1
def getHour1():
	h, m, s = str_hour1.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[1] = [h,m,s]

#Esto debe enviar la hora y el delay del reloj 1 por el socket con hilos y udp
def sendHour1():
	c1.enviar_datos(str.encode(formatToSend(strtimes[1] + ":"+str(delays[1]))))


#Obtiene el delay para actualizar el reloj 1 en milisegundos
def getDelay1():
	delays[1] = int(str_delay1.get())

##Componentes graficos del reloj 1
lblNew1 = Label(root, text = "New hour for clock 2 (H:M:S)")
lblNew1.grid(row = 1, column = 1)
str_hour1 = StringVar()
entry_hour1 = Entry(root, textvariable = str_hour1)
entry_hour1.grid(row = 2, column = 1)
btnChange1 = Button(root, text = "Change hour", command = lambda: getHour1())
btnChange1.grid(row = 3, column = 1)

lblDelay1 = Label(root, text = "New delay for clock 2 (milliseconds)")
lblDelay1.grid(row = 4, column = 1)
str_delay1 = StringVar()
entry_delay1 = Entry(root, textvariable = str_delay1)
entry_delay1.grid(row = 5, column = 1)
btnDelay1 = Button(root, text = "Change delay", command = lambda: getDelay1())
btnDelay1.grid(row = 6, column = 1)

lblSend1 = Label(root, text = "Send hour for clock 2")
lblSend1.grid(row = 7, column = 1)
btnSend1 = Button(root, text = "Send", command = lambda: sendHour1())
btnSend1.grid(row = 8, column = 1)

#Obtiene la hora como cadena (H:M:S) para el reloj 2
def getHour2():
	h, m, s = str_hour2.get().split(":")
	h = int(h)
	m = int(m)
	s = int(s)
	current_times[2] = [h,m,s]

#Esto debe enviar la hora y el delay del reloj 2 por el socket con hilos y udp
def sendHour2():
	c2.enviar_datos(str.encode(formatToSend(strtimes[2] + ":"+str(delays[2]))))
#Obtiene el delay para actualizar el reloj 2 en milisegundos
def getDelay2():
	delays[2] = int(str_delay2.get())

##Componentes graficos del reloj 2
lblNew2 = Label(root, text = "New hour for clock 3 (H:M:S)")
lblNew2.grid(row = 1, column = 2)
str_hour2 = StringVar()
entry_hour2 = Entry(root, textvariable = str_hour2)
entry_hour2.grid(row = 2, column = 2)
btnChange2 = Button(root, text = "Change hour", command = lambda: getHour2())
btnChange2.grid(row = 3, column = 2)

lblDelay2 = Label(root, text = "New delay for clock 3 (milliseconds)")
lblDelay2.grid(row = 4, column = 2)
str_delay2 = StringVar()
entry_delay2 = Entry(root, textvariable = str_delay2)
entry_delay2.grid(row = 5, column = 2)
btnDelay2 = Button(root, text = "Change delay", command = lambda: getDelay2())
btnDelay2.grid(row = 6, column = 2)

lblSend2 = Label(root, text = "Send hour for clock 3")
lblSend2.grid(row = 7, column = 2)
btnSend2 = Button(root, text = "Send", command = lambda: sendHour2())
btnSend2.grid(row = 8, column = 2)

root.mainloop()