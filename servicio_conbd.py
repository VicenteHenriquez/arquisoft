import socket
import sqlite3 as sql
import sys
import time

conn = sql.connect('proyecto.db', check_same_thread=False)
cursor = conn.cursor()

def larstr(largo):
    ceros = 5-len(str(largo))
    if ceros == 4:
        largo="0000" + str(largo)
    elif ceros == 3:
        largo = "000" + str(largo)
    elif ceros == 2:
        largo = "00" + str(largo)
    elif ceros == 1:
        largo = "0" + str(largo)
    return (largo) 
 
PORT=5000
conex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conex.connect(('localhost', PORT))

conex.send(b'00012sinitOKconbd')
data = conex.recv(4096)
print(data.decode())

while True:
    data = conex.recv(4096)
    data = data.decode()
    print(data)
    
