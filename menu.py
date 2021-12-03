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
    2. Ramos
    3. Evaluaciones
    4. Notas
    5. Salir
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
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        print("Cerrando sesion...")
        return menu_4_options()
    else:
        print("Opción incorrecta")
        return menu_sesionini(user)

def menu_ramos(user):
    print("----------------------------------------------------------")
    print("""
    1. Ver ramos
    2. Agregar ramo
    3. Eliminar ramo
    4. Volver
    """)
    print("----------------------------------------------------------")
    choice = input("Elija la opción correspondiente: ")
    if choice == "1": #ver ramos
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
        print("Escriba el numero del ramo que desea ver: ")
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
            respuesta = respuesta.split("---")
            print(respuesta)
            print("----------------------------------------------------------")
            print("Nombre: " + respuesta[0])
            print("Descripción: " + respuesta[1])
            print("Profesor: " + respuesta[2])
            print("----------------------------------------------------------")
            return menu_ramos(user)

    elif choice == "2": #agregar ramo
        print("----------------------------------------------------------")
        print("INGRESE LOS DATOS DEL RAMO")
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
    
    elif choice == "3": #eliminar ramo
        pass
    
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
    if choice == "1":
        pass
    elif choice == "2":
        print("----------------------------------------------------------")
        print("INGRESE LOS DATOS DE LA  NUEVA EVALUACIÓN: ")
        ramo = str(input("Ramo: "))
        nombre = str(input("Nombre: "))
        fecha = str(input("Fecha(dd/mm/aaaa): "))
        ponderacion = str(input("Ponderación(ej. 1 = 100%, 0.2 = 20%): "))
        descripcion = str(input("Descripción: "))
        nota = str(input("Nota(si no tiene, dejar en blanco): "))
        print("----------------------------------------------------------")
        usuario = user
        largo = 5 + 1 + len(usuario) + 3 + len(nombre) + 3 + len(fecha) + 3 + len(ponderacion) + 3 + len(descripcion) + 3 + len(nota) + 3 + len(ramo)
        texto = larstr(largo) + "adeva" + "---" + nombre + "---" + fecha + "---" + ponderacion + "---" + descripcion + "---" + nota + "---" + ramo
        s.send(texto.encode("utf-8"))
        resp = s.recv(4096)
        respuesta = resp.decode("utf-8")
        print(respuesta)
        if respuesta == "err":
            print("Ramo no encontrado")
            return menu_evaluaciones(user)
        else:
            pass
        
    elif choice == "3":
        pass
    elif choice == "4":
        menu_sesionini(user)
    else:
        print("Opción incorrecta")
        return menu_evaluaciones(user)

menu_4_options()    
