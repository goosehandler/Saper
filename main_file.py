import random
import pickle
import sys

def takeNeighbors(GRID, x, y):
    GRID_L = len(GRID[0])
    GRID_W = len(GRID)
    if x == 1 and y == 1:
        data = [[0, 1], [1, 0], [1, 1]]
    elif x == GRID_L and y == GRID_W:
        data = [[GRID_W-2, GRID_L-2], [GRID_W-1, GRID_L-2], [GRID_W-2, GRID_L-1]]
    elif x == 1 and y == GRID_W:
        data = [[GRID_W-2, 0], [GRID_W-2, 1], [GRID_W-1, 1]]
    elif x == GRID_L and y == 1:
        data = [[0, GRID_L-2], [1, GRID_L-2], [1, GRID_L-1]]
    elif x == 1:
        data = [[y-2, 0], [y-2, 1], [y-1, 1], [y, 0], [y, 1]]
    elif y == 1:
        data = [[0, x-2], [0, x], [1, x-2], [1, x-1], [1, x]]
    elif x == GRID_L:
        data = [[y-2, GRID_L-2], [y-2, GRID_L-1], [y-1, GRID_L-2], [y, GRID_L-2], [y, GRID_L-1]]
    elif y == GRID_W:
        data = [[GRID_W-2, x-2], [GRID_W-2, x-1], [GRID_W-2, x], [GRID_W-1, x-2], [GRID_W-1, x]]
    else:
        data = [[y-2, x-2], [y-2, x-1], [y-2, x], [y-1, x-2], [y-1, x], [y, x-2], [y, x-1], [y, x]]
    return data


def countMines(GRID, data):
    count = 0
    for i in data:
        if GRID[i[0]][i[1]] == -1:
            count += 1
    return count


def printGrid(GRID):
    print('  ', end='')
    print(*[str(i+1) for i in range(len(GRID[0]))])
    for i in range(len(GRID)):
        print(str(i+1)+' ', end='')
        for j in range(len(GRID[0])):
            if GRID[i][j] == -1:
                print('X', end = ' ')
            elif GRID[i][j] == 0:
                print('□', end = ' ')
            elif GRID[i][j] == 9:
                print('▀', end = ' ')
            elif GRID[i][j] == 10:
                print('F', end = ' ')
            else:
                print(str(GRID[i][j]), end = ' ')
        print()
    print()


def changeHideGrid(HIDE_GRID, GRID, x, y):
    if 0 < GRID[y-1][x-1] < 9:
        HIDE_GRID[y-1][x-1] = GRID[y-1][x-1]
    if GRID[y-1][x-1] == 0 and HIDE_GRID[y-1][x-1] == 9:
        HIDE_GRID[y-1][x-1] = 0
        neib = takeNeighbors(GRID, x, y)
        for i in neib:
            changeHideGrid(HIDE_GRID, GRID, i[1]+1, i[0]+1)
    return HIDE_GRID
    
    
def moveProcessing(HIDE_GRID, GRID, x, y, z):
    if z == 'Open' and GRID[y-1][x-1] == -1:
        printGrid(GRID)
        return -1
    
    elif z == 'Open':
        HIDE_GRID = changeHideGrid(HIDE_GRID, GRID, x, y)
        printGrid(HIDE_GRID)
        return 0
    
    elif z == 'Flag':
        if HIDE_GRID[y-1][x-1] == 9:
            HIDE_GRID[y-1][x-1] = 10
        elif HIDE_GRID[y-1][x-1] == 10:
            HIDE_GRID[y-1][x-1] = 9
        count = 0
        flags = 0
        for i in range(len(GRID)):
            for j in range(len(GRID[0])):
                if HIDE_GRID[i-1][j-1] == 10:
                    flags += 1
                if GRID[i-1][j-1] == -1:
                    count += 1
                if HIDE_GRID[i-1][j-1] != 10 and GRID[i-1][j-1] == -1:
                    printGrid(HIDE_GRID)
                    return 0
        if flags == count:
            printGrid(GRID)
            return 1
        printGrid(HIDE_GRID)
        return 0
    
           
def enterCommand(GRID_L, GRID_W):
    COMMAND = input('Enter your move: ').split()
    if COMMAND == ['Save']:
        return 0, 0, 0
    x = 0
    y = 0
    z = 0
    try:
        x = int(COMMAND[0])
        y = int(COMMAND[1])
        z = COMMAND[2]
    except:
        pass
    while not ((1 <= x <= GRID_L) and (1 <= y <= GRID_W) and (z  in ['Flag', 'Open'])):
        print('Error. Incorrect command')
        COMMAND = input('Enter your move: ').split()
        try:
            x = int(COMMAND[0])
            y = int(COMMAND[1])
            z = COMMAND[2]
        except:
            pass
    return x, y, z


def startGame(GRID_L = 0, GRID_W = 0, BOMBS_N = 0, GRID = 0, HIDE_GRID = 0):
    if GRID == 0 and HIDE_GRID == 0:
        GRID = [[9 for i in range(GRID_L)] for j in range(GRID_W)]
        HIDE_GRID = [[9 for i in range(GRID_L)] for j in range(GRID_W)]
        print('  ', end='')
        print(*[str(i+1) for i in range(GRID_L)])
        for i in range(GRID_W):
            print(str(i+1)+' ', end='')
            print(*['▀' for j in range(GRID_L)])
        x, y, z = enterCommand(len(GRID[0]), len(GRID))
        while z != 'Open':
            print('Please, choose "Open"')
            x, y, z = enterCommand(GRID_L, GRID_W)
        neib = takeNeighbors(GRID, x, y)
        rand = list(range(0, GRID_L*GRID_W))
        rand.remove((y-1)*GRID_L+x-1)
        for i in neib:
            rand.remove((i[0])*GRID_L+i[1])
        random.shuffle(rand)
        for i in range(BOMBS_N):
            GRID[rand[i]//GRID_L][rand[i]%GRID_L] = -1
        for i in range(len(GRID)):
            for j in range(len(GRID[0])):
                if GRID[i][j] != -1:
                    neib = takeNeighbors(GRID, j+1, i+1)
                    GRID[i][j] = countMines(GRID, neib)
        res = moveProcessing(HIDE_GRID, GRID, x, y, z)
        
    if GRID_L == 0 and GRID_W == 0 and BOMBS_N == 0:
        printGrid(HIDE_GRID)
        res = 0
        
    while res == 0:
        x, y, z = enterCommand(len(GRID[0]), len(GRID))
        if x == 0 and y == 0 and z == 0:
            output = open('data.pkl', 'wb')
            data = [GRID, HIDE_GRID]
            pickle.dump(data, output)
            output.close()
            return 2
        res = moveProcessing(HIDE_GRID, GRID, x, y, z)
    return res


a = 0
while a != 1 and a != 2:
    try:
        a = input('Do you want to start new game (1) or load previous (2) ? ')
        a = int(a)
    except:
        print('Error. Incorrect data')
        
if a == 1:
    GRID_L, GRID_W, BOMBS_N = 0, 0, 0
    try:       
        GRID_L, GRID_W = input('Input lenth and width of grid (two numbers): ').split()
        GRID_L, GRID_W = int(GRID_L), int(GRID_W)
    except:
        print('Error. Incorrect data')
    while GRID_W < 3 or GRID_L < 3 or (GRID_W == 3 and GRID_L == 3):
        try:
            print('Grid must be more then 3x3')
            GRID_L, GRID_W = input('Input lenth and width of grid (two numbers): ').split()
            GRID_L, GRID_W = int(GRID_L), int(GRID_W)
        except:
            print('Error. Incorrect data')
            GRID_L = 0
            GRID_W = 0
            
    try:
        BOMBS_N = int(input('Input numbers of bombs: '))
    except:
        print('Error. Incorrect data')
        BOMBS_N = 0
    while BOMBS_N <= 0:
        try:
            BOMBS_N = int(input('Input numbers of bombs: '))
        except:
            print('Error. Incorrect data')
            BOMBS_N = 0

    while BOMBS_N >= GRID_L*GRID_W-8:
        print("Number of bombs can't be more or equal then number of cells in grid minus eight")
        try:
            BOMBS_N = int(input('Input numbers of bombs: '))
        except:
            print('Error. Incorrect data')
            
    sys.setrecursionlimit(5000)
    res = startGame(GRID_L, GRID_W, BOMBS_N, 0, 0)
    if res == 1:
        print('You won')
    elif res == -1:
        print('You lose')
    elif res == 2:
        print('You saved the game')
            
elif a == 2:
    err = 0
    try:
        pkl_file = open('data.pkl', 'rb')
        data = pickle.load(pkl_file)
        GRID = data[0]
        HIDE_GRID = data[1]
        err = 1
    except:
        print("Perhaps you didn't save the game")
        
    sys.setrecursionlimit(5000)
    if err == 1:
        res = startGame(0, 0, 0, GRID, HIDE_GRID)
    else: res = 0
    if res == 1:
        print('You won')
    elif res == -1:
        print('You lose')
    elif res == 2:
        print('You saved the game')
