# -*- coding: utf-8 -*-

import socket
import _thread

# BASE DE DATOS
import random

KEY = random.randint(1000, 10001)

BD = {}

####FUNCIONAMIENTO DE SERVIDOR####

# parametros del servidor
host = socket.gethostname()
DIR = socket.gethostbyname(host)
PORT = 8080


# funcion de comunicacion cliente-servidor
lock = _thread.allocate_lock()
def server_cliente(conexion, dir_cl):
    conectado = False
    cnct_msj = conexion.recv(
        1024).decode()  # se recibe un mensaje inicial de coneccion, si el mensaje es "conectado" se procede con la coneccion, de otro modo el proceso termina
    cnct_msj = cnct_msj.split("/")
    #si el mansaje inicial es connect, ser inicia la coneccion del cliente
    if cnct_msj[1] == "connect":
        print("Se ha conectado un cliente!")
        conectado = True
    else:
        return None

    header = str(DIR)+","+str(PORT)+","+str(dir_cl)
    while conectado:
        mensaje = conexion.recv(1024).decode()
        mensaje = mensaje.split("/")
        if mensaje[1] == "insert":
            #se genera la entrada en la base de datos con el valor entregado
            val = mensaje[2]
            global KEY
            if KEY in BD:
                while KEY in BD:
                    KEY += 1

            BD[KEY] = val
            state = "211"
            body = "Se ha insertado el valor {} con la key {}".format(val,KEY)
            msj = state+"/"+header+"/"+body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "insertKV":
            kv = mensaje[2].split(",")
            try:
                key = int(kv[0])
            except:
                state = "430"
                body = "Error, key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            val = kv[1]
            if key not in BD:
                BD[key] = val
                state = "210"
                body = "Se ha insertado el valor {} con la key {}".format(val,key)
            else:
                state = "410"
                body = "Error de insercion, key ya existente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "peek":
            try:
                key = int(mensaje[2])
            except:
                state = "430"
                body = "Error, key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            if key in BD:
                state = "230"
                body = "key existente"
            else:
                state = "420"
                body = "key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "get":
            try:
                key = int(mensaje[2])
            except:
                state = "430"
                body = "Error, key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            if key in BD:
                state = "220"
                body = BD[key]
            else:
                state = "420"
                body = "Error, key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "update":
            kv = mensaje[2].split(",")
            try:
                key = int(kv[0])
            except:
                state = "430"
                body = "Error, key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            val = kv[1]
            if key in BD:
                pval = BD[key]
                BD[key] = val
                state = "240"
                body = "Se ha cambiado el valor {} por {}, en la key {}".format(pval, val, key)
            else:
                state = "420"
                body = "Error, key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "delete":
            try:
                key = int(mensaje[2])
            except:
                state = "430"
                body = "Error, key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            if key in BD:
                eval = BD[key]
                BD.pop(key)
                state = "250"
                body = "se ha eliminado el valor {} presente en la key {}".format(eval, key)
            else:
                state = "420"
                body = "Error, key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
        elif mensaje[1] == "list":
            body = ""
            for k in BD:
                body += str(k)
                body += ","
            state = "260"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
    return None


# inicio del proceso servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creamos el socket

svr_addr = (DIR, PORT)
sock.bind(svr_addr)
print("server iniciado...")

# inicio de procesamiento de clientes
sock.listen()
while 1:
    conn, cl_addr = sock.accept()
    _thread.start_new_thread(server_cliente, (conn, cl_addr))