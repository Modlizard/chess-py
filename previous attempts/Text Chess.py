# chessHelp.py 

# 

# this program displays a chess board and then asks players 

# in turn to enter moves for their pieces 

# the program then updates the board to show their move 

# 

# BH - 11/10/20 

# 

  

board = [['bR','bk','bB','bQ','bK','bB','bk','bR'], 
         ['bP','bP','bP','bP','bP','bP','bP','bP'], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['  ','  ','  ','  ','  ','  ','  ','  '], 
         ['wP','wP','wP','wP','wP','wP','wP','wP'], 
         ['wR','wk','wB','wQ','wK','wB','wk','wR']] 

letters = {'A': 0,'B': 1,'C': 2,'D': 3,'E': 4,'F': 5,'G': 6,'H': 7} 

def displayBoard(aBoard): 
    print("     A    B    C    D    E    F    G    H   ") 
    print("   |---------------------------------------|") 
    for row in range(8): 
        for col in range(8):   
            if col == 0: 
                print(' '+str(row+1)+' | '+board[row][col]+' | ', end='') 
            else: 
                print(board[row][col]+' | ', end='') 
        print() 
        print("   |---------------------------------------|")   

def enterMove(aPlayer): 
    move = input("Please enter "+aPlayer+" move (XX YY) : ") 
    return move   

def applyMove(aMove,aPlayer,theBoard): 
    aMove = aMove.split(' ') 
    theBoard[int(aMove[1][1])-1][letters[aMove[1][0]]] = theBoard[int(aMove[0][1])-1][letters[aMove[0][0]]] 
    theBoard[int(aMove[0][1])-1][letters[aMove[0][0]]] = '  ' 
    return True,theBoard 

player = 'white' 
while True: 
    displayBoard(board)   
    successful = False 

    while not successful: 
        move = enterMove(player) 
        successful,board = applyMove(move, player, board) 

    if player == 'white': 
        player = 'black' 
    else: 
        player = 'white' 
