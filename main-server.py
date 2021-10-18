import socket
from random import randrange
import time

HOST = "172.16.8.13"      # El hostname o IP del servidor
PORT = 5432                 # El puerto que usa el servidor
BUFFERSIZE = 1024           # Tamano del buffer
MYSOCKET = socket.socket()  # Iniciamos el socket
MYSOCKET.bind((HOST, PORT)) # Lo ligamos al host y al puerto
MYSOCKET.listen(10)         # Definimos el numero de conecciones a escuchar
GAMESTATE = 0               # Estado actual del juego
GAMEDIFFICULT = 0           # Dificultad del juego
TABLES = [[                 # Tableros
            [' ','A','B','C'],
            ['1','-','-','-'],
            ['2','-','-','-'],
            ['3','-','-','-']
        ], [
            [' ','A','B','C','D','E'],
            ['1','-','-','-','-','-'],
            ['2','-','-','-','-','-'],
            ['3','-','-','-','-','-'],
            ['4','-','-','-','-','-'],
            ['5','-','-','-','-','-']
        ]]
GAMETABLE = TABLES[1]       # Inicializa un tablero
PLAYERS =[]                 # Lista de jugadores
FICHAS = []                 # Fichas de jugadores

def validPos(throwPos, playerChar):      # Verifica si la posicion es valida
    convertedPos = ""
    if throwPos[0].isdigit():
        convertedPos = throwPos[1]
        throwPos = str(throwPos[0]) + str(throwPos[0])
    else:
        if throwPos[0] == "A":
            convertedPos = '1'
        elif throwPos[0] == "B":
            convertedPos = '2'
        elif throwPos[0] == "C":
            convertedPos = '3'
        elif throwPos[0] == "D":
            convertedPos = '4'
        elif throwPos[0] == "E":
            convertedPos = '5'
        else:
            return False
    
    if GAMETABLE[int(throwPos[1])][int(convertedPos)] == '-':
        GAMETABLE[int(throwPos[1])][int(convertedPos)] = playerChar
        print("pos valida "+throwPos[1]+convertedPos)
        return True
    else:
        print("pos NO valida")
        return False

def pcThrow():                          # Genera un tiro aleatorio
    ready = False
    if GAMEDIFFICULT == 1:
        size = 4
    else:
        size = 6
    while ready == False:
        randStr = str(randrange(1,size)) + str(randrange(1,size))
        print ("Intento de pc: "+randStr)
        ready = validPos(randStr, 'o')

def tableToStr():                       # Convierte el tablero a cadena
    genStr = '\n'
    for i in range(len(GAMETABLE)):
        for j in range(len(GAMETABLE[i])):
            genStr = genStr + str(GAMETABLE[i][j]) +' '
        genStr = genStr + '\n'

    return genStr

def gameFinished(char2check):           # Se verifican las lineas
    size = 0
    i = 1
    j = 1
    print("validando ganador " + str(type(char2check)))
    if GAMEDIFFICULT == 1:
        size = 4
    else:
        size = 6
    print("flag1")
    while i < size:
        if GAMETABLE[i][j] == char2check:
            j+=1
        else:
            i+=1
            j=1
        if j == size:
            print("Fila")
            return True

    print("flag2")
    i = 1
    while i < size:
        if GAMETABLE[j][i] == char2check:
            j+=1
        else:
            i+=1
            j=1
        if j == size:
            print("Columna")
            return True

    i = 1
    j = 1
    print("flag3")
    while i < size:
        if GAMETABLE[i][j] == char2check:
            i+=1
            j+=1
        else:
            i = size
    if j == size:
        print("Diagonal 1")
        return True
    
    i = 1
    j = size-1
    print("flag4")
    while i < size:
        if GAMETABLE[i][j] == char2check:
            i+=1
            j-=1
        else:
            i = size
    if j == 0:
        print("diagonal 2")
        return True
    
    print("Aun no gana nadie")
    return False

def actualizaPantallas(msg):
    for player in PLAYERS:
        player.send(msg)

print("En espera ... ")
CONN, ADDR = MYSOCKET.accept()      # En espera de cliente
PLAYERS.append(CONN)
INITIME = time.time()
print ("Nueva conexion!")
print (ADDR)

STATESTR = ""                       # Se inicializan valores para el juego
WINNERSTR = ""
AGAINSTR = ""
THROWCOUNTER = 0
TURNO = 0
GOOD_THROW = True

while (GAMESTATE == 0):             # Bienvenida al gato dummy

    STATESTR = "Escribe la cordenada de tu siguiente tiro"
    AGAINSTR = "Juegas de nuevo?\n(1)Si\n(2)No"
    THROWCOUNTER = 0
    GAMESTATE = 1

    while GAMESTATE == 1:       # Preguntando por dificultad y agregando jugadores
        CONN.send(str.encode("Bienvenido al Gato Dummy :)\n"
                        +"Elige dificultad\n(1) Normal\n(2) Avanzado"))
        gd_data = int(CONN.recv(BUFFERSIZE).decode('UTF-8'))
        print("Dificultad elegida: "+ str(gd_data))

        CONN.send(str.encode("Cuantos jugadores mas juegan?\n"
                        +"(1 - 10)"))

        NUM_PLAYERS = int(CONN.recv(BUFFERSIZE).decode('UTF-8'))
        print("Jugadores totales: "+ str(NUM_PLAYERS))
        TURNO = NUM_PLAYERS

        CONN.send(str.encode("Elige una ficha"))

        FICHA = CONN.recv(BUFFERSIZE).decode('UTF-8')
        print("Ficha elegida: "+ str(FICHA))
        FICHAS.append(FICHA)

        CONN.send(str.encode("Tu turno es el: "+str(TURNO-NUM_PLAYERS)))

        while NUM_PLAYERS > 0:
            print ('Esperando '+str(NUM_PLAYERS)+' jugadores mas')
            CONN, ADDR = MYSOCKET.accept()
            PLAYERS.append(CONN)
            print ("Nueva conexion!")
            print (ADDR)
            CONN.send(str.encode("Elige una ficha\n"))

            FICHA = CONN.recv(BUFFERSIZE).decode('UTF-8')
            print("Ficha elegida: "+ str(FICHA))
            FICHAS.append(FICHA)
            CONN.send(str.encode("Tu turno es el: "+str(TURNO-NUM_PLAYERS)))
            NUM_PLAYERS = NUM_PLAYERS - 1;

        if gd_data == 1:
            GAMEDIFFICULT = 1
            GAMESTATE = 2
            THROWCOUNTER = 9
            GAMETABLE = TABLES[0]
        elif gd_data == 2:
            GAMEDIFFICULT = 2
            GAMESTATE = 2
            THROWCOUNTER = 25
            GAMETABLE = TABLES[1]
        else:
            gd_data = ""

        NUM_PLAYERS = TURNO
        print ('Ficha elegida: ')
        for f in FICHAS:
            print (str(f))

    while GAMESTATE == 2:       # Desarrollo del juego

        if GOOD_THROW :
            if TURNO == NUM_PLAYERS:
                TURNO = 0
            else:
                TURNO += 1
        else:
            GOOD_THROW = True

        print ('Turno: ' + str(TURNO))
        CONN = PLAYERS[TURNO]

        if THROWCOUNTER > 0:
            actualizaPantallas(str.encode('Turno de:'+FICHAS[TURNO]+'\n'+tableToStr() +STATESTR))
            gt_data = CONN.recv(BUFFERSIZE).decode('UTF-8')
            print ("Tiro elegido: " + str(gt_data))

            if validPos(gt_data, FICHAS[TURNO]):
                STATESTR = "Escribe la cordenada de tu siguiente tiro"
                if gameFinished(FICHAS[TURNO]):
                    WINNERSTR = tableToStr() + "Has ganado " +FICHAS[0]+ "!\n"
                    GAMESTATE = 3
                else:
                    THROWCOUNTER -= 1
            else:
                GOOD_THROW = False
                STATESTR = "No puedes tirar ahi\nElige un nuevo lugar"
        else:
            WINNERSTR = "Empate! Ya no quedan mas tiros\n"
            GAMESTATE = 3

    while GAMESTATE == 3:       # Quieres jugar de nuevo?
        CONN = PLAYERS[0]
        ENDTIME = time.time()
        AGAINSTR = WINNERSTR + "La partida ha durado " + str(ENDTIME-INITIME) + " segundos\n" + AGAINSTR
        actualizaPantallas(str.encode(AGAINSTR))
        ng_data = int(CONN.recv(BUFFERSIZE).decode('UTF-8'))

        if ng_data == 1:
            print("va de nuez")
            GAMESTATE = 0
        elif ng_data == 2:
            print("Bye")
            GAMESTATE = 4

for p in PLAYERS:
    p.close();