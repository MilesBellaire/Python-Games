import random
import pygame

size = 15
mines = int(size*size/5)
flagsLeft = mines
board = []
map = []
display = []
moves = []

running = True
gameover = False
BOXSIZE = 40
SCREENSIZE = size*BOXSIZE
pygame.init()
pygame.font.init()
normal_font = pygame.font.SysFont("comicsans", int(BOXSIZE/2))
larger_font = pygame.font.SysFont("comicsans", 50)
pygame.display.set_caption("Mine Sweeper")
WIN = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))


def redraw(window):
    pygame.draw.rect(window, (0, 0, 0), (0, 0, SCREENSIZE, SCREENSIZE))

    for j in range(len(display)):
        for i in range(len(display)):
            if display[j][i] == ' ': 
                pygame.draw.rect(window, (50, 50, 50), (j*BOXSIZE+1, i*BOXSIZE+1, BOXSIZE-2, BOXSIZE-2))
                pygame.draw.rect(window, (100, 100, 100), (j*BOXSIZE+BOXSIZE/5, i*BOXSIZE+BOXSIZE/5, BOXSIZE-2*BOXSIZE/5, BOXSIZE-2*BOXSIZE/5))
                pygame.draw.rect(window, (200, 200, 200), (j*BOXSIZE+BOXSIZE/2.5, i*BOXSIZE+BOXSIZE/3.5, BOXSIZE-BOXSIZE/2.5-BOXSIZE/4, BOXSIZE-BOXSIZE/3.5-BOXSIZE/4))
                pygame.draw.rect(window, (225, 225, 225), (j*BOXSIZE+BOXSIZE/1.8, i*BOXSIZE+BOXSIZE/3, BOXSIZE-BOXSIZE/1.8-BOXSIZE/4, BOXSIZE-BOXSIZE/3-BOXSIZE/4))
            elif display[j][i] == 'f':
                pygame.draw.rect(window, (50, 50, 50), (j*BOXSIZE+1, i*BOXSIZE+1, BOXSIZE-2, BOXSIZE-2))
                pygame.draw.rect(window, (100, 100, 100), (j*BOXSIZE+BOXSIZE/5, i*BOXSIZE+BOXSIZE/5, BOXSIZE-2*BOXSIZE/5, BOXSIZE-2*BOXSIZE/5))
                pygame.draw.rect(window, (200, 200, 200), (j*BOXSIZE+BOXSIZE/2.5, i*BOXSIZE+BOXSIZE/3.5, BOXSIZE-BOXSIZE/2.5-BOXSIZE/4, BOXSIZE-BOXSIZE/3.5-BOXSIZE/4))
                pygame.draw.rect(window, (225, 225, 225), (j*BOXSIZE+BOXSIZE/1.8, i*BOXSIZE+BOXSIZE/3, BOXSIZE-BOXSIZE/1.8-BOXSIZE/4, BOXSIZE-BOXSIZE/3-BOXSIZE/4))
                pygame.draw.rect(window, (150, 25, 25), (j*BOXSIZE+BOXSIZE/4, i*BOXSIZE+BOXSIZE/4, BOXSIZE-2*BOXSIZE/4, BOXSIZE-2*BOXSIZE/4))
            else:
                num = normal_font.render(display[j][i], True, (255, 255, 255))
                window.blit(num, (BOXSIZE/2 + j*BOXSIZE, BOXSIZE/2 + i*BOXSIZE))
    
    for i in range(size-1):
        pygame.draw.rect(window, (255,255,255), (0, (i+1)*BOXSIZE-1, SCREENSIZE, 2))
        pygame.draw.rect(window, (255,255,255), ((i+1)*BOXSIZE-1, 0, 2, SCREENSIZE))

    flagsleft = larger_font.render(str(flagsLeft), True, (225,225,225))
    window.blit(flagsleft, (10,10))
    pygame.display.update()

def printArr(arr):
    for i in range(len(arr)):
        string = ""
        for j in range(len(arr)):
            if arr[j][i] != -1: string += " " + str(arr[j][i]) 
            else: string += str(arr[j][i])
            string += " "
        print(string)

def gotoArea(pos, cmp, func, l):

    # Bottom
    if pos[0]+1 < l:
        if cmp((pos[0]+1,pos[1])): 
            func((pos[0]+1,pos[1])) # Bottom
        # Bottom Right
        if pos[1]+1 < l and cmp((pos[0]+1,pos[1]+1)): 
            func((pos[0]+1,pos[1]+1))
        # Bottom Left
        if pos[1]-1 >= 0 and cmp((pos[0]+1,pos[1]-1)): 
            func((pos[0]+1,pos[1]-1))
    # Top
    if pos[0]-1 >= 0:
        if cmp((pos[0]-1,pos[1])): 
            func((pos[0]-1,pos[1])) # Top
        # Top Right
        if pos[1]+1 < l and cmp((pos[0]-1,pos[1]+1)): 
            func((pos[0]-1,pos[1]+1))
        # Top Left
        if pos[1]-1 >= 0 and cmp((pos[0]-1,pos[1]-1)): 
            func((pos[0]-1,pos[1]-1))
    # Right
    if pos[1]+1 < l:
        if cmp((pos[0],pos[1]+1)): 
            func((pos[0],pos[1]+1)) # Right
    # Left
    if pos[1]-1 >= 0:
        if cmp((pos[0],pos[1]-1)): 
            func((pos[0]+1,pos[1]-1)) # Left

def createBoard(s):
    for i in range(s):
        row = []
        for j in range(s):
            row.append(False)
        board.append(row)
    
    used = set()
    i = 0
    while i < mines:
        pos = (random.randint(0,s-1), random.randint(0,s-1))
        if not pos in used:
            board[pos[0]][pos[1]] = True
            i += 1
            used.add(pos)

def createMap(board):
    l = len(board)
    for i in range(l):
        row = []
        for j in range(l):
            row.append((0,-1)[board[i][j]])
        map.append(row)

    def markPos2(pos):
        def cmp(coord): 
            return not board[coord[0]][coord[1]]
        def func(coords): 
            print("pass")
            map[coords[0]][coords[1]] += 1
        gotoArea(pos, cmp, func, size)

    def markPos(pos):
        # Bottom
        if pos[0]+1 < l:
            if (not board[pos[0]+1][pos[1]]): 
                map[pos[0]+1][pos[1]] += 1 # Bottom
            # Bottom Right
            if (pos[1]+1 < l and not board[pos[0]+1][pos[1]+1]): 
                map[pos[0]+1][pos[1]+1] += 1
            # Bottom Left
            if (pos[1]-1 >= 0 and not board[pos[0]+1][pos[1]-1]): 
                map[pos[0]+1][pos[1]-1] += 1
        # Top
        if(pos[0]-1) >= 0:
            if (not board[pos[0]-1][pos[1]]): 
                map[pos[0]-1][pos[1]] += 1 # Top
            # Top Right
            if (pos[1]+1 < l and not board[pos[0]-1][pos[1]+1]): 
                map[pos[0]-1][pos[1]+1] += 1 
            # Top Left
            if (pos[1]-1 >= 0 and not board[pos[0]-1][pos[1]-1]): 
                map[pos[0]-1][pos[1]-1] += 1 
        # Right
        if(pos[1]+1 < l):
            if (not board[pos[0]][pos[1]+1]): 
                map[pos[0]][pos[1]+1] += 1 # Right
        # Left
        if(pos[1]-1 >= 0):
            if (not board[pos[0]][pos[1]-1]): 
                map[pos[0]][pos[1]-1] += 1 # Left
    
    for i in range(l):
        for j in range(l):
            if board[i][j]: markPos((i,j))

def setDisplay(map):
    l = len(map)
    for i in range(l):
        row = []
        for j in range(l):
            row.append(' ')
        display.append(row)

def showZeros(pos):
    l = len(display)
    # Bottom
    if pos[0]+1 < l:
        if display[pos[0]+1][pos[1]] == ' ':
            click(pos[0]+1, pos[1]) # Bottom
        # Bottom Right
        if (pos[1]+1 < l and display[pos[0]+1][pos[1]+1] == ' '): 
            click(pos[0]+1,pos[1]+1)
        # Bottom Left
        if (pos[1]-1 >= 0 and display[pos[0]+1][pos[1]-1] == ' '): 
            click(pos[0]+1, pos[1]-1)
    # Top
    if(pos[0]-1) >= 0:
        if display[pos[0]-1][pos[1]] == ' ':
            click(pos[0]-1, pos[1]) # Top
        # Top Right
        if (pos[1]+1 < l and display[pos[0]-1][pos[1]+1] == ' '): 
            click(pos[0]-1, pos[1]+1)
        # Top Left
        if (pos[1]-1 >= 0 and display[pos[0]-1][pos[1]-1] == ' '): 
            click(pos[0]-1, pos[1]-1)
    # Right
    if(pos[1]+1 < l and display[pos[0]][pos[1]+1] == ' '):
        click(pos[0], pos[1]+1) # Right
    # Left
    if(pos[1]-1 >= 0 and display[pos[0]-1][pos[1]] == ' '):
        click(pos[0]-1, pos[1]) # Left

def click(x,y):
    global flagsLeft, running
    if display[y][x] == 'f':
        flagsLeft += 1
    if map[y][x] < 0:                   # Hit mine
        display[y][x] = 'B'
        running = False
    else:
        display[y][x] = str(map[y][x])
        
def flag(x,y):
    global flagsLeft

    if display[y][x] == ' ':
        display[y][x] = 'f'
        flagsLeft -= 1
    elif display[y][x] == 'f':
        display[y][x] = ' '
        flagsLeft += 1

def playerMove():

    while True:
        print()
        choice = input("Would you like to click, flag, or stop(c, f, s)?: ")
        if choice == 's': raise Exception('Stop')
        x = input("Enter x position: ")
        y = input("Enter y position: ")

        
        try: 
            x, y = int(x)-1, int(y)-1
            if (x < 0) or (y < 0) or (x > len(map)) or (y > len(map)): raise Exception('Invalid Position')
        except:
            print()
            print("Invalid Position")
            continue

        if choice == 'c':
            click(x,y)
            moves.append((x,y))
            break
        elif choice == 'f':
            if display[y][x] == 'f': display[y][x] = ' '
            else: display[y][x] = 'f'
            break
        else:
            print()
            print("Invalid input")
            print("Please enter c for click and f for flag")
        
createBoard(size)
createMap(board)
printArr(map)
setDisplay(map)
redraw(WIN)

ready = True
while running:
    if pygame.mouse.get_pressed()[0]:
        if ready:
            click(int(pygame.mouse.get_pos()[1]/BOXSIZE), int(pygame.mouse.get_pos()[0]/BOXSIZE))
            redraw(WIN)
            ready = False
    elif pygame.mouse.get_pressed()[2]:
        if ready: 
            flag(int(pygame.mouse.get_pos()[1]/BOXSIZE), int(pygame.mouse.get_pos()[0]/BOXSIZE))
            redraw(WIN)
            ready = False
    else:
        ready = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
