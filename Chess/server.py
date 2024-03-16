import socket
import threading

import os
import random
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)



class Game:
    def __init__(self):
        self.board = [["BR","BH","BB","BQ","BK","BB","BH","BR"],
                    ["BP","BP","BP","BP","BP","BP","BP","BP"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["WP","WP","WP","WP","WP","WP","WP","WP"],
                    ["WR","WH","WB","WQ","WK","WB","WH","WR"]]
        self.turn = "w"

        #until both players have joined the game it will be null
        self.player1 = "-"
        self.player2 = "-"

        self.clientList = []


    def move():
        pass

    def sendPlayers(self):

        #randomizes which player is which colour
        turnNumb = random.randint(1,2)
        if turnNumb == 1:
            self.player1 = "w"
            self.player2 = "b"
        elif turnNumb == 2:
            self.player1 = "b"
            self.player2 = "w"
        
        #sends each player there colour
        self.clientList[0][0].send((self.player1).encode(FORMAT))
        print("Player1",self.player1)
        self.clientList[1][0].send((self.player2).encode(FORMAT))
        print("Player2",self.player2)



game = Game()

server.listen(2)
print(f"[SERVER] Server is listening on {SERVER}")

while True:
    conn, addr  = server.accept()
    game.clientList.append([conn,addr])
    if len(game.clientList) == 2: 
        print(f"[ACTIVE CONNECTIONS] {len(game.clientList)}")
        break     

#sends each player the type of player they are
game.sendPlayers()

#waits for the move of the player and changes board, as well as sends the opposing teaming the move being made
while True:
    print("Turn",game.turn)

    #sends move to player that is waiting right now
    if game.player1 == game.turn:
        move = game.clientList[0][0].recv(2048).decode(FORMAT)
        print(game.player1,move)
        game.clientList[1][0].send((move).encode(FORMAT))
        #recieves in form of letter#letter#, first move to new place
        
        

    elif game.player2 == game.turn:
        move = game.clientList[1][0].recv(2048).decode(FORMAT)
        print(game.player2,move)
        game.clientList[0][0].send((move).encode(FORMAT))
        #recieves in form of letter#letter#, first move to new place
        
        
    
    #changes turn based on who made a move
    if game.turn == "w":
        game.turn = "b"
    elif game.turn == "b":
        game.turn = "w"
    
    