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
        data2 = data[6:]
        data2 = data2.split("---")
        usuario = data2[0]
        idcurso = data2[1]
        sql1 = "SELECT id FROM usuario WHERE correo = '" + usuario + "'"
        largo = 5 + 1 + len(sql1) + 3 + len(str(idcurso))
        texto = larstr(largo) + "conbd" + "8" + sql1 + "---" + str(idcurso)
        s.send(texto.encode("utf-8"))
        data = s.recv(4096)
        print(data.decode("utf-8"))
        data = data.decode("utf-8")[5:]
        data = data[7:]
        if data == "err":
            s.send(b'00008adevaerr')
        else:
            data = data.split("---")
            nombreramo = data[0]
            evaluaciones = data[1]
            evaluaciones = evaluaciones[14:]
            largo = 5 + len(str(nombreramo)) + 3 + len(str(evaluaciones))
            texto = larstr(largo) + "adeva" + nombreramo + "---" + evaluaciones
            print(texto)
            s.send(texto.encode("utf-8"))

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
        sql = "SELECT id FROM usuario WHERE correo = '" + usuario + "'"
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
            datos = datos.split("---")
            idusuario = datos[0]
            idcurso = datos[1]
            sentencia = "INSERT INTO evaluaciones (nombre, fecha, ponderacion, descripcion, nota, idramo, idusuario) VALUES ('" + nombrev + "', '" + fechaev + "', '" + pondev + "', '" + descev + "', '" + notaev + "', '" + idcurso + "', '" + idusuario + "')"
            largo = 5 + 2 + len(sentencia)
            texto = larstr(largo) + "conbd" + "a" + sentencia
            s.send(texto.encode("utf-8"))
            data = s.recv(4096)
            data = data.decode("utf-8")
            if data[12:] == "a":
                s.send(b'00008adevaa')
            else:
                s.send(b'00008adevae')
        pass
    elif data1 == "3": #elimina evaluacion
        pass
    else:
        pass