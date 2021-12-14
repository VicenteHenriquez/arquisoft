# -*- coding: utf-8 -*-
import socket
import sys
#create a socket client

host = 'localhost'
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))



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

def menu_4_options():
    while True:
        print("----------------------------------------------------------")
        print("""
        1. Iniciar sesion
        2. Registrar
        3. Salir
        """)
        print("----------------------------------------------------------")
        choice = input("Elija la opción correspondiente: ")
        if choice == "1":#iniciar sesion
            print("----------------------------------------------------------")
            print("Iniciar sesion")
            correo = input("Correo: ")
            password = input("Password: ")
            print("----------------------------------------------------------")
            largo = 5 + 1 +len(correo) + 1 + len(password)
            texto = larstr(largo) + "adusr" + "1" + correo + " " + password
            s.send(texto.encode("utf-8"))
            resp = s.recv(4096)
            print(resp.decode("utf-8"))
            respuesta = resp.decode("utf-8")
            respuesta = respuesta[12:]
            if respuesta == "v":
                user = correo
                menu_sesionini(user)
            elif respuesta == "f":
                print("Correo o contraseña incorrecta")
            else:
                print("Error")
        elif choice == "2": #registrar
            print("Ingrese su nombre y apellido: ")
            nombre = str(input())
            print("Ingrese su correo: ")
            correo = str(input())
            print("Ingrese su establecimiento: ")
            establecimiento = str(input())
            print("Ingrese su password(sin espacios): ")
            password1 = str(input())
            print("Ingrese su password nuevamente: ")
            password2 = str(input())
            if password1 == password2:
                largo = 5 + 1 + len(nombre) + 1 + len(correo) + 1 + len(establecimiento) + 1 + len(password1)
                texto = larstr(largo) + "adusr" + "2" + nombre + "," + correo + "," + establecimiento + "," + password1
                s.send(texto.encode("utf-8"))
                resp = s.recv(4096)
                print(resp.decode("utf-8"))
                respuesta = resp.decode()[12]
                print(respuesta)
                if respuesta == "r":
                    print("Registro exitoso")
                elif respuesta == "e":
                    print("Correo ya registrado o error al registrar")
                else:
                    print("Error")
            else:
                print("Las contraseñas no coinciden")
        elif choice == "3":
            print("Saliendo...Muchas gracias por utilizar nuestros servicios")
            sys.exit()
        else:
            print("Opción incorrecta")

def menu_sesionini(user):
    print("----------------------------------------------------------")
    print("""
    Bienvenido
    1. Ver perfil
    2. Cursos
    3. Evaluaciones
    4. Salir
    """)
    print("----------------------------------------------------------")
    choice = input("Elija la opción correspondiente: ")
    if choice == "1":
        usuario = user
        largo = 5 + 1 + len(usuario)
        texto = larstr(largo) + "adusr" + "3" + usuario
        s.send(texto.encode("utf-8"))
        resp = s.recv(4096)
        print(resp.decode("utf-8"))
        respuesta = resp.decode("utf-8")
        respuesta = respuesta[12:]
        respuesta = respuesta.split("---")
        print("----------------------------------------------------------")
        print("Nombre: " + respuesta[0])
        print("Correo: " + respuesta[1])
        print("Establecimiento: " + respuesta[2])
        print("Clave: " + respuesta[3])
        print("----------------------------------------------------------")
        return menu_sesionini(user)
    elif choice == "2":
        menu_ramos(user)
    elif choice == "3":
        menu_evaluaciones(user)
    elif choice == "4":
        print("Cerrando sesion...")
        return menu_4_options()
    else:
        print("Opción incorrecta")
        return menu_sesionini(user)

def menu_ramos(user):
    print("----------------------------------------------------------")
    print("""
    1. Ver cursos
    2. Agregar curso
    3. Eliminar curso
    4. Volver
    """)
    print("----------------------------------------------------------")
    choice = input("Elija la opción correspondiente: ")
    if choice == "1": #ver cursos
        usuario = user
        largo = 5 + 1 + len(usuario)
        texto = larstr(largo) + "adram" + "1" + usuario
        s.send(texto.encode("utf-8"))
        resp = s.recv(4096)
        respuesta = resp.decode("utf-8")
        respuesta = respuesta[12:]
        respuesta = respuesta.split("), (")
        largresp = len(respuesta)
        print("----------------------------------------------------------")
        for i in range(len(respuesta)):
            if i == largresp-1:
                print(respuesta[i].strip(")]"))
            else:
                print(respuesta[i])
        print("----------------------------------------------------------")
        print("Escriba el numero del ramo que desea ver(0 si desea salir): ")
        idramo = input()
        if idramo.isnumeric() == False:
            print("Ramo no encontrado")
            return menu_ramos(user)
        else:
            largo = 5 + 1 + len(usuario) + 1 + len(idramo)
            texto = larstr(largo) + "adram" + "4" + usuario + "," + idramo
            s.send(texto.encode("utf-8"))
            resp = s.recv(4096)
            respuesta = resp.decode("utf-8")
            respuesta = respuesta[12:]
            if respuesta == "e":
                print("Curso no encontrado")
            else:
                respuesta = respuesta.split("---")
                print(respuesta)
                print("----------------------------------------------------------")
                print("Nombre: " + respuesta[0])
                print("Descripción: " + respuesta[1])
                print("Profesor: " + respuesta[2])
                print("----------------------------------------------------------")
                return menu_ramos(user)

    elif choice == "2": #agregar curso
        print("----------------------------------------------------------")
        print("INGRESE LOS DATOS DEL CURSO")
        print("Nombre: ")
        nombre = str(input())
        print("Descripción: ")
        descripcion = str(input())
        print("Profesor: ")
        profesor = str(input())
        print("----------------------------------------------------------")
        usuario = user
        largo = 5 + 1 + len(usuario) + 3 + len(nombre) + 3 + len(descripcion) + 3 + len(profesor)
        texto = larstr(largo) + "adram" + "2" + usuario + "---" + nombre + "---" + descripcion + "---" + profesor
        s.send(texto.encode("utf-8"))
        resp = s.recv(4096)
        respuesta = resp.decode("utf-8")
        print(respuesta)
        respuesta = respuesta[12:]
        if respuesta == "a":
            print("Ramo agregado")
            return menu_ramos(user)
        elif respuesta == "e":
            print("Error al agregar ramo")
            return menu_ramos(user)
        elif respuesta == "y":
            print("Ramo ya existente")
            return menu_ramos(user)
        else:
            print("Error")
            return menu_ramos(user)
    
    elif choice == "3": #eliminar curso
        print("Sus cursos son:")
        ver_cursos(user)
        print("Escriba el numero del curso que desea eliminar(0 si desea salir): ")
        idcurso = input()
        if idcurso.isnumeric() == False:
            print("Error")
            return menu_ramos(user)
        elif idcurso == "0":
            return menu_ramos(user)
        else:
            largo = 5 + 1 + len(user) + 3 + len(idcurso)
            texto = larstr(largo) + "adram" + "3" + user + "---" + idcurso
            print(texto)
            s.send(texto.encode("utf-8"))
            resp = s.recv(4096)
            respuesta2 = resp.decode("utf-8")
            respuesta2 = respuesta2[12:]
            print(respuesta2)
            if respuesta2 == "err":
                print("Error")
                return menu_ramos(user)
            elif respuesta2 == "a":
                print("Curso eliminado")
                return menu_ramos(user)
            else:
                print("Error al eliminar curso")
                return menu_ramos(user)

    elif choice == "4": #volver
        menu_sesionini(user)
    
    else:
        pass
    return menu_ramos(user)

def menu_evaluaciones(user):
    print("----------------------------------------------------------")
    print("""
    1. Ver evaluaciones
    2. Agregar evaluación
    3. Eliminar evaluación
    4. Volver
    """)
    print("----------------------------------------------------------")
    choice = input("Elija la opción correspondiente: ")
    if choice == "1": #ver evaluaciones y editar nota
        ver_cursos(user)
        print("Ingrese el id del curso que desea ver evaluaciones(0 si desea volver): ")
        idcurso = input()
        if idcurso.isnumeric() == False:
            print("Error")
            return menu_evaluaciones(user)
        else:
            if idcurso == "0":
                return menu_evaluaciones(user)
            else:
                largo = 5 + 1 + len(user) + 3 + len(idcurso)
                texto = larstr(largo) + "adeva" + "1" + user + "---" + idcurso
                s.send(texto.encode("utf-8"))
                resp = s.recv(4096)
                respuesta = resp.decode("utf-8")
                respuesta = respuesta[12:]
                if respuesta == "err":
                    print("Error")
                    return menu_evaluaciones(user)
                else:
                    respuesta = respuesta.split("---")
                    nombrecurso = respuesta[0]
                    evaluaciones = respuesta[1]
                    evaluaciones = evaluaciones.split("), (")
                    largoev = len(evaluaciones)
                    print("----------------------------------------------------------")
                    print("Evaluaciones del curso " + nombrecurso)
                    print("Orden: ID, Nombre, Fecha, Ponderación, Descripción, Nota")
                    for i in range(len(evaluaciones)):
                        if i == largoev-1:
                            print(evaluaciones[i].strip(")]"))
                        else:

                            print(evaluaciones[i])
                    print("----------------------------------------------------------")
                    print("Escriba el numero id de la evaluación que desea editar su nota (0 si desea salir): ")
                    idevaluacion = input()
                    if idevaluacion.isnumeric() == False:
                        print("Error")
                        return menu_evaluaciones(user)
                    elif idevaluacion == "0":
                        return menu_evaluaciones(user)
                    else:
                        print("Ingrese la nueva nota(0 - 70): ")
                        nota = input()
                        if nota.isnumeric() == False:
                            print("Error")
                            return menu_evaluaciones(user)
                        elif int(nota) >= 0 and int(nota) <= 70:
                            largo = 5 + 1 + len(user) + 3 + len(str(idevaluacion)) + 3 + len(str(nota))
                            texto = larstr(largo) + "adnot" + "1" + user + "---" + str(idevaluacion) + "---" + str(nota)
                            s.send(texto.encode("utf-8"))
                            resp = s.recv(4096)
                            respuesta = resp.decode("utf-8")
                            respuesta = respuesta[12:]
                            if respuesta == "ne":
                                print("Evaluación no encontrada")
                                return menu_evaluaciones(user)
                            elif respuesta == "a":
                                print("Nota actualizada")
                                return menu_evaluaciones(user)
                            elif respuesta == "e":
                                print("Error al actualizar nota")
                                return menu_evaluaciones(user)
                            else:
                                print("Error")
                                return menu_evaluaciones(user)
                    return menu_evaluaciones(user)

    elif choice == "2": #agregar evaluacion
        ver_cursos(user)
        print("----------------------------------------------------------")
        print("INGRESE LOS DATOS DE LA  NUEVA EVALUACIÓN: ")
        ramo = str(input("Curso: "))
        nombre = str(input("Nombre: "))
        fecha = str(input("Fecha(dd/mm/aaaa): "))
        ponderacion = str(input("Ponderación(0-100): "))
        if not ponderacion:
            ponderacion = "0"
        descripcion = str(input("Descripción: "))
        if not descripcion:
            descripcion = "none"
        nota = str(input("Nota(0 a 70): "))
        if not nota:
            nota = "0"
        print("----------------------------------------------------------")
        usuario = user
        largo = 5 + 1 + len(usuario) + 3 + len(nombre) + 3 + len(fecha) + 3 + len(ponderacion) + 3 + len(descripcion) + 3 + len(nota) + 3 + len(ramo)
        texto = larstr(largo) + "adeva" + "2" + usuario + "---" + nombre + "---" + fecha + "---" + ponderacion + "---" + descripcion + "---" + nota + "---" + ramo
        s.send(texto.encode("utf-8"))
        resp = s.recv(4096)
        respuesta = resp.decode("utf-8")
        print(respuesta)
        if respuesta[12:] == "err":
            print("Curso no encontrado")
            return menu_evaluaciones(user)
        elif respuesta[12:] == "a":
            print("Evaluación agregada")
            return menu_evaluaciones(user)
        else:
            print("Error al agregar evaluación")
            return menu_evaluaciones(user)
    
    elif choice == "3": #eliminar evaluacion
        ver_cursos(user)
        print("Ingrese el id del curso que desea ver evaluaciones(0 si desea volver): ")
        ver_evaluaciones(user)
        print("Ingrese el id de la evaluación que desea eliminar(0 si desea volver): ")
        idevaluacion = input()
        if idevaluacion.isnumeric() == False:
            print("Error")
            return menu_evaluaciones(user)
        elif idevaluacion == "0":
            return menu_evaluaciones(user)
        else:
            largo = 5 + 1 + len(user) + 3 + len(str(idevaluacion))
            texto = larstr(largo) + "adeva" + "3" + user + "---" + str(idevaluacion)
            s.send(texto.encode("utf-8"))
            data = s.recv(4096)
            respuesta = data.decode("utf-8")
            respuesta = respuesta[12:]
            if respuesta == "err":
                print("Error")
                return menu_evaluaciones(user)
            elif respuesta == "a":
                print("Evaluación eliminada")
                return menu_evaluaciones(user)
            else:
                print("Error al eliminar evaluación")
                return menu_evaluaciones(user)
    
    elif choice == "4": #volver
        menu_sesionini(user)
    
    else:
        print("Opción incorrecta")
        return menu_evaluaciones(user)

def ver_cursos(user): #funcion para ver cursos
    largo = 5 + 1 + len(user)
    texto = larstr(largo) + "adram" + "1" + user
    s.send(texto.encode("utf-8"))
    resp = s.recv(4096)
    respuesta = resp.decode("utf-8")
    respuesta = respuesta[12:]
    respuesta = respuesta.split("), (")
    largresp = len(respuesta)
    print("----------------------------------------------------------")
    for i in range(len(respuesta)):
        if i == largresp-1:
            print(respuesta[i].strip(")]"))
        else:
            print(respuesta[i])
    print("----------------------------------------------------------")

def ver_evaluaciones(user): #funcion para ver evaluaciones
    idcurso = input()
    if idcurso.isnumeric() == False:
        print("Error")
        return menu_evaluaciones(user)
    else:
        if idcurso == "0":
            return menu_evaluaciones(user)
        else:
            largo = 5 + 1 + len(user) + 3 + len(idcurso)
            texto = larstr(largo) + "adeva" + "1" + user + "---" + idcurso
            s.send(texto.encode("utf-8"))
            resp = s.recv(4096)
            respuesta = resp.decode("utf-8")
            respuesta = respuesta[12:]
            if respuesta == "err":
                print("Error")
                return menu_evaluaciones(user)
            else:
                respuesta = respuesta.split("---")
                nombrecurso = respuesta[0]
                evaluaciones = respuesta[1]
                evaluaciones = evaluaciones.split("), (")
                largoev = len(evaluaciones)
                print("----------------------------------------------------------")
                print("Evaluaciones del curso " + nombrecurso)
                print("Orden: ID, Nombre, Fecha, Ponderación, Descripción, Nota")
                for i in range(len(evaluaciones)):
                    if i == largoev-1:
                        print(evaluaciones[i].strip(")]"))
                    else:
                         print(evaluaciones[i])
                print("----------------------------------------------------------")

menu_4_options()    
