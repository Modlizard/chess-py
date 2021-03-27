def verifyCheckButShit(row,col,vBoard): #Row and column coordinates of the king that should be in check
    if row > col: #/\ < 
        boardLimit = col #bottom left of board
    else:
        boardLimit = row
    if vBoard[row][col][0] == 'w'  and vBoard[row-1][col-1] == 'bP': #For black pawns
        return True
    else:
        pass
    for x in range(1,boardLimit+1): 
        if (vBoard[row-x][col-x][1] == 'B' or vBoard[row-x][col-x][1] == 'Q') and (vBoard[row-x][col-x][0] != vBoard[row][col][0]): #For bishops and queens
            return True
        elif vBoard[row-x][col-x] != '  ':
            break
        else:
            pass

    if row > 7-col: #\/ <
        boardLimit = 7-row #bottom right of board
    else:
        boardLimit = col
    if vBoard[row][col][0] == 'b'  and vBoard[row+1][col-1] == 'wP': #For white pawns
        return True
    else:
        pass
    for x in range(1,boardLimit+1):
        if (vBoard[row+x][col-x][1] == 'B' or vBoard[row+x][col-x][1] == 'Q') and (vBoard[row+x][col-x][0] != vBoard[row][col][0]): #For bishops and queens
            return True
        elif vBoard[row+x][col-x] != '  ':
            break
        else:
            pass
    
    if row > col: #\/ >
        boardLimit = 7-row #bottom left of board
    else:
        boardLimit = 7-col
    if vBoard[row][col][0] == 'b'  and vBoard[row+1][col+1] == 'wP': #For white pawns
        return True
    else:
        pass
    for x in range(1,boardLimit+1):
        if (vBoard[row+x][col+x][1] == 'B' or vBoard[row+x][col+x][1] == 'Q') and (vBoard[row+x][col+x][0] != vBoard[row][col][0]): #For bishops and queens
            return True
        elif vBoard[row+x][col+x] != '  ':
            break
        else:
            pass

    if row > 7-col: #/\ >
        boardLimit = 7-col #bottom right of board
    else:
        boardLimit = row
    if vBoard[row][col][0] == 'w'  and vBoard[row-1][col+1] == 'bP': #For black pawns
        return True
    else:
        pass
    for x in range(1,boardLimit+1):
        if (vBoard[row-x][col+x][1] == 'B' or vBoard[row-x][col+x][1] == 'Q') and (vBoard[row-x][col+x][0] != vBoard[row][col][0]): #For bishops and queens
            return True
        elif vBoard[row-x][col+x] != '  ':
            break
        else:
            pass
    
    for x in range(row)[::-1]: # /\ check direction, 0 to current position minus one space but check begins at piece so the array is reversed
        if (vBoard[x][col][1] == 'R' or vBoard[x][col][1] == 'Q') and (vBoard[x][col][0] != vBoard[row][col][0]): #If opposite colour rook or queen
            return True
        elif vBoard[x][col] != '  ':
            break
        else:
            pass
            
    for x in range(row+1, 8): #\/ check direction
        if (vBoard[x][col][1] == 'R' or vBoard[x][col][1] == 'Q') and (vBoard[x][col][0] != vBoard[row][col][0]): #If opposite colour rook or queen
            return True
        elif vBoard[x][col] != '  ':
            break
        else:
            pass
            
    for x in range(col)[::-1]: #< check direction
        if (vBoard[row][x][1] == 'R' or vBoard[row][x][1] == 'Q') and (vBoard[row][x][0] != vBoard[row][col][0]): #If opposite colour rook or queen
            return True
        elif vBoard[row][x] != '  ':
            break
        else:
            pass
            
    for x in range(col+1, 8): #> check direction
        if (vBoard[row][x][1] == 'R' or vBoard[row][x][1] == 'Q') and (vBoard[row][x][0] != vBoard[row][col][0]): #If opposite colour rook or queen
            return True
        elif vBoard[row][x] != '  ':
            break
        else:
            pass


    kingMoveset = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    for move in kingMoveset:
        if (row+move[0] < 0 or row+move[0] > 7) or (col+move[1] < 0 or col+move[1] > 7): #If either out of board range 
            pass
        elif vBoard[row+move[0]][col+move[1]][1] == 'K' and vBoard[row][col][0] != vBoard[row+move[0]][col+move[1]][0]: #If opposite colour king
            return True
        else:
            pass
    
    knightMoveset = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]
    for move in knightMoveset:
        if (row+move[0] < 0 or row+move[0] > 7) or (col+move[1] < 0 or col+move[1] > 7): #If either out of board range 
            pass
        elif vBoard[row+move[0]][col+move[1]][1] == 'N' and vBoard[row][col][0] != vBoard[row+move[0]][col+move[1]][0]: #If opposite colour knight
            return True
        else:
            pass
    return False
