
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
        print("""
        1. Iniciar sesion
        2. Registrar
        3. Salir
        """)
        choice = int(input("Elija la opción correspondiente: "))
        if choice == 1:#iniciar sesion
            print("Iniciar sesion")
            correo = input("Correo: ")
            password = input("Password: ")
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
        elif choice == 2: #registrar
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
        elif choice == 3:
            print("Saliendo...Muchas gracias por utilizar nuestros servicios")
            sys.exit()
        else:
            print("Opción incorrecta")

def menu_sesionini(user):
    print("""
    Bienvenido
    1. Ver perfil
    2. Ramos
    3. Evaluaciones
    4. Notas
    5. Salir
    """)
    choice = int(input("Elija la opción correspondiente: "))
    if choice == 1:
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
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        print("Saliendo...Muchas gracias por utilizar nuestros servicios")
        sys.exit()

def menu_ramos(user):
    print("""
    1. Ver ramos
    2. Agregar ramo
    3. Eliminar ramo
    4. Volver
    """)
    choice = int(input("Elija la opción correspondiente: "))
    if choice == 1:
        pass
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        menu_4_options()


menu_4_options()    
