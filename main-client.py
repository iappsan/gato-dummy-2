import socket
from threading import Thread

HOST = "172.16.8.13"
PORT = 5432
BUFFERSIZE = 1024
MYSOCKET = socket.socket()

def receive(): # Recibe una actualizacion
    global MYSOCKET
    global BUFFERSIZE
    
    while True:
        try:
            RESPONSE = MYSOCKET.recv(BUFFERSIZE).decode('UTF-8')
            print (RESPONSE)
        except OSError:
            break

def main():
    print("Introduce la direccion IP del servidor")
    HOST = input()
    print("Introduce el puerto del servidor")
    PORT = int(input())
    MYSOCKET.connect((HOST, PORT))

    RECV_THREAD = Thread(target=receive)
    RECV_THREAD.start()

    while True:
        inputStr = input()
        MYSOCKET.send(str.encode(inputStr))

    MYSOCKET,close()

if __name__ == '__main__':
    main()