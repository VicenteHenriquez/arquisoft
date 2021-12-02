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
        s.send(sendbd.encode("utf-8"))
        datarec = s.recv(4096)
        datarec = datarec.decode("utf-8")
        print(datarec)
        resp = datarec[9:]
        resp = "00006"+ "adusr" + resp
        s.send(resp.encode("utf-8"))

    elif data1 == "2": #registro de usuario
        pass
    else:
        pass
