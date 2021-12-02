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
    if data[5:6] == "1": #inicio de sesion, corrobora si existe el usuario
        sentencia = data[6:] #excluimos la sentencia
        print(sentencia)
        cursor.execute(sentencia) #ejecutamos la sentencia
        resultado = cursor.fetchone() #obtenemos el resultado
        if resultado == None: #no existe el usuario
            s.send(b'00006conbdf')
        elif len(resultado) == 1: #existe el usuario
            s.send(b'00006conbdv')
        else:
            pass
    elif data[5:6] == "2": #registro de usuario
        sentencia = data[6:].split("---")
        sentencia1 = sentencia[0] #excluimos la sentencia 1(insert)
        sentencia2 = sentencia[1] #excluimos la sentencia 2(select)
        print(sentencia)
        try:
            cursor.execute(sentencia2) #ejecutamos la sentencia 1 para saber si el correo ya esta en uso
            resultado = cursor.fetchone() #obtenemos el resultado
            if resultado == None: #no existe el correo
                cursor.execute(sentencia1)
                conn.commit()
                s.send(b'00006conbdr')
            else:
                s.send(b'00006conbde')
        except:
            conn.rollback()
            s.send(b'00006conbde')
        pass
