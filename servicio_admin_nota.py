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

s.send(b'00010sinitadnot')
data = s.recv(4096)
print(data.decode("utf-8"))

while True:
    data = s.recv(4096)
    print(data.decode("utf-8"))
    data = data.decode("utf-8")[5:]
    data1 = data[5:6]
    if data1 == "1":
        data = data[6:]
        data = data.split("---")
        usuario = data[0]
        idevaluacion = data[1]
        nnota = data[2]
        sql = "SELECT id FROM usuario WHERE correo = '" + usuario + "'"
        largo = 5 + 1 + len(sql)
        texto = larstr(largo) + "conbd" + "b" + sql
        print(texto)
        s.send(texto.encode("utf-8"))
        data = s.recv(4096)
        data = data.decode("utf-8")
        datos = data[12:]
        if datos == "err":
            s.send(b'00008adnoterr')
        else:
            idusuario = datos
        sql1 = "SELECT id FROM evaluaciones WHERE id = '" + idevaluacion + "' AND idusuario = '" + idusuario + "'"
        print(sql1)
        largo = 5 + 1 + len(sql1) + 3 + len(str(nnota))
        texto = larstr(largo) + "conbd" + "c" + sql1 + "---" + str(nnota)
        s.send(texto.encode("utf-8"))
        data = s.recv(4096)
        data = data.decode("utf-8")
        datos = data[12:]
        print(datos)
        if datos == "ne":
            s.send(b'00007adnotne')
        elif datos == "a":
            s.send(b'00006adnota')
        elif datos == "e":
            s.send(b'00006adnote')
        else:
            s.send(b'00008adnoterr')
    