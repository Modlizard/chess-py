import os #Used to get current directory
import json
from tkinter import *
from verifier import * #Custom module made for verifying moves, checks etc.
from copy import deepcopy #Used for verifying checks and checkmates where board cloning is necessary

window=Tk()
pieceDir = os.path.dirname(os.path.realpath(__file__))+'\pieces\\' #Filepath uses paths instead of getcwd() because other IDE's often change the cwd

with open(os.path.dirname(os.path.realpath(__file__))+'\config.json','r') as settingsFile: #Loads the board colours config
    cfgColours = json.load(settingsFile)

pieceChars = {'wP':'♙','wN':'♘','wB':'♗','wR':'♖','wK':'♔','wQ':'♕', #Quirky ascii characters used in the move history
              'bP':'♟','bN':'♞','bB':'♝','bR':'♜','bK':'♚','bQ':'♛'}
fullName = {'w': 'white', 'b': 'black', 'P':'pawn', 'N':'knight', 'B':'bipshop', 'R':'rook', 'K':'king', 'Q':'queen'} #Used for text detailing the move that just occurred

board = [['bR','bN','bB','bQ','bK','bB','bN','bR'], #Empty spaces have to have characters in them because windows doesn't like the idea of a ghost image with spaces for names
         ['bP','bP','bP','bP','bP','bP','bP','bP'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['wP','wP','wP','wP','wP','wP','wP','wP'], 
         ['wR','wN','wB','wQ','wK','wB','wN','wR']]

#Below board was for testing
'''board = [['OO','OO','OO','OO','bK','OO','OO','OO'],
         ['OO','OO','bQ','OO','OO','bQ','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['OO','OO','OO','OO','OO','OO','OO','OO'], 
         ['wP','OO','OO','wP','OO','wP','OO','OO'], 
         ['OO','OO','OO','wR','wK','wR','OO','OO']]'''

buttons = [['','','','','','','',''], #Initialising array for buttons
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','','']]

#Global flags used in the program
castling = {'w':{'king':False, 'rook':{'L': False, 'R': False}}, 'b':{'king':False, 'rook':{'L': False, 'R': False}}} #Castling flags to see if something moved
selection = [False,0,0] #If it's live, row of selection, column of selection
turn = 'w'
promoting = False #If the program state should be 'promoting a last rank pawn' right now
kings = {'w':{'checked':False,'row':7,'col':4},'b':{'checked':False,'row':0,'col':4}} #If they're in check and their coordinates
#End of global flags

def drawBoard(dBoard): #Draws the board
    for y in range(8):
        for x in range(8): 
            if (y%2 == 0) == (x%2 == 0): #if (odd number, odd row) or (even number, even row) make it a white square
                piecePicture = PhotoImage(master=window,file=pieceDir+dBoard[x][y]+'.png', width=64, height=64) 
                buttons[x][y] = Button(window, bg=cfgColours['whiteSquare'], height=64, width=64, image=piecePicture, compound='c', relief='groove', command=lambda row=x, column=y : checkMoves(row,column))
                buttons[x][y].grid(row=x, column=y) #.grid() has to be on a seperate line don't question it idk either
                buttons[x][y].image = piecePicture #This stops garbage collection clearing the pictures (check the bototm of https://effbot.org/tkinterbook/photoimage.htm)
            else:
                piecePicture = PhotoImage(master=window,file=pieceDir+dBoard[x][y]+'.png', width=64, height=64) #Pictures are named same as pieces
                buttons[x][y] = Button(window, bg=cfgColours['blackSquare'], height=64, width=64, image=piecePicture, compound='c', relief='groove', command=lambda row=x, column=y : checkMoves(row,column))
                buttons[x][y].grid(row=x, column=y)
                buttons[x][y].image = piecePicture

def clearMoveOpts():
    for x in range(8):
        for y in range(8):
            if board[x][y][1] == 'K' and kings[board[x][y][0]]['checked']: #If this colour king is in check
                buttons[x][y].config(bg=cfgColours['inCheck'], relief='groove')
            elif (y%2 == 0) == (x%2 == 0): #Stop skim reading, if you read start to finish you'd understand this smh
                buttons[x][y].config(bg=cfgColours['whiteSquare'], relief='groove')
            else:
                buttons[x][y].config(bg=cfgColours['blackSquare'], relief='groove')

def updateTurn():
    global turn
    if turn == 'w':
        turn = 'b'
    else:
        turn = 'w'
    turnLabel()

def turnLabel():
    if turn == 'w':
        turnText.config(text='White\'s turn!')
    else:
        turnText.config(text='Black\'s turn!')

def createPromotionWindow(pieceColour,row,col):
    promoteWindow = Tk()

    promoteButtons = ['','','','']
    pieces = ['R','B','N','Q']

    promoteWindow.title('Piece selection')
    promoteWindowText = Label(promoteWindow, text='Choose a piece to promote to:', font=('',12))
    promoteWindowText.grid(columnspan = 4)

    for n in range(4): #Display the buttons for choosing a piece
        picture = PhotoImage(master=promoteWindow, file=(pieceDir+pieceColour+pieces[n]+'.png'), width=64, height=64)
        promoteButtons[n] = Button(promoteWindow, bg=cfgColours['whiteSquare'], height=64, width=64, image=picture, relief='groove', command = lambda popup = promoteWindow, piece=pieces[n], x=row, y=col : promotePawn(popup,piece,x,y))
        promoteButtons[n].grid(row=1,column=n)
        promoteButtons[n].image = picture #Referencing image again to stop garbage collection clearing it, read the note at the bottom https://effbot.org/tkinterbook/photoimage.htm

def promotePawn(window,piece,x,y):
    global promoting
    if x == 7:
        colour = 'b'
    else:
        colour = 'w'
    
    board[x][y] = colour+piece #Backend

    picture = PhotoImage(file=(pieceDir+board[x][y]+'.png'), height=64, width=64) #Frontend
    buttons[x][y].config(image=picture)
    buttons[x][y].image = picture

    log = chr(ord(str(y+1))+48) + str(8-(x+1)) + '=' + pieceChars[board[x][y]] #chr(ord... turns the row number into a letter by shifting along ascii table
    move = fullName[colour] + ' pawn promotes to ' + fullName[piece] + '.'
    history.config(text=history['text']+' '+log)
    moveText.config(text=move.capitalize())

    gameFinished = False     
    if turn == 'w' and verifyCheck(kings['b']['row'],kings['b']['col'],board) == True: #Did you check the enemy king?
        kings['b']['checked'] = True
        buttons[kings['b']['row']][kings['b']['col']].config(bg=cfgColours['inCheck']) #Updating global flags
        if verifyCheckMate(kings['b']['row'],kings['b']['col'],board) == True:
            moveText.config(text='Checkmate by white!')
            turnText.config(text='White wins!')
            gameFinished = True
        else:
            pass
    elif turn == 'b' and verifyCheck(kings['w']['row'],kings['w']['col'],board) == True:
        buttons[kings['w']['row']][kings['w']['col']].config(bg=cfgColours['inCheck'])
        kings['w']['checked'] = True
        if verifyCheckMate(kings['w']['row'],kings['w']['col'],board) == True:
            moveText.config(text='Checkmate by black!')
            turnText.config(text='Black wins!')
            gameFinished = True
        else:
            pass
    else:
        pass 

    window.destroy() #A selection has been made, the window must be destroyed
    promoting = False #Resume the game

def movePiece(row,col):
    board[row][col] = board[selection[1]][selection[2]] #Back end updating
    board[selection[1]][selection[2]] = 'OO'
    
    picture = PhotoImage(file=(pieceDir+board[row][col]+'.png'), height = 64, width=64)
    buttons[row][col].config(image=picture) #Front end updating
    buttons[row][col].image = picture

    picture = PhotoImage(file=(pieceDir+board[selection[1]][selection[2]]+'.png'), height = 64, width = 64)
    buttons[selection[1]][selection[2]].config(image=picture) #And now the empty space
    buttons[selection[1]][selection[2]].image = picture

def castle(row,col): #These are the ROOK's row and column
    global kings
    if col == 7: #King side Castling
        for x in range(1,3): #1,2
            testBoard = deepcopy(board)
            testBoard[row][col-x] = testBoard[row][col]
            testBoard[row][col] = 'OO'
            if verifyCheck(row,col-x,testBoard) == True:
                return False #Failed to castle because one of the intermediate spaces would place the king under check
        else:
            log = pieceChars[board[selection[1]][selection[2]]] + 'O-O'
            move = fullName[turn] + ' executes a kingside castle.'

            board[row][col-1] = board[row][col-3] #Moving king - back end
            board[row][col-3] = 'OO'
            castling[turn]['king'] = True
            kings[turn]['col'] = col-1 #Updating the king's position
            
            board[row][col-2] = board[row][col] #Moving rook - back end
            board[row][col] = 'OO'
            castling[turn]['rook']['R'] = True

            for x in range(4): #Updating board (front end)
                picture = PhotoImage(file=(pieceDir+board[row][col-x]+'.png'), height=64, width=64)
                buttons[row][col-x].config(image=picture)
                buttons[row][col-x].image = picture

            moveText.config(text=move)
            history.config(text=history['text']+log)
            return True
        
    else: #Queen side Castling, everything in same order
        for x in range(1,4): #1,2,3
            testBoard = deepcopy(board)
            testBoard[row][col+x] = testBoard[row][col]
            testBoard[row][col] = 'OO'
            if verifyCheck(row,col-x,testBoard) == True:
                return False #Failed to castle because one of the intermediate spaces would place the king under check
        else:
            log = pieceChars[board[selection[1]][selection[2]]] + 'O-O-O'
            move = fullName[turn] + ' executes a queenside castle.'

            board[row][col+2] = board[row][col+4]
            board[row][col+4] = 'OO'
            castling[turn]['king'] = True
            kings[turn]['col'] = col+2

            board[row][col+3] = board[row][col]
            board[row][col] = 'OO'
            castling[turn]['rook']['L'] = True

            for x in [0,2,3,4]: #The second column doesn't change in a queen side castle
                picture = PhotoImage(file=(pieceDir+board[row][col+x]+'.png'), height=64, width=64)
                buttons[row][col+x].config(image=picture)
                buttons[row][col+x].image = picture
        

    history.config(text=history['text'] + ' ' + log)
    moveText.config(text=move.capitalize())

def putsKingInCheck(row,col): #Checks if a move will cause the same player's king to be in check
    testBoard = deepcopy(board) #The move is tested on a copy of the board so that we don't have to undo it on the actual board if it fails
    testBoard[row][col] = testBoard[selection[1]][selection[2]] #Back end updating
    testBoard[selection[1]][selection[2]] = 'OO'
    
    if testBoard[row][col][1] == 'K': #This should run instead if you're e.g. moving your king out of check
        putsInCheck = verifyCheck(row,col,testBoard)
    else:
        putsInCheck = verifyCheck(kings[turn]['row'],kings[turn]['col'],testBoard)
    
    return putsInCheck #True or False

def checkMoves(row,col):
    global selection, castling, promoting, kings
    if promoting == True:
        pass
    elif buttons[row][col]['relief'] == 'groove' and buttons[row][col]['bg'] != cfgColours['moving'] and board[row][col] == 'OO':
        pass #If it's an empty, non highlighted space

    elif (buttons[row][col]['bg'] != cfgColours['attacking'] and turn != board[row][col][0]) and board[row][col] != 'OO':
        pass #If it's the wrong colour's piece and it isn't a potential attack target or default move

    elif buttons[row][col]['bg'] == cfgColours['moving'] or buttons[row][col]['bg'] == cfgColours['attacking']: #Attacking and moving
        if putsKingInCheck(row,col) == True: #If this move will put your king in check
            move = 'Your move can\'t put your king in check!'
            moveText.config(text=move)
        else:
            kings[turn]['checked'] = False #In the case that you did just move the king out of check
            
            if (board[selection[1]][selection[2]] == 'bP' and row == 7) or (board[selection[1]][selection[2]] == 'wP' and row == 0): #Checking for pre-final rank pawn as the move hasn't been executed yet
                createPromotionWindow(turn,row,col)
                promoting = True
                #The move log is created within the promoting functions
            else:
                if buttons[row][col]['bg'] == cfgColours['moving']: #Log text, \/ this converts the column number into its respective character
                    log = pieceChars[board[selection[1]][selection[2]]] + chr(ord(str(col+1))+48) + str(8-(row+1)) #Actual chess coordinates start at the bottom
                    move = fullName[turn]+' '+fullName[board[selection[1]][selection[2]][1]]+' '+'moves to'+' '+chr(ord(str(col+1))+48) + str(8-(row+1)) + '.'
                else: #If it's a capture
                    log = pieceChars[board[selection[1]][selection[2]]] + 'x' + chr(ord(str(col+1))+48) + str(8-(row+1))
                    move = fullName[turn]+' '+fullName[board[selection[1]][selection[2]][1]]+' '+'captures'+' '+fullName[board[row][col][0]]+' '+fullName[board[row][col][1]] + '.'
                
                history.config(text=history['text']+' '+log)
                moveText.config(text=move.capitalize())
            
            movePiece(row,col) #Executes the move, from now we use row, col to reference the piece's coordinates rather than selection[1], selection[2]

            if castling[turn]['king'] == False and board[row][col][1] == 'K': #Castling flag updating if anything relevant moved
                castling[turn]['king'] = True
            elif castling[turn]['rook']['L'] == False and board[row][col][1] == 'R' and col == 0:
                castling[turn]['rook']['L'] = True 
            elif castling[turn]['rook']['R'] == False and board[row][col][1] == 'R' and col == 7:
                castling[turn]['rook']['R'] = True
            else:
                pass
            
            if board[row][col][1] == 'K': #Updating king's position if he moved
                kings[turn]['row'] = row
                kings[turn]['col'] = col
            else:
                pass

            gameFinished = False     
            if turn == 'w' and verifyCheck(kings['b']['row'],kings['b']['col'],board) == True: #Did you check the enemy king?
                kings['b']['checked'] = True
                buttons[kings['b']['row']][kings['b']['col']].config(bg=cfgColours['inCheck'])
                if verifyCheckMate(kings['b']['row'],kings['b']['col'],board) == True:
                    moveText.config(text='Checkmate by white!')
                    turnText.config(text='White wins!')
                    gameFinished = True
                else:
                    pass
            elif turn == 'b' and verifyCheck(kings['w']['row'],kings['w']['col'],board) == True:
                buttons[kings['w']['row']][kings['w']['col']].config(bg=cfgColours['inCheck'])
                kings['w']['checked'] = True
                if verifyCheckMate(kings['w']['row'],kings['w']['col'],board) == True:
                    moveText.config(text='Checkmate by black!')
                    turnText.config(text='Black wins!')
                    gameFinished = True
                else:
                    pass
            else:
                pass 

            clearMoveOpts()
            selection[0] = False

            if gameFinished == True:
                promoting = True
            else:
                updateTurn()
        
    elif buttons[row][col]['bg'] == cfgColours['castling']: #Castling - array referencing from the chosen rook's perspective
        if castle(row, col) == False: #The function itself castles, surprising I know; move log in function; the function returns wether it succeeded
            move = 'You cannot castle this way as one of the intermediate spaces would put the king in check.'
            moveText.config(text=move)
        else: #This runs only if castle didn't return False (so it succeeded)
            clearMoveOpts()
            updateTurn()
            selection[0] = False

    elif buttons[row][col]['relief'] == 'groove': #If unselected piece
        clearMoveOpts()
        buttons[row][col].config(bg=cfgColours['selected'], relief='sunken')
        if board[row][col][1] == 'P': #Pawn
            pawnMoves(row,col)
        elif board[row][col][1] == 'R': #Non directional pieces
            rookMoves(row,col)
        elif board[row][col][1] == 'B':
            bishopMoves(row,col)
        elif board[row][col][1] == 'K':
            kingMoves(row,col)
        elif board[row][col][1] == 'Q': #She's just a combination of the two
            rookMoves(row,col)
            bishopMoves(row,col)
        elif board[row][col][1] == 'N':
            knightMoves(row,col)
        else:
            pass
        selection = [True,row,col] #Now move selection is live
        
    else: #If selected
        if buttons[row][col]['bg'] == cfgColours['selected']:
            clearMoveOpts()
        else:
            pass
        selection[0] = False #Selection is no longer live

def pawnMoves(row,col):
    moves = pawnLocations(row,col,board) #Only empty or enemy piece containing coordinates are returned
    for move in moves:
        if board[move[0]][move[1]] == 'OO': #If empty space
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else: #Then it must be an enemy piece
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])

def rookMoves(row,col):
    moves = rookLocations(row,col,board)
    for move in moves:
        if board[move[0]][move[1]] == 'OO':
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])

def bishopMoves(row,col):
    moves = bishopLocations(row,col,board)
    for move in moves:
        if board[move[0]][move[1]] == 'OO': 
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])

def queenMoves(row,col):
    moves = queenLocations(row,col,board)
    for move in moves:
        if board[move[0]][move[1]] == 'OO':
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])

def kingMoves(row,col):
    moves = kingLocations(row,col,board)
    for move in moves:
        if board[move[0]][move[1]] == 'OO':
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])

    if (castling[turn]['king'] == False and castling[turn]['rook']['R'] == False) and (board[row][col+1] == 'OO' and board[row][col+2] == 'OO'):
        buttons[row][col+3].config(bg=cfgColours['castling'])
    else: #This is for the King side
        pass
    
    if (castling[turn]['king'] == False and castling[turn]['rook']['L'] == False) and (board[row][col-1] == 'OO' and board[row][col-2] == 'OO' and board[row][col-3] == 'OO'):
        buttons[row][col-4].config(bg=cfgColours['castling'])
    else: #This is for the Queen side
        pass
    
def knightMoves(row,col):
    moves = knightLocations(row,col,board)
    for move in moves:
        if board[move[0]][move[1]] == 'OO':
            buttons[move[0]][move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[move[0]][move[1]].config(bg=cfgColours['attacking'])
        

drawBoard(board)
window.title('Chess is cooler than reports v1.3')
turnText = Label(window, text='White\'s turn!', font=('Century Gothic',16))
turnText.grid(columnspan = 8)

#wraplength Wraps text to next line when in excess of that many pixels
moveText = Label(window,text='Make the first move.', font=('Century Gothic',10), wraplength=550)
moveText.grid(columnspan = 8)

history = Label(window,text='', font=('Century Gothic',12), wraplength=200)
history.grid(rowspan=8, columnspan=1, column=8, row=0)

window.geometry("760x646+130+130") #width x height + xoffset + yoffset (from top left of screen)
window.mainloop()
    

