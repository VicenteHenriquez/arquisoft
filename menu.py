
import socket
import sys
#create a socket client

def connect_socket():
    try:
        global host
        global port
        global s
        host = 'localhost'
        port = 5000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

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
        choice = int(input("Enter your choice: "))
        if choice == 1:
            #iniciar sesion
            print("Iniciar sesion")
            correo = input("Correo: ")
            password = input("Password: ")
            largo = 5 + len(correo) + 1 + len(password)
            texto = larstr(largo) + "serv1" + correo + " " + password
            connect_socket()
            s.send(texto.encode("utf-8"))
            resp = s.recv(4096)
            print(resp.decode("utf-8"))
            
            pass
        elif choice == 2:
            #registrar
            pass
        elif choice == 3:
            sys.exit()

menu_4_options()    
