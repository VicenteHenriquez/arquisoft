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

s.send(b'00010sinitadeva')
data = s.recv(4096)
print(data.decode("utf-8"))

while True:
    data = s.recv(4096)
    print(data.decode("utf-8"))
    data = data.decode("utf-8")[5:]
    data1 = data[5:6]
    if data1 == "1": #consulta evaluaciones
        pass
    elif data1 == "2": #ingresa evaluacion
        data = data[6:]
        data = data.split("---")
        usuario = data[0]
        nombrev = data[1]
        fechaev = data[2]
        pondev = data[3]
        descev = data[4]
        notaev = data[5]
        ramo = data[6]
        sql = "SELECT id FROM usuarios WHERE usuario = '" + usuario + "'"
        sql1 = "SELECT id FROM ramos WHERE nombre = '" + ramo + "'"
        largo = 5 + 1 + len(sql) + 3 + len(sql1)
        texto = larstr(largo) + "conbd" + "9" + sql + "---" + sql1
        s.send(texto.encode("utf-8"))
        data = s.recv(4096)
        data = data.decode("utf-8")
        datos = data[12:]
        if datos == "err":
            print(datos)
            s.send(b'00008adevaerr')
        else:

            idusuario = datos[0]
            idramo = datos[1]

        pass
    elif data1 == "3": #elimina evaluacion
        pass
    else:
        pass