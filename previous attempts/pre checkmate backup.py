import os
import json
from tkinter import *
from verifier import verifyCheck #Custom module because the check validation function was too
from copy import deepcopy

window=Tk()
pieceDir = os.path.dirname(os.path.realpath(__file__))+'\pieces\\' #Filepath uses paths instead of getcwd() because other IDE's often change the cwd

with open(os.path.dirname(os.path.realpath(__file__))+'\config.json','r') as settingsFile: #Loads the board colours config
    cfgColours = json.load(settingsFile)

pieceChars = {'wP':'♙','wN':'♘','wB':'♗','wR':'♖','wK':'♔','wQ':'♕',
              'bP':'♟','bN':'♞','bB':'♝','bR':'♜','bK':'♚','bQ':'♛'}
fullName = {'w': 'white', 'b': 'black', 'P':'pawn', 'N':'knight', 'B':'bipshop', 'R':'rook', 'K':'king', 'Q':'queen'}

board = [['bR','bN','bB','bQ','bK','bB','bN','bR'], 
         ['bP','bP','bP','bP','bP','bP','bP','bP'], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['wP','wP','wP','wP','wP','wP','wP','wP'], 
         ['wR','wN','wB','wQ','wK','wB','wN','wR']]

'''board = [['  ','  ','  ','  ','bK','  ','  ','  '], 
         ['  ','  ','bQ','  ','  ','  ','  ','  '], 
         ['wR','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['bR','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','wQ','  ','  '], 
         ['wR','  ','  ','  ','wK','  ','  ','  ']]'''

buttons = [['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','',''],
           ['','','','','','','','']]

#Global flags used in the program
castling = {'w':{'king':False, 'rook':{'L': False, 'R': False}}, 'b':{'king':False, 'rook':{'L': False, 'R': False}}} #Castling flags to see if something moved
selection = [False,0,0] #If it's live, x co-ord of selection, y co-ord of selection
turn = 'w'
promoting = False #If the program should be promoting a last rank pawn right now
kings = {'w':{'checked':False,'row':7,'col':4},'b':{'checked':False,'row':0,'col':4}} #If they're in check and their coordinates
#End of global flags

def dispBoard(dBoard):
    for y in range(8):
        for x in range(8): #BUTTONS ARE ACTUALLY 58 NOT 50 PIXELS BECAUSE IDFK
            if (y%2 == 0) == (x%2 == 0): #if (odd number, odd row) or (even number, even row) make it a white square
                piecePicture = PhotoImage(master=window,file=pieceDir+dBoard[x][y]+'.png', width=64, height=64)
                buttons[x][y] = Button(window, bg=cfgColours['whiteSquare'], height=64, width=64, image=piecePicture, compound='c', relief='groove', command=lambda row=x, column=y : checkMoves(row,column))
                buttons[x][y].grid(row=x, column=y) #.grid() has to be seperate don't question it idk either
                buttons[x][y].image = piecePicture #This stops garbage collection clearing the pictures
            else:
                piecePicture = PhotoImage(master=window,file=pieceDir+dBoard[x][y]+'.png', width=64, height=64)
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
        promoteButtons[n].image = picture

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

    log = chr(ord(str(y+1))+48) + str(8-(x+1)) + '=' + pieceChars[board[x][y]]
    move = fullName[colour] + ' pawn promotes to ' + fullName[piece] + '.'
    history.config(text=history['text']+' '+log)
    moveText.config(text=move.capitalize())

    window.destroy() #A selection has been made, the window must be destroyed
    promoting = False #Resume the game

def movePiece(row,col):
    board[row][col] = board[selection[1]][selection[2]] #Back end updating
    board[selection[1]][selection[2]] = '  '
    
    picture = PhotoImage(file=(pieceDir+board[row][col]+'.png'), height = 64, width=64)
    buttons[row][col].config(image=picture) #Front end updating
    buttons[row][col].image = picture

    picture = PhotoImage(file=(pieceDir+board[selection[1]][selection[2]]+'.png'), height = 64, width = 64)
    buttons[selection[1]][selection[2]].config(image=picture)
    buttons[selection[1]][selection[2]].image = picture

def castle(row,col):
    global kings
    if col == 7: #King side Castling
        if verifyCheck(row,col-1,board) == True or verifyCheck(row,col-2,board) == True:
            return False #Failed to castle because one of the intermediate spaces would place the king under check
        else:
            log = pieceChars[board[selection[1]][selection[2]]] + 'O-O'
            move = fullName[turn] + ' executes a kingside castle.'

            board[row][col-1] = board[row][col-3] #Moving king - back end
            board[row][col-3] = '  '
            castling[turn]['king'] = True
            kings[turn]['col'] = col-1 #Updating the king's position
            
            board[row][col-2] = board[row][col] #Moving rook - back end
            board[row][col] = '  '
            castling[turn]['rook']['R'] = True

            for x in range(4): #Updating board (front end)
                picture = PhotoImage(file=(pieceDir+board[row][col-x]+'.png'), height=64, width=64)
                buttons[row][col-x].config(image=picture)
                buttons[row][col-x].image = picture
            return True
        
    else: #Queen side Castling, everything in same order
        if verifyCheck(row,col+1,board) == True or verifyCheck(row,col+2,board) == True or verifyCheck(row,col+3,board) == True:
            return False #Failed to castle because one of the intermediate spaces would place the king under check
        else:
            log = pieceChars[board[selection[1]][selection[2]]] + 'O-O-O'
            move = fullName[turn] + ' executes a queenside castle.'

            board[row][col+2] = board[row][col+4]
            board[row][col+4] = '  '
            castling[turn]['king'] = True
            kings[turn]['col'] = col+2

            board[row][col+3] = board[row][col]
            board[row][col] = '  '
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
    testBoard[selection[1]][selection[2]] = '  '
    
    if testBoard[row][col][1] == 'K': #This should run instead if you're e.g. moving your king out of check
        putsInCheck = verifyCheck(row,col,testBoard)
    else:
        putsInCheck = verifyCheck(kings[turn]['row'],kings[turn]['col'],testBoard)
    
    return putsInCheck #True or False

def checkMoves(row,col):
    global selection, castling, promoting, kings
    if promoting == True:
        pass
    elif buttons[row][col]['relief'] == 'groove' and buttons[row][col]['bg'] != cfgColours['moving'] and board[row][col] == '  ':
        pass #If it's an empty, non highlighted space

    elif (buttons[row][col]['bg'] != cfgColours['attacking'] and turn != board[row][col][0]) and board[row][col] != '  ':
        pass #If it's the wrong colour's piece and it isn't a potential attack target or default move

    elif buttons[row][col]['bg'] == cfgColours['moving'] or buttons[row][col]['bg'] == cfgColours['attacking']: #Attacking and moving
        if putsKingInCheck(row,col) == True: #If this move will put your king in check
            move = 'Your king is in check and must be protected before you can make a different move!'
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

            if turn == 'w' and verifyCheck(kings['b']['row'],kings['b']['col'],board) == True: #Did you check the enemy king?
                kings['b']['checked'] = True
                buttons[kings['b']['row']][kings['b']['col']].config(bg=cfgColours['inCheck'])
            elif turn == 'b' and verifyCheck(kings['w']['row'],kings['w']['col'],board) == True:
                buttons[kings['w']['row']][kings['w']['col']].config(bg=cfgColours['inCheck'])
                kings['w']['checked'] = True
            else:
                pass 

            clearMoveOpts()
            selection[0] = False
            
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
        if board[row][col] == 'wP': #White pawn
            pawnMoves(row,col,'w')
        elif board[row][col] == 'bP': #Black pawn
            pawnMoves(row,col,'b')
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

def pawnMoves(row,col,colour):
    if row+1 < 8 and colour == 'b': #First statement avoids index out of range bs because imagine making an extra if statement #Move higlighting
        if board[row+1][col] == '  ':
            buttons[row+1][col].config(bg=cfgColours['moving'])
            if row == 1 and board[row+2][col] == '  ':
                buttons[row+2][col].config(bg=cfgColours['moving'])
            else:
                pass
        else:
            pass
        
        if col-1 > -1 and board[row+1][col-1][0] == 'w': #If opposite colour piece
            buttons[row+1][col-1].config(bg=cfgColours['attacking'])
        else:
            pass
        
        if col+1 < 8 and board[row+1][col+1][0] == 'w':
            buttons[row+1][col+1].config(bg=cfgColours['attacking'])
        else:
            pass
        
    elif row-1 > -1 and colour == 'w':
        if board[row-1][col] == '  ':
            buttons[row-1][col].config(bg=cfgColours['moving'])
            if row == 6 and board[row-2][col] == '  ':
                buttons[row-2][col].config(bg=cfgColours['moving'])
            else:
                pass
        else:
            pass
        if col-1 > -1 and board[row-1][col-1][0] == 'b':
            buttons[row-1][col-1].config(bg=cfgColours['attacking'])
        else:
            pass
        
        if col+1 < 8 and board[row-1][col+1][0] == 'b':
            buttons[row-1][col+1].config(bg=cfgColours['attacking'])
        else:
            pass
    else:
        pass

def rookMoves(row,col):
    for x in range(row)[::-1]: # /\ check direction, 0 to current position minus one space but check begins at piece so the array is reversed
        if board[x][col] != '  ': #If piece in the way (current pos minus one space because current pos has the piece itself which would trigger this)
            if board[row][col][0] == board[x][col][0]: #If same colour
                pass
            else: 
                buttons[x][col].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[x][col].config(bg=cfgColours['moving'])
            
    for x in range(row+1, 8): #\/ check direction
        if board[x][col] != '  ':
            if board[row][col][0] == board[x][col][0]:
                pass
            else:
                buttons[x][col].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[x][col].config(bg=cfgColours['moving'])
            
    for x in range(col)[::-1]:
        if board[row][x] != '  ':
            if board[row][col][0] == board[row][x][0]:
                pass
            else:
                buttons[row][x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row][x].config(bg=cfgColours['moving'])
            
    for x in range(col+1, 8):
        if board[row][x] != '  ':
            if board[row][col][0] == board[row][x][0]:
                pass
            else:
                buttons[row][x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row][x].config(bg=cfgColours['moving'])

def bishopMoves(row,col):
    if row > col: #/\ < 
        boardLimit = col #bottom left of board
    else:
        boardLimit = row
    for x in range(1,boardLimit+1): 
        if board[row-x][col-x] != '  ': #If something is in that space
            if board[row][col][0] == board[row-x][col-x][0]: #If same colour
                pass
            else:
                buttons[row-x][col-x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row-x][col-x].config(bg=cfgColours['moving'])

    if row > 7-col: #\/ <
        boardLimit = 7-row #bottom right of board
    else:
        boardLimit = col
    for x in range(1,boardLimit+1):
        if board[row+x][col-x] != '  ':
            if board[row][col][0] == board[row+x][col-x][0]:
                pass
            else:
                buttons[row+x][col-x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row+x][col-x].config(bg=cfgColours['moving'])
    
    if row > col: #\/ >
        boardLimit = 7-row #bottom left of board
    else:
        boardLimit = 7-col
    for x in range(1,boardLimit+1):
        if board[row+x][col+x] != '  ':
            if board[row][col][0] == board[row+x][col+x][0]:
                pass
            else:
                buttons[row+x][col+x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row+x][col+x].config(bg=cfgColours['moving'])

    if row > 7-col: #/\ >
        boardLimit = 7-col #bottom right of board
    else:
        boardLimit = row
    for x in range(1,boardLimit+1):
        if board[row-x][col+x] != '  ':
            if board[row][col][0] == board[row-x][col+x][0]:
                pass
            else:
                buttons[row-x][col+x].config(bg=cfgColours['attacking'])
            break
        else:
            buttons[row-x][col+x].config(bg=cfgColours['moving'])

def highlightMoveset(row,col,moveset):
    for move in moveset:
        if (row+move[0] < 0 or row+move[0] > 7) or (col+move[1] < 0 or col+move[1] > 7): #If either out of board range 
            pass
        elif board[row][col][0] == board[row+move[0]][col+move[1]][0]: #If same colour piece
            pass
        elif board[row+move[0]][col+move[1]] == '  ':
            buttons[row+move[0]][col+move[1]].config(bg=cfgColours['moving'])
        else:
            buttons[row+move[0]][col+move[1]].config(bg=cfgColours['attacking'])

def kingMoves(row,col):
    moveset = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #King moveset
    highlightMoveset(row,col,moveset)
    
    if (castling[turn]['king'] == False and castling[turn]['rook']['R'] == False) and (board[row][col+1] == '  ' and board[row][col+2] == '  '):
        buttons[row][col+3].config(bg=cfgColours['castling'])
    else: #This is for the King side
        pass
    
    if (castling[turn]['king'] == False and castling[turn]['rook']['L'] == False) and (board[row][col-1] == '  ' and board[row][col-2] == '  ' and board[row][col-3] == '  '):
        buttons[row][col-4].config(bg=cfgColours['castling'])
    else: #This is for the Queen side
        pass
    
def knightMoves(row,col):
    moveset = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]] #Knight moveset
    highlightMoveset(row,col,moveset)

def turnLabel():
    if turn == 'w':
        turnText.config(text='White\'s turn!')
    else:
        turnText.config(text='Black\'s turn!')

dispBoard(board)
window.title('AI is for noobs v1.69')
turnText = Label(window, text='White\'s turn!', font=('Century Gothic',16))
turnText.grid(columnspan = 8)
moveText = Label(window,text='Make the first move.', font=('Century Gothic',10), wraplength=550)
moveText.grid(columnspan = 8)
history = Label(window,text='', font=('Century Gothic',12), wraplength=200)
history.grid(rowspan=8, columnspan=1, column=8, row=0)
window.geometry("760x646+130+130") #width x height + xoffset + yoffset #Added 42 to height for n text label lines

window.mainloop()# add widgets here whatever that means idk ._.
