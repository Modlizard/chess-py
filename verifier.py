from copy import deepcopy

def pawnLocations(row,col,vBoard): #Returns an array of all potential pawn move coordinates
    locations = []
    colour = vBoard[row][col][0]
    if row+1 < 8 and colour == 'b': #First statement avoids index out of range bs because imagine making an extra if statement
        if vBoard[row+1][col] == 'OO':
            locations.append([row+1,col])
            if row == 1 and vBoard[row+2][col] == 'OO': #First pawn move can go two spaces, this checks for it
                locations.append([row+2,col])
            else:
                pass
        else:
            pass
        
        if col-1 > -1 and vBoard[row+1][col-1][0] == 'w': #If opposite colour piece and diagonal
            locations.append([row+1,col-1])
        else:
            pass
        
        if col+1 < 8 and vBoard[row+1][col+1][0] == 'w':
            locations.append([row+1,col+1])
        else:
            pass

    elif row-1 > -1 and colour == 'w':
        if vBoard[row-1][col] == 'OO':
            locations.append([row-1,col])
            if row == 6 and vBoard[row-2][col] == 'OO':
                locations.append([row-2,col])
            else:
                pass
        else:
            pass
        if col-1 > -1 and vBoard[row-1][col-1][0] == 'b':
            locations.append([row-1,col-1])
        else:
            pass
        
        if col+1 < 8 and vBoard[row-1][col+1][0] == 'b':
            locations.append([row-1,col+1])
        else:
            pass
    else:
        pass
    return locations

def rookLocations(row,col,vBoard): #As above, returns array of potential rook move coordinates
    locations = []
    for x in range(row)[::-1]: # /\ check direction, 0 to current position minus one space but check begins at piece so the array is reversed
        if vBoard[x][col] != 'OO': #If piece in the way (^ current pos minus one space because current pos has the piece itself which would trigger this)
            if vBoard[row][col][0] == vBoard[x][col][0]: #If same colour
                pass
            else: 
                locations.append([x,col])
            break #Collision was made with a piece
        else:
            locations.append([x,col])
            
    for x in range(row+1, 8): #\/ check direction
        if vBoard[x][col] != 'OO':
            if vBoard[row][col][0] == vBoard[x][col][0]:
                pass
            else:
                locations.append([x,col])
            break
        else:
            locations.append([x,col])
            
    for x in range(col)[::-1]:
        if vBoard[row][x] != 'OO':
            if vBoard[row][col][0] == vBoard[row][x][0]:
                pass
            else:
                locations.append([row,x])
            break
        else:
            locations.append([row,x])
    
    for x in range(col+1, 8):
        if vBoard[row][x] != 'OO':
            if vBoard[row][col][0] == vBoard[row][x][0]:
                pass
            else:
                locations.append([row,x])
            break
        else:
            locations.append([row,x])
    return locations

def bishopLocations(row,col,vBoard):
    locations = []
    if row > col: #/\ < #This splits the board diagonally to determine if the rows left or columns left limit the potential spaces in that direction
        boardLimit = col #bottom left of board
    else:
        boardLimit = row
    for x in range(1,boardLimit+1): 
        if vBoard[row-x][col-x] != 'OO': #If something is in that space
            if vBoard[row][col][0] == vBoard[row-x][col-x][0]: #If same colour
                pass
            else: #If it's a different colour piece
                locations.append([row-x,col-x])
            break
        else:
            locations.append([row-x,col-x])

    if row > 7-col: #\/ <
        boardLimit = 7-row #bottom right of board
    else:
        boardLimit = col
    for x in range(1,boardLimit+1):
        if vBoard[row+x][col-x] != 'OO':
            if vBoard[row][col][0] == vBoard[row+x][col-x][0]:
                pass
            else:
                locations.append([row+x,col-x])
            break
        else:
            locations.append([row+x,col-x])
    
    if row > col: #\/ >
        boardLimit = 7-row #bottom left of board
    else:
        boardLimit = 7-col
    for x in range(1,boardLimit+1):
        if vBoard[row+x][col+x] != 'OO':
            if vBoard[row][col][0] == vBoard[row+x][col+x][0]:
                pass
            else:
                locations.append([row+x,col+x])
            break
        else:
            locations.append([row+x,col+x])

    if row > 7-col: #/\ >
        boardLimit = 7-col #bottom right of board
    else:
        boardLimit = row
    for x in range(1,boardLimit+1):
        if vBoard[row-x][col+x] != 'OO':
            if vBoard[row][col][0] == vBoard[row-x][col+x][0]:
                pass
            else:
                locations.append([row-x,col+x])
            break
        else:
            locations.append([row-x,col+x])
    return locations
    
def queenLocations(row,col,vBoard):
    locations = []
    for location in (rookLocations(row,col,vBoard)):
        locations.append(location)
    for location in (bishopLocations(row,col,vBoard)):
        locations.append(location)
    return locations

def knightLocations(row,col,vBoard):
    locations = []
    offsets = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]] #Knight move offsets
    for offset in offsets:
        if (row+offset[0] < 0 or row+offset[0] > 7) or (col+offset[1] < 0 or col+offset[1] > 7): #If either calculated coordinate out of board range 
            pass
        elif vBoard[row][col][0] == vBoard[row+offset[0]][col+offset[1]][0]: #If same colour piece
            pass
        else: #Valid move that's on the board targetting an empty space or enemy piece
            locations.append([row+offset[0],col+offset[1]])
    return locations

def kingLocations(row,col,vBoard):
    locations = []
    offsets = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #King move offsets
    for offset in offsets: #Coord as in co-ordinate
        if (row+offset[0] < 0 or row+offset[0] > 7) or (col+offset[1] < 0 or col+offset[1] > 7): #If either out of board range 
            pass
        elif vBoard[row][col][0] == vBoard[row+offset[0]][col+offset[1]][0]: #If same colour piece
            pass
        else:
            locations.append([row+offset[0],col+offset[1]])
    return locations

def verifyCheck(row,col,vBoard): #Row and column coordinates of the king that should be in check
    for move in pawnLocations(row,col,vBoard):
        if vBoard[move[0]][move[1]][1] == 'P': #If the king can take using the pawn's path then the enemy pawn can take the king
            return True #King is in check, no further tests required
        else:
            pass
    for move in bishopLocations(row,col,vBoard): #Same principle as above etc.
        if vBoard[move[0]][move[1]][1] == 'B' or vBoard[move[0]][move[1]][1] == 'Q':
            return True
        else:
            pass
    for move in rookLocations(row,col,vBoard):
        if vBoard[move[0]][move[1]][1] == 'R' or vBoard[move[0]][move[1]][1] == 'Q':
            return True
        else:
            pass
    for move in knightLocations(row,col,vBoard):
        if vBoard[move[0]][move[1]][1] == 'N':
            return True
        else:
            pass
    for move in kingLocations(row,col,vBoard):
        if vBoard[move[0]][move[1]][1] == 'K':
            return True
        else:
            pass
    return False

def verifyCheckMate(kingRow,kingCol,vBoard): #Row and column coordinates for the king that should be in check mate
    colour = vBoard[kingRow][kingCol][0]
    for row in range(8):
        for col in range(8):
            if vBoard[row][col] == 'OO' or vBoard[row][col][0] != colour:
                pass
            else:
                if vBoard[row][col][1] == 'P':
                    moves = pawnLocations(row,col,vBoard)
                elif vBoard[row][col][1] == 'R':
                    moves = rookLocations(row,col,vBoard)
                elif vBoard[row][col][1] == 'B':
                    moves = bishopLocations(row,col,vBoard)
                elif vBoard[row][col][1] == 'Q':
                    moves = queenLocations(row,col,vBoard)
                elif vBoard[row][col][1] == 'N':
                    moves = knightLocations(row,col,vBoard)
                else: #If king
                    moves = kingLocations(row,col,vBoard)
                for move in moves:
                    testBoard = deepcopy(vBoard)
                    testBoard[move[0]][move[1]] = testBoard[row][col]
                    testBoard[row][col] = 'OO'

                    if vBoard[row][col][1] == 'K': #If you're moving the king himself then the king's coordinates obviously have to be updated.
                        kingRow = move[0]
                        kingCol = move[1]
                    else:
                        pass

                    if verifyCheck(kingRow,kingCol,testBoard) == False:
                        return False #There is a way out of checkmate
                    else:
                        pass
    return True #If there isn't a single check mate = False scenario then it is a checkmate
