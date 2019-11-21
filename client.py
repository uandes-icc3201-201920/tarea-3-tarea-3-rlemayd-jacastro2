import socket


DIR =  "/tmp/db.tuples.sock"                #direccion predeterminada del socket


cmd = ""                                    #string de la linea de comandos
sflag = 0                                   #flag que nos dice si el usuario define un socket distinto al predeterminado
opt = socket.gethostname()
sock_dir = socket.gethostbyname(opt)
PORT = 8080
sock = 0                                    #numero en el cual guardaremos el valor que nos retorne la funcion socket()
conectado = False

while cmd != "quit":
    cmd = input(">")
    if cmd == "connect":       #veo si el comando del usuario es connect
        if conectado == 1:
            print("Ya estas conectado al servidor")
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #Creamos el socket
            cliente_addr = (sock_dir, PORT)
            if sock.connect(cliente_addr) < 0:
                print("Conexion fallida")
                exit()
            print("Conexión exitosa con el servidor!")
            conectado = True
            sock.send("conectado".encode())

    elif cmd == "disconnect" and conectado:                      #veo si el comando del usuario es disconnect
        sock.send("desconectado".encode())
        sock.close()
        conectado = False;
        print("Socket desconectado!")

    elif cmd == "list" and conectado:                            #veo si el comando del usuairo es list
        print("Lista de claves:")
        sock.send("list".encode())

        buffer = sock.recv(4096).decode()
        print(buffer)                                                       #NO ESTOY SEGURO SI ES ASI

    #si no es ninguno de los anteriores, significa que el comando es del tipo cmd(a) o cmd(a,b)
    else:
        val = cmd.strip(")").split("(")
        if val[0] == "insert" and conectado:
            val1 = val[1].split(",")
            if len(val1) == 1:
                msg = "1;"+val1[0]
                sock.send(msg.encode())
                buffer = sock.recv(4096).decode()
                print(buffer)

            elif len(val1) == 2:
                msg = "2;" + val1[0] + ";" + val1[1] + ")"
                sock.send(msg.encode())
                buffer = sock.recv(4096).decode()
                print(buffer)

        elif val[0] == "get" and conectado:
            msg = "3;"+ val[1]
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "peek" and conectado:
            msg = "4;" + val[1]
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "update" and conectado:
            val1 = val[1].split(",")
            msg = "5;" + val1[0] + ";" + val1[1] + ")"
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        elif val[0] == "delete" and conectado:
            msg = "6;" + val[1]
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            print(buffer)
        else:
            print("Comando invalido")

