import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))

sock.send(b'00012sinitOKadusr')
data = sock.recv(4096)
print(data.decode())

while True:
    data = sock.recv(4096)
    print(data.decode())
    data = data.decode()[10:]
    espacio = data.find(' ')
    usuario = data[:espacio]
    password = data[espacio+1:]
    print(usuario, password)

