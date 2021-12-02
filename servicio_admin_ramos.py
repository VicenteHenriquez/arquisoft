import socket
import sys
import time
from typing import TextIO

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

s.send(b'00010sinitadram')
data = s.recv(4096)
print(data.decode("utf-8"))

while True:
    data = s.recv(4096)
    print(data.decode("utf-8"))
    data = data.decode("utf-8")[5:]
    data1 = data[5:6]
    if data1 == "1": #vista de los ramos inscritos
        pass
    elif data1 == "2": #agregar un ramo
        datos = data[6:].split("---")
        usuario = datos[0]
        nomramo = datos[1]
        descurso = datos[2]
        profesor = datos[3]
        largo = 5 + 1 + len(usuario) + 3 + len(nomramo) + 3 + len(descurso) + 3 + len(profesor)
        texto = larstr(largo)+ "conbd" + "5" + usuario + "---" + nomramo + "---" + descurso + "---" + profesor
        s.send(texto.encode("utf-8"))
        datarec = s.recv(4096)
        data = datarec.decode("utf-8")
        print(data)
        resp = data[12:]
        resp = "00006" + "adram" + resp
        s.send(resp.encode("utf-8"))
    elif data1 == "3": #eliminar un ramo
        pass