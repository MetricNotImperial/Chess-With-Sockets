import socket
import pygame
import os
import time
import math
import random




WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))




pygame.font.init()
FONT = pygame.font.SysFont("Times New Roman", 200)


pygame.display.set_caption("Chess")






SERVER = "10.0.0.231"


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECTED_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)




client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)




class Board():
    def __init__(self):
       
        #first thing it does is recieve it's colour
        self.PLAYER = client.recv(2048).decode(FORMAT)
        print("Player: ",self.PLAYER)
       
        #1. your turn, #2. waiting for opponent to send a move, #3. your turn and you picked up a piece, #4. your turn and you placed the piece somewhere, #5 being choosing a piece to make the pawn to
        #makes the board based on if the player is white or black, and the state of the game
        if self.PLAYER == "w":
            self.state = "1"
            self.OPPONENT = "b"
            self.BOARD = [["BR","BH","BB","BQ","BK","BB","BH","BR"],
                        ["BP","BP","BP","BP","BP","BP","BP","BP"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["--","--","--","--","--","--","--","--"],
                        ["WP","WP","WP","WP","WP","WP","WP","WP"],
                        ["WR","WH","WB","WQ","WK","WB","WH","WR"]]
        elif self.PLAYER == "b":
            self.state = "2"
            self.OPPONENT = "w"
            self.BOARD = [["WR","WH","WB","WK","WQ","WB","WH","WR"],
                          ["WP","WP","WP","WP","WP","WP","WP","WP"],
                          ["--","--","--","--","--","--","--","--"],
                          ["--","--","--","--","--","--","--","--"],
                          ["--","--","--","--","--","--","--","--"],
                          ["--","--","--","--","--","--","--","--"],
                          ["BP","BP","BP","BP","BP","BP","BP","BP"],
                          ["BR","BH","BB","BK","BQ","BB","BH","BR"]]
        

        for i in range(8):
            if self.BOARD[7][i][1] == "K":
                king = i
                break
        #goes from left to right, starting from pawns then going down one and going from left rook, king, then right rook, to check for pawn moving twice as well as castles
        self.piecesMoved = [[True,True,True,True,True,True,True,True],
                            [True,True,True,True,True,True,True,True],
                            [True,True,True,True,True,True,True,True],
                            [True,True,True,True,True,True,True,True],
                            [True,True,True,True,True,True,True,True],
                            [True,True,True,True,True,True,True,True],
                            [False,False,False,False,False,False,False,False],
                            [False,True,True,True,True,True,True,False]]
        self.piecesMoved[7][i] = False
        

        #opponent from left to right, for the opposing teams move
        self.oppoPiecesMoved = [False,False,False,False,False,False,False,False]
           
        #makes the boards start from bottom left a1 and top right h8
        if self.PLAYER == "w":
            self.locationList = [["a","b","c","d","e","f","g","h"],["8","7","6","5","4","3","2","1"]]
        elif self.PLAYER == "b":
            self.locationList = [["h","g","f","e","d","c","b","a"],["1","2","3","4","5","6","7","8"]]
       
        self.WHITE = (244,220,180)
        self.BLACK = (180,140,100)
        #the (x,y) cords of the selected box
        self.selectedBox = [0,0]


    def draw_window(self,val = ["null","null","null"],val2 =["null"]):
        #paints the entire board including the pieces
        WIN.fill(self.WHITE)
        pieceList = [(self.PLAYER).upper()+"Q",(self.PLAYER).upper()+"H",(self.PLAYER).upper()+"R",(self.PLAYER).upper()+"B"]


        #prints all of the pieces
        for i in range(8):
            for j in range(8):


                #if a piece is selected it will make it transparent otherwise, it will be normal
               
                if self.state == "3" and i == self.selectedBox[1] and j == self.selectedBox[0]:
                    if i % 2 == 0 and j % 2 == 1:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(j*100,i*100, 100, 100))
                    elif i % 2 == 1 and j % 2 == 0:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(j*100,i*100, 100, 100))


                    img = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + self.BOARD[i][j] + ".png")
                    SURFACE = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)
                    SURFACE.set_alpha(125)
                    SURFACE.blit(img,(j*100,i*100))
                    WIN.blit(SURFACE,(0,0))
                   
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(j*100,i*100, 100, 100))
                    elif i % 2 == 0 and j % 2 == 1:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(j*100,i*100, 100, 100))
                    if self.BOARD[i][j] != "--":
                        img = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + self.BOARD[i][j] + ".png")
                       
                        WIN.blit(img,(j*100,i*100))
       
        #if the state is 3, meaning the player has picked up a piece, it will be on the cursor
        if self.state == "3":
            x = (pygame.mouse.get_pos())[0]-50
            y = (pygame.mouse.get_pos())[1]-50
            selectedPiece = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + self.BOARD[self.selectedBox[1]][self.selectedBox[0]] + ".png")
            WIN.blit(selectedPiece,(x,y))
        
        #checks if the list is not null, meaning it is not asking for a move to be animated, and if it is being asked then it continues
        if val[0] != "null":
            piece = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + val[2] + ".png")
            WIN.blit(piece,(val[0],val[1]))
        
        #checks if the player is choosing what piece the pawn should become
        if self.state == "5" and val2[0] != "null":
            if self.locationList[0].index(val2[0][2]) % 2 == 0:
                #makes the squares under the place being picked clean
                for i in range(4):
                    if i % 2 == 0:
                        pygame.draw.rect(WIN, self.WHITE, pygame.Rect(self.locationList[0].index(val2[0][2])*100,i*100, 100, 100))
                    elif i % 2 == 1:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(self.locationList[0].index(val2[0][2])*100,i*100, 100, 100))

                    piece = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + pieceList[i] + ".png")
                    WIN.blit(piece,(self.locationList[0].index(val2[0][2])*100,i*100))
            elif self.locationList[0].index(val2[0][2]) % 2 == 1:
                #makes the squares under the place being picked clean
                for i in range(4):
                    if i % 2 == 1:
                        pygame.draw.rect(WIN, self.WHITE, pygame.Rect(self.locationList[0].index(val2[0][2])*100,i*100, 100, 100))
                    elif i % 2 == 0:
                        pygame.draw.rect(WIN, self.BLACK, pygame.Rect(self.locationList[0].index(val2[0][2])*100,i*100, 100, 100))

                    piece = pygame.image.load("C:\\Users\\shubh\\OneDrive\\Desktop\\Chess\\assets\\" + pieceList[i] + ".png")
                    WIN.blit(piece,(self.locationList[0].index(val2[0][2])*100,i*100))
            



        pygame.display.update()
    
    def animatedMove(self,move):
        clock = pygame.time.Clock()

        SPEED = 30

        x1 = self.locationList[0].index(move[0])*100
        y1 = self.locationList[1].index(move[1])*100

        x2 = self.locationList[0].index(move[2])*100
        y2 = self.locationList[1].index(move[3])*100


        #for the x value, get where the new location is minus the old location, divided by 60, and that is how much to increment the piece by everytime
        #for the y value, get where the new location is minus the old location, divided by 60, and that is how much to increment the piece by everytime

        xIncrement = (x2-x1) / SPEED
        yIncrement = (y2-y1) / SPEED

        #for normal moves, not things like castle, en passant, or pawn to queen
        #players piece that is being moved
        playerPiece = self.BOARD[self.locationList[1].index(move[1])][self.locationList[0].index(move[0])]
        #temporarly changes the board and removes the piece from it
        self.BOARD[self.locationList[1].index(move[1])][self.locationList[0].index(move[0])] = "--"
        #piece the the player is moving to
        oppPiece = self.BOARD[self.locationList[1].index(move[3])][self.locationList[0].index(move[2])]



        #the old piece at that new location, and the old piece at the old location

        while True:
            clock.tick(60)

            self.draw_window([x1,y1,playerPiece])

            #increments the piece
            x1 = x1 + xIncrement
            y1 = y1 + yIncrement

            #checks if the move has moved far enough, and changes the board back to how it was before the animation
            if round(x1) == x2 and round(y1) == y2:
                self.BOARD[self.locationList[1].index(move[1])][self.locationList[0].index(move[0])] = playerPiece
                break

            pygame.display.update()


    #checks if the move made is legal and returns True if so else False
    def legalMove(self,move,pieces):
        #CHECK IF THE MOVE WAS A CASTLE FIRST AND IF NOT THEN GO TO KING

        #gets x and y values of the box inside the board
        x1 = self.locationList[0].index(move[0])
        y1 = self.locationList[1].index(move[1])

        #where they attempted to move it to
        x2 = self.locationList[0].index(move[2])
        y2 = self.locationList[1].index(move[3])

        #checks if the person is trying to move the piece to the same location and if not then you can continue
        if move[:2] != move[2:]:

            #pawn Moves
            if pieces[0][1] == "P":
                #checks if it the first move and if it is then the piece can move two pieces forward
                if x2-x1 == 0 and (y2-y1)*-1 == 2 and self.piecesMoved[y1][x1] == False and self.BOARD[y2][x2] == "--" and self.BOARD[y2+1][x2] == "--":
                    self.piecesMoved[y1][x1] = True
                    return [True]
                
                #checks if the pawn moves one forward by checking if there is no other pieces there
                elif (y2-y1)*-1 == 1 and x2-x1 == 0 and self.BOARD[y2][x2] == "--":
                    print(self.BOARD[y2][x2])
                    
                    #checks if the piece was at home
                    if y1 == 6:
                        self.piecesMoved[y1][x1] = True

                    #checks if it is at the back of the side and checks to make it a piece
                    if y2 == 0:
                        return [True,True,True]
                    return [True]

                #checks if the pawn moved diagnolly and if there is a opposiing piece there than it can
                elif (y2-y1)*-1 == 1 and abs(x2-x1) == 1 and self.BOARD[y2][x2][0] == (self.OPPONENT).upper():

                    #checks if the piece was at home
                    if y1 == 6:
                        self.piecesMoved[y1][x1] = True

                    #checks if it is at the back of the side and checks to make it a piece
                    if y2 == 0:
                        return [True,True,True]
                    return [True]
                
                #checks for en passant, by checking if the pawn moves diagnoally, checks if the piece to the right or left, the way the piece goes, is the opposite coloured pawn, and if the pawn if there is on the very next turn.
                elif (y2-y1)*-1 == 1 and abs(x2-x1) == 1 and self.BOARD[y1][x2][0] == (self.OPPONENT).upper() and self.oppoPiecesMoved[x2] == True:

                    return [True,True]

                #else no
                else: 
                    return [False]

                
                
            
            elif pieces[0][1] == "R":

                #checks if the piece was only moved horizontally or only vertically and to check if the piece trying to be taken is the players

                if (((y2-y1) == 0) or ((x2-x1) == 0)) and self.BOARD[y1][x1][0] != self.BOARD[y2][x2][0]:
                    #checks if there is a piece in the way of the two squares
                    n = 1

                    if x2-x1 == 0:
                        yIncrement = int((y2-y1)/abs(y2-y1))
                        xIncrement = 0

                    elif y2-y1 == 0:
                        xIncrement = int((x2-x1)/abs(x2-x1))
                        yIncrement = 0
                    
                    #checks top right diagnally
                    #checks if the increment plus orignal location equals new location
                    while (x1+n*xIncrement != x2 and xIncrement != 0) or (y1+n*yIncrement != y2 and yIncrement != 0):
                        #if the current increment value is on the board and not --
                        if self.BOARD[y1+yIncrement*n][x1+xIncrement*n] != "--":
                            return [False]
                        n += 1

                    return [True]
                
                else:
                    return [False]
            
            elif pieces[0][1] == "H":
                #checks if it is moved like a horse, and the horse can move over pieces, and if the piece it is trying to move onto is not the same colour
                if 1 in [abs(x2-x1), abs(y2-y1)] and 2 in [abs(x2-x1), abs(y2-y1)] and self.BOARD[y1][x1][0] != self.BOARD[y2][x2][0]:
                    return [True]
                else:
                    return [False]
            
            #checsk if the bishop moves are legal
            elif pieces[0][1] == "B":
                
                #checks if the moves was diagonol, this done by checking if the increment vertically was the same horizontally, and if the piece it was trying to take is the same as the players
                if abs(x2-x1) == abs(y2-y1) and self.BOARD[y1][x1][0] != self.BOARD[y2][x2][0]:
                    #checks if there is a piece in the way of the two squares
                    n = 1
                    xIncrement = int((x2-x1)/abs(x2-x1))
                    yIncrement = int((y2-y1)/abs(y2-y1))
                    #checks top right diagnally
                    #checks if the increment plus orignal location equals new location
                    while x1+n*xIncrement != x2:
                        #if the current increment value is on the board and not --
                        if self.BOARD[y1+yIncrement*n][x1+xIncrement*n] != "--":
                            return [False]
                        n += 1

                    return [True]

                #if it was not the same increment ampount in both directions return, false
                else:
                    return [False]
            
            #checks if the king moves are legal
            elif pieces[0][1] == "K":
                #later add a part where to check if the player can cancel, and if they are attempting to castle
                

                #checks if the piece is moved only one square away
                if ((x2-x1) in [-1,0,1] and (y2-y1) in [-1,0,1]):
                    
                    #checks if the place where the piece is moved to does not have any other piece from the players team on it, and if the piece are you are trying to take is not the opposing king
                    if (self.BOARD[y2][x2][0]).lower() != self.PLAYER:
                        
                        #also later add parts to check if the place where it is going to will be checked after moving there
                        #all the moves around the piece
                        increments = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]

                        #checks if every square directly around the move does not contain the opposing king
                        for i in range(8):
                            #checks if the piece around the board is actually on the board meaning you cannot go to square or 9
                            if (x2+increments[i][0] >= 0 and x2+increments[i][0] <= 7) and (y2+increments[i][1] >= 0 and y2+increments[i][1] <= 7):
                                #checks if the piece around the square you are trying to move into has a king right beside it, only one square away

                                if self.BOARD[y2+increments[i][1]][x2+increments[i][0]] == ((self.OPPONENT).upper()+"K"):

                                    return [False]
                        
                        #will check every black piece apart from their king and see if there is a legal move to move that piece to the new location of the king, essentially checking for a checkable spot
                        for i in range(8):
                            for j in range(8):
                                #checks if the piece it is checking for is the opponents piece and that it is not a king piece, either the players or opponenets
                                if self.BOARD[i][j][0] == (self.OPPONENT).upper() and self.BOARD[i][j][1] != "K":
                                    #checks legal move with this piece to the new king location
                                    move1 = self.locationList[0][j] + self.locationList[1][i] + move[2] + move[3]

                                    #this part does the move and stores the old move and location for later usage
                                    playerInfo = self.BOARD[y1][x1]
                                    opponenetInfo = self.BOARD[y2][x2]

                                    #this part actually does the move before checking for the legal moves
                                    self.BOARD[y2][x2] = self.BOARD[y1][x1]
                                    self.BOARD[y1][x1] = "--"

                                    #put a part where the move is done on the pboard temporarly so when the legal move function is called it doesnt assume another piece is at the location
                                    if self.legalMove(move1,[self.BOARD[i][j],playerInfo[1]])[0] == True:
                                        #reverse the move just made and return False
                                        self.BOARD[y1][x1] = playerInfo
                                        self.BOARD[y2][x2] = opponenetInfo

                                        return [False]
                                    
                                    else:
                                        #reverse the move just made
                                        self.BOARD[y1][x1] = playerInfo
                                        self.BOARD[y2][x2] = opponenetInfo

                                        

                    
                        #reverse the move and send True
                        self.BOARD[y1][x1] = playerInfo
                        self.BOARD[y2][x2] = opponenetInfo
                        return [True]



                        #add a part where if there is a piece there you are trying to take, check if it has something protecting it
                        #FOR NOW LEAVE IT IS AS
                        return [True]


                    
                    else:
                        
                        return [False]
                else:
                    return [False]

            elif pieces[0][1] == "Q":
                #checks if the piece was only moved horizontally or vertically or diagnolly and to check if the piece trying to be taken is the players
                if (((y2-y1) == 0) or ((x2-x1) == 0)) and self.BOARD[y1][x1][0] != self.BOARD[y2][x2][0]:
                    #checks if there is a piece in the way of the two squares
                    n = 1

                    if x2-x1 == 0:
                        yIncrement = int((y2-y1)/abs(y2-y1))
                        xIncrement = 0

                    elif y2-y1 == 0:
                        xIncrement = int((x2-x1)/abs(x2-x1))
                        yIncrement = 0
                    
                    #checks top right diagnally
                    #checks if the increment plus orignal location equals new location
                    while (x1+n*xIncrement != x2 and xIncrement != 0) or (y1+n*yIncrement != y2 and yIncrement != 0):
                        #if the current increment value is on the board and not --
                        if self.BOARD[y1+yIncrement*n][x1+xIncrement*n] != "--":
                            return [False]
                        n += 1

                    return [True]

                
                #checks if the moves was diagonol, this done by checking if the increment vertically was the same horizontally, and if the piece it was trying to take is the same as the players
                elif abs(x2-x1) == abs(y2-y1) and self.BOARD[y1][x1][0] != self.BOARD[y2][x2][0]:
                    #checks if there is a piece in the way of the two squares
                    n = 1
                    xIncrement = int((x2-x1)/abs(x2-x1))
                    yIncrement = int((y2-y1)/abs(y2-y1))
                    #checks top right diagnally
                    #checks if the increment plus orignal location equals new location
                    while x1+n*xIncrement != x2:
                        #if the current increment value is on the board and not --
                        if self.BOARD[y1+yIncrement*n][x1+xIncrement*n] != "--":
                            return [False]
                        n += 1

                    return [True]

                else:
                    return [False]
                
        
        #the player attempted to move the piece to the same location
        elif move[:2] == move[2:]:
            return [False]
        
        #returns False as the attempted move was to the same square it was on currently


    #changes the location of the piece on the board
    def move(self,cord,selectedBox):
        #checks if you are under check
        #checks if piece you are trying to move is pin to the king
        #checks if the move made is illegal

        #where the thing was and then the new cords of the piece(oldx,oldy,newx,newy)(a1h8 for example being the old location and new location)
        move = self.locationList[0][selectedBox[0]] + self.locationList[1][selectedBox[1]] + self.locationList[0][cord[0]] + self.locationList[1][cord[1]]

        #players piece that is being moved
        playerPiece = self.BOARD[selectedBox[1]][selectedBox[0]]
        #piece the the player is moving to
        oppPiece = self.BOARD[cord[1]][cord[0]]

        
        legalMove = self.legalMove(move,[playerPiece,oppPiece])
        print(legalMove)
        
        #checks if the move made is illegal
        if legalMove[0] == True or playerPiece[0] == (self.OPPONENT).upper():

            #move legal
        
            self.state = "4"

            self.animatedMove(move)

            #checks if it is not the pawn promoting to the last square
            if len(move) == 4:
                #changes the boards piece of where the thing was at that boxm into the selected boxes piece
                self.BOARD[cord[1]][cord[0]] = self.BOARD[selectedBox[1]][selectedBox[0]]

            elif len(move) != 4:
                #checks if it is the pawn promoting to the last square and if it is then the that square becomes whtever the move was choosen from Q,H,R,B
                self.BOARD[cord[1]][cord[0]] = move[5:]
                print(move[5:])
                print(self.BOARD[cord[1]][cord[0]])
            #changes the old location to an empty square
            self.BOARD[selectedBox[1]][selectedBox[0]] = "--"

            #if it is en pasant move
            if len(legalMove) == 2 or ((self.locationList[1].index(move[3])-self.locationList[1].index(move[1])) == 1 and abs(self.locationList[0].index(move[2])-self.locationList[0].index(move[0])) == 1 and playerPiece[0] == (self.OPPONENT).upper()):
                self.BOARD[selectedBox[1]][cord[0]] = "--"

            #checks if a pawn is own the last square
            elif len(legalMove) == 3:
                self.state = "5"

        else:
            move = "null"

        #makes all the en passant moves go away
        self.oppoPiecesMoved = [False,False,False,False,False,False,False,False]
        
        #sends the move done
        return move
        


    #decodes opponents message as a move and changes the board
    def oppoMove(self):
        #b2b3
        move = client.recv(2048).decode(FORMAT)
        print("Opp Move",move)


        x1 = self.locationList[0].index(move[0])
        y1 = self.locationList[1].index(move[1])


        x2 = self.locationList[0].index(move[2])
        y2 = self.locationList[1].index(move[3])


        val = self.move([x2,y2],[x1,y1])

 
        if abs(y2-y1) == 2 and move[0] == move[2] and self.BOARD[y2][x2][1] == "P":
            self.oppoPiecesMoved[x2] = True

        self.state = "1"






BOARD = Board()


#main game loop waiting to see what the player will do while it is their turn
run = True
clock = pygame.time.Clock()

while run:
    BOARD.draw_window()
    clock.tick(60)


    #checks if the state(the turn) is ours, and will check for input
    if BOARD.state == "1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #will get the box the player is clicking
                x = (pygame.mouse.get_pos())[0]//100
                y = (pygame.mouse.get_pos())[1]//100
                #checks if the thing selected is the players piece, and if so changes the state to that
                if (BOARD.BOARD[y][x][0]).lower() == BOARD.PLAYER:
                    BOARD.state = "3"
                    BOARD.selectedBox = [x,y]

    #checks if the state(the turn) is the player has selected a certain piece
    elif BOARD.state == "3":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #will get the box the player is clicking
                x = (pygame.mouse.get_pos())[0]//100
                y = (pygame.mouse.get_pos())[1]//100
                #has to check if it is a legal move, HAVE NOT CODED THAT PART YET
                move = BOARD.move([x,y],BOARD.selectedBox)
                if move != "null" and BOARD.state != "5":
                    #makes it blacks turn
                    BOARD.state = "2"
                    print("Player Move",move)
                    client.send((move).encode(FORMAT))
                elif move == "null" and BOARD.state != "5":
                    #makes it so your picking a piece up again
                    BOARD.state = "1"

                    


    elif BOARD.state == "2":
       
        BOARD.draw_window()
        BOARD.oppoMove()
        n = 0

    #checks if the plqayer is making a pawn into a piece
    elif BOARD.state == "5":
        while BOARD.state != "2":
            pawnPieces = [(BOARD.PLAYER).upper()+"Q",(BOARD.PLAYER).upper()+"H",(BOARD.PLAYER).upper()+"R",(BOARD.PLAYER).upper()+"B",]
            BOARD.draw_window(["null","null","null"],[move])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #will get the box the player is clicking
                    x = (pygame.mouse.get_pos())[0]//100
                    y = (pygame.mouse.get_pos())[1]//100
                    if x == BOARD.locationList[0].index(move[2]) and y >= 0 and y <= 3:
                        BOARD.BOARD[0][x] = pawnPieces[y]
                        move = move+"="+pawnPieces[y]
                        #makes it blacks turn a1a1=KQ

                        print("Player Move",move)
                        client.send((move).encode(FORMAT))

                        BOARD.state = "2"
                        


   
               
pygame.quit()









