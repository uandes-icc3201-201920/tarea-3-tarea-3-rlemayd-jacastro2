import socket
import sys


cmd = ""#string de la linea de comandos
info = socket.gethostbyname_ex(socket.gethostname())
cl_name = info[0]
cl_dir = info[-1][0]
sock_dir = info[-1][1]
PORT = 42069
conectado = False

if "-s" in sys.argv:
    idx = sys.argv.index("-s")
    sock_dir = sys.argv[idx+1]

header = str(PORT)+","+str(cl_dir)
while cmd != "quit":

    cmd = input(">")
    if cmd == "connect":       #veo si el comando del usuario es connect
        oper = "connect"
        data = None
        if conectado == 1:
            print("Ya estas conectado al servidor")
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #Creamos el socket
            sock.connect((sock_dir, PORT))

            msg = header+"/"+oper+"/"+str(data)
            print("Conexión exitosa con el servidor!")
            conectado = True
            sock.send(msg.encode())
    elif conectado == True:
        if cmd == "disconnect" and conectado:                      #veo si el comando del usuario es disconnect
            oper = "disconnect"
            data = None
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())
            sock.close()
            conectado = False
            print("Socket desconectado!")

        elif cmd == "list" and conectado:                            #veo si el comando del usuairo es list

            oper = "list"
            data = None
            msg = header + "/" + oper + "/" + str(data)
            sock.send(msg.encode())

            buffer = sock.recv(4096).decode()
            buff = buffer.split("/")

            if len(buff[2]) > 0:
                buffL = buff[2].strip(",").split(",")
                buffFinal = ""
                for t in buffL:
                    buffFinal += (str(t)+"\n")
                buffFinal+="Fin de lista de claves"
                print("Lista de claves:")
                print(buffFinal)
            else:
                print("No hay elementos en la base de datos!")

        #si no es ninguno de los anteriores, significa que el comando es del tipo cmd(a) o cmd(a,b)
        else:
            if "(" not in cmd and ")" not in cmd:
                print("comando invalido")
                continue
            val = cmd.strip(")").split("(")
            if val[0] == "insert" and conectado:
                val1 = val[1].split(",")
                if len(val1) == 1:
                    oper = "insert"
                    data = str(val1[0])
                    msg = header + "/" + oper + "/" + str(data)
                    sock.send(msg.encode())

                    buffer = sock.recv(4096).decode()
                    buff = buffer.split("/")
                    print(buff[2])

                elif len(val1) == 2:
                    oper = "insertKV"
                    try:
                        int(val1[0])
                    except:
                        print ("Error: las llaves deben ser valores numericos")
                        continue
                    data = str(val1[0])+","+str(val1[1])
                    msg = header + "/" + oper + "/" + str(data)
                    sock.send(msg.encode())

                    buffer = sock.recv(4096).decode()
                    buff = buffer.split("/")
                    code = buff[0]
                    if code == "210":
                        print(buff[2])
                    elif code == "410":
                        print("ERROR 410:", buff[2])
                    elif code == "430":
                        print("ERROR 430:", buff[2])

            elif val[0] == "get" and conectado:
                oper = "get"
                try:
                    int(val[1])
                except:
                    print ("Error: las llaves deben ser valores numericos")
                    continue
                data = str(val[1])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                buff = buffer.split("/")
                code = buff[0]
                if code == "210":
                    print("El valor pedido por la llave",val[1],"es:",buff[2])
                elif code == "410":
                    print("ERROR 410:", buff[2])
                elif code == "430":
                    print("ERROR 430:", buff[2])

            elif val[0] == "peek" and conectado:
                try:
                    int(val[1])
                except:
                    print ("Error: las llaves deben ser valores numericos")
                    continue
                oper = "peek"
                data = str(val[1])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                buff = buffer.split("/")
                code = buff[0]
                if code == "230":
                    print(buff[2])
                elif code == "420":
                    print(buff[2])
                    print("Error 420: clave inexistente")
                elif code == "430":
                    print("Error 430: clave invalida")
            elif val[0] == "update" and conectado:
                val1 = val[1].split(",")
                try:
                    int(val1[0])
                except:
                    print ("Error: las llaves deben ser valores numericos")
                    continue
                oper = "update"
                data = str(val1[0]) + "," + str(val1[1])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                buff = buffer.split("/")
                code = buff[0]
                if code == "210":
                    print(buff[2])
                elif code == "410":
                    print("ERROR 410:", buff[2])
                elif code == "430":
                    print("ERROR 430:", buff[2])
            elif val[0] == "delete" and conectado:
                try:
                    int(val[1])
                except:
                    print ("Error: las llaves deben ser valores numericos")
                    continue
                oper = "delete"
                data = str(val[1])
                msg = header + "/" + oper + "/" + str(data)
                sock.send(msg.encode())

                buffer = sock.recv(4096).decode()
                buff = buffer.split("/")
                code = buff[0]
                if code == "210":
                    print(buff[2])
                elif code == "410":
                    print("ERROR 410:", buff[2])
                elif code == "430":
                    print("ERROR 430:", buff[2])
            elif val[0]=="quit":
                break
            else:
                if val[0]!="connect":
                    print("Comando invalido")
    else:
        if cmd!="quit":
            print("Para realizar una operación primero debes conectarte al server, con el comando connect")

if conectado:
    oper = "close"
    data = None
    msg = header + "/" + oper + "/" + str(data)
    sock.send(msg.encode())
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
