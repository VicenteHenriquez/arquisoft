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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', PORT))

s.send(b'00010sinitconbd')
data = s.recv(4096)
print(data.decode("utf-8"))

while True:
    data = s.recv(4096)
    data = data.decode("utf-8")[5:]
    print(data)
    if data[5:6] == "1": #corrobora si existe el usuario
        sentencia = data[6:]
        cursor.execute(sentencia)
        resultado = cursor.fetchone()
        #resultado = len(resultado)
        if resultado == None:
            s.send(b'00006adusrf')
        elif resultado == 1:
            s.send(b'00006adusrv')
        else:
            pass
    else:
        pass
