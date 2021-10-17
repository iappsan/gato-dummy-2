import socket

HOST = "192.168.1.107"
PORT = 5432
BUFFERSIZE = 1024
MYSOCKET = socket.socket()

def main():
    print("Introduce la direccion IP del servidor")
    HOST = input()
    print("Introduce el puerto del servidor")
    PORT = int(input())
    MYSOCKET.connect((HOST, PORT))

    while True:
        RESPONSE = MYSOCKET.recv(BUFFERSIZE).decode('UTF-8')
        print (RESPONSE)
        inputStr = input()
        MYSOCKET.send(str.encode(inputStr))

    MYSOCKET,close()

if __name__ == '__main__':
    main()