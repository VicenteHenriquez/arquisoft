import socket
import sys
import time

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

s.send(b'00010sinitadusr')
data = s.recv(4096)
print(data.decode("utf-8"))

while True:
    data = s.recv(4096)
    print(data.decode("utf-8"))
    data = data.decode("utf-8")[5:]
    data1 = data[5:6]
    if data1 == "1": #inicio de sesion
        espacio = data.find(' ') #busca el espacio
        servicio = data[0:5] #define servicio
        usuario = data[6:espacio] #define usuario
        password = data[espacio+1:] #define password
        print(usuario, password)
        largousuario = len(usuario)
        largopassword = len(password)
        sql = "SELECT id FROM usuario WHERE correo = '"+ usuario +"' AND clave = '" + password + "'"
        largosen = 5+ 1 +len(sql)
        largosen = larstr(largosen)
        sendbd = largosen + "conbd" + "1" + sql 
        s.send(sendbd.encode("utf-8")) #enviamos a servicio_conbd.py
        datarec = s.recv(4096) #recibimos respuesta
        datarec = datarec.decode("utf-8")
        print(datarec)
        resp = datarec[12:] #00008conbdOK + v o f
        resp = "00006"+ "adusr" + resp #formulamos respuesta para menu.py
        s.send(resp.encode("utf-8")) #enviamos respuesta menu.py

    elif data1 == "2": #registro de usuario
        espacios = data.split(',')
        nombre = espacios[0]
        nombre = nombre[6:]
        correo = espacios[1]
        establecimiento = espacios[2]
        clave = espacios[3]
        sql1 = "SELECT id FROM usuario WHERE correo = '"+ correo +"'"
        sql = "INSERT INTO usuario (nombre, correo, establecimiento, clave) VALUES ('"+ nombre +"', '"+ correo +"', '"+ establecimiento +"', '"+ clave +"')" 
        largosen = 5+ 1 +len(sql) + 3 + len(sql1)
        largosen = larstr(largosen)
        sendbd = largosen + "conbd" + "2" + sql + "---" + sql1
        s.send(sendbd.encode("utf-8")) #enviamos a servicio_conbd.py
        datarec = s.recv(4096) #recibimos respuesta
        datarec = datarec.decode("utf-8")
        print(datarec)
        resp = datarec[12:] #00008conbdOK + r o e
        resp = "00006"+ "adusr" + resp #formulamos respuesta para menu.py
        s.send(resp.encode("utf-8")) #enviamos respuesta menu.py
    
    elif data1 == "3": #ver usuario
        usuario = data[6:]
        sql = "SELECT * FROM usuario WHERE correo = '"+ usuario +"'"
        largosen = 5+ 1 +len(sql)
        largosen = larstr(largosen)
        sendbd = largosen + "conbd" + "3" + sql
        s.send(sendbd.encode("utf-8")) #enviamos a servicio_conbd.py
        datarec = s.recv(4096) #recibimos respuesta
        datarec = datarec.decode("utf-8")[12:] #quitamos 00008conbdOK
        print(datarec)
        largo = 5 + len(datarec)
        enviar = larstr(largo) + "adusr" + datarec
        s.send(enviar.encode("utf-8")) #enviamos respuesta menu.py
    
    else:
        pass