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
    cnct_msj = conexion.recv(1024).decode()  # se recibe un mensaje inicial de coneccion, si el mensaje es "conectado" se procede con la coneccion, de otro modo el proceso termina
    cnct_msj = cnct_msj.split("/")
    #si el mansaje inicial es connect, ser inicia la coneccion del cliente
    if cnct_msj[1] == "connect":
        print("Se ha conectado el cliente",dir_cl[0])
        conectado = True
    else:
        return None

    header = str(DIR)+","+str(PORT)+","+str(dir_cl)
    while conectado:
        try:
            mensaje = conexion.recv(1024).decode()
        except:
            print("Error de conexion con el cliente!")
            conectado = False
            break
        mensaje = mensaje.split("/")
        if mensaje[1] == "close":
            conexion.close()
            print("El cliente se ha desconectado de manera abrupta")
            conectado = False
        elif mensaje[1] == "insert":
            #se genera la entrada en la base de datos con el valor entregado
            lock.acquire()              #Para bloquear entrada en la seccion critica
            val = mensaje[2]
            global KEY
            if KEY in BD:
                while KEY in BD:
                    KEY += 1

            BD[KEY] = val
            state = "211"
            body = "Se ha insertado el valor \"{}\" con la key \"{}\"".format(val,KEY)
            msj = state+"/"+header+"/"+body
            conexion.sendall(msj.encode())
            print("Cliente",dir_cl[0],", a guardado el valor","\""+str(val)+"\"","en la base de datos con key","\""+str(KEY)+"\"")
            lock.release()          #Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "insertKV":
            lock.acquire()  # Para bloquear entrada en la seccion critica
            kv = mensaje[2].split(",")
            try:
                key = int(kv[0])
            except:
                state = "430"
                body = "Key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            val = kv[1]
            if key not in BD:
                BD[key] = val
                state = "210"
                body = "Se ha insertado el valor \"{}\" con la key \"{}\"".format(val,key)
            else:
                state = "410"
                body = "Key ya existente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente",dir_cl[0],", a guardado el valor","\""+str(val)+"\"","en la base de datos con key","\""+str(key)+"\"")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "peek":
            lock.acquire()  # Para bloquear entrada en la seccion critica
            try:
                key = int(mensaje[2])
            except:
                state = "430"
                body = "Key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            if key in BD:
                state = "230"
                body = "True"
            else:
                state = "420"
                body = "False"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente",dir_cl[0],", a pedido verificar la llave","\""+str(key)+"\"","en la base de datos")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "get":
            lock.acquire()  # Para bloquear entrada en la seccion critica
            try:
                key = int(mensaje[2])
            except:
                state = "430"
                body = "Key invalida"
                msj = state + "/" + header + "/" + body
                conexion.sendall(msj.encode())
                continue
            if key in BD:
                state = "220"
                body = BD[key]
            else:
                state = "420"
                body = "Key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente",dir_cl[0],", a pedido obtener el valor de la llave","\""+str(key)+"\"","en la base de datos")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "update":
            lock.acquire()  # Para bloquear entrada en la seccion critica
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
                body = "Se ha cambiado el valor \"{}\" por \"{}\", en la key \"{}\"".format(pval, val, key)
            else:
                state = "420"
                body = "Error, key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente", dir_cl[0], ", a pedido actualizar el valor de la llave", "\""+str(key)+"\"", "en la base de datos")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "delete":
            lock.acquire()  # Para bloquear entrada en la seccion critica
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
                body = "se ha eliminado el valor \"{}\" junto a su key \"{}\"".format(eval, key)
            else:
                state = "420"
                body = "Error, key inexistente"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente", dir_cl[0], ", a pedido eliminar la llave", "\""+str(key)+"\" junto a su key","\""+str(eval)+"\"", "en la base de datos")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "list":
            lock.acquire()  # Para bloquear entrada en la seccion critica
            body = ""
            for k in BD:
                body += str(k)
                body += ","
            state = "260"
            msj = state + "/" + header + "/" + body
            conexion.sendall(msj.encode())
            print("Cliente", dir_cl[0], ", a pedido listado de la base de datos")
            lock.release()  # Para finalizar el bloqueo de la seccion critica
        elif mensaje[1] == "disconnect":
            conexion.close()
            print("El cliente se ha desconectado")
            conectado = False

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