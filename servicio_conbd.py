import socket
import sqlite3 as sql
from sqlite3.dbapi2 import Error
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
        print(sentencia1)
        print(sentencia2)
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
    
    elif data[5:6] == "3": #consulta de usuario
        sentencia = data[6:] #excluimos la sentencia
        print(sentencia)
        cursor.execute(sentencia) #ejecutamos la sentencia
        resultado = cursor.fetchone() #obtenemos el resultado
        nombre = resultado[1]
        correo = resultado[2]
        establecimiento = resultado[3]
        clave = resultado[4]
        largo = 5 + len(nombre) + 3 + len(correo) + 3 + len(establecimiento) + 3 +len(clave)
        enviar = larstr(largo) + "conbd" + nombre + "---" + correo + "---" + establecimiento + "---" + clave
        print(enviar)
        s.send(enviar.encode("utf-8"))
    
    elif data[5:6] == "4": #consulta de ramos
        sentencia = data[6:] #excluimos la sentencia
        print(sentencia)
        cursor.execute(sentencia) #ejecutamos la sentencia
        idusuario = cursor.fetchone()[0]
        sentencia = "SELECT cursos.id , ramos.nombre FROM cursos,ramos WHERE cursos.idramo = ramos.id AND idusuario = " + str(idusuario) + "" 
        print(sentencia)
        cursor.execute(sentencia) #ejecutamos la sentencia
        resultado = cursor.fetchall() #obtenemos los resultados
        print(resultado)
        largo = 5 + len(resultado)
        enviar = larstr(largo) + "conbd" + str(resultado)
        s.send(enviar.encode("utf-8"))
    
    elif data[5:6] == "5": #agregar ramo
        datos = data[6:].split("---")
        print(datos)
        usuario = datos[0]
        nombreram = datos[1]
        descurso = datos[2]
        profesor = datos[3]
        sentencia = "SELECT id FROM usuario WHERE correo = '" + usuario + "'"
        cursor.execute(sentencia)
        idusuario = cursor.fetchone()
        idusuario = int(idusuario[0])
        print(idusuario)
        sentencia2 = "SELECT id FROM ramos WHERE nombre = '" + nombreram + "'"
        print(sentencia2)
        cursor.execute(sentencia2)
        ramo = cursor.fetchone()
        if ramo == None: #no existe el ramo
            try:
                sentencia3 = "INSERT INTO ramos (nombre) VALUES ('" + nombreram + "')"
                print(sentencia3)
                cursor.execute(sentencia3)
                conn.commit()
            except:
                conn.rollback()
                s.send(b'00006conbde')
            cursor = conn.cursor()
            sentencia4 = "SELECT id FROM ramos WHERE nombre = '" + nombreram + "'"
            print(sentencia4)
            cursor.execute(sentencia4)
            idramo = cursor.fetchone()
            idramo = int(idramo[0])
            try: #insertamos el curso
                sentencia5 = "INSERT INTO cursos (idusuario, idramo, descripcion, profesor) VALUES ("+ str(idusuario) + ", "+ str(idramo) + ", '" + descurso + "', '" + profesor + "')"
                print(sentencia5)
                cursor.execute(sentencia5)
                conn.commit()
                s.send(b'00006conbda')
            except: #hubo un error
                conn.rollback()
                s.send(b'00006conbde')
        else: #existe el ramo
            idramo = int(ramo[0])
            print(idramo)
            sentcursos = "SELECT id FROM cursos WHERE idusuario = " + str(idusuario) + " AND idramo = " + str(idramo) + ""
            cursor.execute(sentcursos)
            curso = cursor.fetchone()
            if curso == None: #no existe el curso con ese alumno
                try: #insertamos el curso , falta que el curso ya esta inscrito
                    sentencia5 = "INSERT INTO cursos (idusuario, idramo, descripcion, profesor) VALUES (" + str(idusuario) + ", " + str(idramo) + ", '" + descurso + "', '" + profesor + "')"
                    print(sentencia5)
                    cursor.execute(sentencia5)
                    conn.commit()
                    s.send(b'00006conbda')
                except Error: #error
                    print("Error:", Error)
                    conn.rollback()
                    s.send(b'00006conbde')
            else: #ya existe el curso
                s.send(b'00006conbdy')
    
    elif data[5:6] == "6": #consulta ramo en particular
        data = data[6:].split("---")
        sentencia = data[0]
        idramo = data[1]
        cursor.execute(sentencia)
        idusuario = cursor.fetchone()[0]
        sentencia1 = "SELECT ramos.nombre, descripcion, profesor FROM cursos,ramos WHERE idusuario ='"+ str(idusuario) +"' AND cursos.idramo = ramos.id and ramos.id = '"+ str(idramo) +"'"
        cursor.execute(sentencia1)
        resultado = cursor.fetchone()
        if resultado == None:
            s.send(b'00006conbde')
        else:
            nombre = resultado[0]
            descripcion = resultado[1]
            profesor = resultado[2]
            largo = 5 + len(nombre) + 3 + len(descripcion) + 3 + len(profesor)
            enviar = larstr(largo) + "conbd" + nombre + "---" + descripcion + "---" + profesor
            s.send(enviar.encode("utf-8"))
