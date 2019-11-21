import socket


DIR =  "/tmp/db.tuples.sock"                #direccion predeterminada del socket


cmd = ""                                    #string de la linea de comandos
sflag = 0                                   #flag que nos dice si el usuario define un socket distinto al predeterminado
opt = socket.gethostname()
sock_dir = socket.gethostbyname(opt)
PORT = 8080
sock = 0                                    #numero en el cual guardaremos el valor que nos retorne la funcion socket()
conectado = False
header = str(PORT)+","+str(sock_dir)
while cmd != "quit":

    cmd = input(">")
    if cmd == "connect":       #veo si el comando del usuario es connect
        oper = "connect"
        data = None
        if conectado == 1:
            print("Ya estas conectado al servidor")
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #Creamos el socket
            cliente_addr = (sock_dir, PORT)
            sock.connect(cliente_addr)

            msg = header+"/"+oper+"/"+str(data)
            print("Conexión exitosa con el servidor!")
            conectado = True
            sock.send(msg.encode())

    elif cmd == "disconnect" and conectado:                      #veo si el comando del usuario es disconnect
        oper = "disconnect"
        data = None
        msg = header + "/" + oper + "/" + str(data)
        sock.send(msg.encode())
        sock.close()
        conectado = False;
        print("Socket desconectado!")

    elif cmd == "list" and conectado:                            #veo si el comando del usuairo es list
        print("Lista de claves:")
        oper = "list"
        data = None
        msg = header + "/" + oper + "/" + str(data)
        sock.send(msg.encode())

        buffer = sock.recv(4096).decode()
        print(buffer)                                                       #NO ESTOY SEGURO SI ES ASI

    #si no es ninguno de los anteriores, significa que el comando es del tipo cmd(a) o cmd(a,b)
    else:
        val = cmd.strip(")").split("(")
        if val[0] == "insert" and conectado:
            val1 = val[1].split(",")
            if len(val1) == 1:
                oper = "insert"
                data = str(val1[0])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                print(buffer)

            elif len(val1) == 2:
                oper = "insertKV"
                data = str(val1[0])+","+str(val1[1])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                print(buffer)

        elif val[0] == "get" and conectado:
            oper = "get"
            data = str(val[1])
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "peek" and conectado:
            oper = "peek"
            data = str(val[1])
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "update" and conectado:
            val1 = val[1].split(",")
            oper = "update"
            data = str(val1[0]) + "," + str(val1[1])
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "delete" and conectado:
            oper = "delete"
            data = str(val[1])
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0]=="quit":
            break
        else:
            print("Comando invalido")

if conectado:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()