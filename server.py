# -*- coding: utf-8 -*-

import socket
import _thread

#BASE DE DATOS
import random
key = random.randint(1000,10001)

BD = {}


####FUNCIONAMIENTO DE SERVIDOR####

#parametros del servidor
host = socket.gethostname()
DIR = socket.gethostbyname(host)
PORT = 8080

#funcion de comunicacion cliente-servidor
def server_cliente(conexion, dir_cl):
    conectado = False
    cnct_msj = conexion.recv(1024).decode()#se recibe un mensaje inicial de coneccion, si el mensaje es "conectado" se procede con la coneccion, de otro modo el proceso termina
    if cnct_msj == "conectado":
        conectado = True
    else:
        return None
    
    cont = 0
    
    while conectado:
        mensaje = conexion.recv(1024).decode()
        print(mensaje)
        cont += 1
        
        if cont == 10:
            break
    return None

#inicio del proceso servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creamos el socket

svr_addr = (DIR,PORT)
sock.bind(svr_addr)
print("server iniciado...")

#inicio de procesamiento de clientes
sock.listen()
while 1:
    conn, cl_addr = sock.accept()
    _thread.start_new_thread(server_cliente,(conn,cl_addr))