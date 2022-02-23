import pygame,sys,os,time

# CHECK BOARD STATE --------------------------------------- #
def check_board_state(board):
    # ROWS ----------------------------------- #
    for row in board:
        if row == [-1,-1,-1]:
            return -1
        elif row == [1,1,1]:
            return 1
    # COLS ----------------------------------- #
    for i in range(3):
        col = [board[0][i],board[1][i],board[2][i]]
        if col == [-1,-1,-1]:
            return -1
        elif col == [1,1,1]:
            return 1
            
    # DIAGS ------------------------------------ #
    diag = [board[0][0],board[1][1],board[2][2]]
    if diag == [-1,-1,-1]:
        return -1
    elif diag == [1,1,1]:
        return 1
      
    diag2 = [board[0][2],board[1][1],board[2][0]]
    if diag2 == [-1,-1,-1]:
        return -1
    elif diag2 == [1,1,1]:
        return 1

    # Moves Left
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return None
    # DRAW
    return 0

# GET CHILDREN NODES -------- #
def get_moves(board, maximize):
    children = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                temp_board = [x[:] for x in board]
                temp_board[i][j] = maximize
                children.append(temp_board)
    
    return children 
    
# Minimax Function ----------------------------------------------------- #    
def minimax(board, maximize, a, b, depth):
    result = check_board_state(board)
    if result is not None:
        return result, board
    if depth == 0 and result is None:
        return maximize, board
    
    moves = get_moves(board,maximize)
      
    if maximize == 1:
        value = -999
        for move in moves:
            score, _ = minimax(move, -maximize,a,b, depth-1)
            if score > value:
                value = score
                best_move = move        
            if value >= b:
                return value, move 
            a = max(a, value)
        return value, best_move
    else:
        value = 999
        for move in moves:
            score, _ = minimax(move, -maximize,a,b,depth-1)
            if score < value:
                value = score
                best_move = move  
            if value <= a:
                return value, move 
            b = min(b, value)
        return value, best_move

# GAMEOVER --------------------------------------------------------------- #
def gameover():
    click = False
    running = True
    while running:
        screen.fill((0,0,0))
        
        mx,my = pygame.mouse.get_pos()
        
        text = mediumFont.render("Game Over", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (250,50)
        screen.blit(text, textRect) 

        text = mediumFont.render("Play Again", True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (250,450)
        pygame.draw.rect(screen, (255,255,255),textRect)
        screen.blit(text, textRect) 
        
        if click and textRect.collidepoint(mx,my):
            return
        
        for i in range(3):
            for j in range(3):
                color = colors[board[i][j]]
                pygame.draw.rect(screen, color , board_rects[i*3+j], 0)
        
        for rect in board_rects:
            pygame.draw.rect(screen, (255,255,255), rect, 1)    
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True   
        
        pygame.display.update()
        clock.tick(60)  

# RESET BOARD ---------------------------------------- #
def reset_board():
    board = [[0,0,0],
             [0,0,0],
             [0,0,0]]
    player = select_player()
    return board, player

# Player Select ----------------------------------------------- #
def select_player():
    click = False
    running = True
    while running:
        screen.fill((0,0,0))
        mx,my = pygame.mouse.get_pos()
        
        stext = mediumFont.render("Who Goes First?", True, (255,255,255))
        stextRect = stext.get_rect()
        stextRect.center = (250,50)
        screen.blit(stext, stextRect) 
        
        text1 = mediumFont.render("You", True, (0,0,255))
        textRect1 = text1.get_rect()
        textRect1.center = (100,250)
        pygame.draw.rect(screen, (255,255,255),textRect1)
        screen.blit(text1, textRect1) 

        text2 = mediumFont.render("Computer", True, (255,0,0))
        textRect2 = text2.get_rect()
        textRect2.center = (400,250)
        pygame.draw.rect(screen, (255,255,255),textRect2)
        screen.blit(text2, textRect2) 
        
        if click and textRect2.collidepoint(mx,my):
            return 1
        
        if click and textRect1.collidepoint(mx,my):
            return -1
                  
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True   
        
        pygame.display.update()
        clock.tick(60)   

# VARS and INIT ------------------------------------- #
WIDTH = 500
HEIGHT = 500

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

size = 100
board_rects = [pygame.Rect((size+i*size,size+j*size,size,size)) for i in range(3) for j in range(3)]

mediumFont = pygame.font.Font("./assets/OpenSans-Regular.ttf", 28)

board = [[0,0,0],
         [0,0,0],
         [0,0,0]]

click = False
running = True

player = -1
depth = 9
colors = [(0,0,0),(255,0,0),(0,0,255)]

# GAME LOOP -------------------- #
player = select_player()

while running:
    screen.fill((0,0,0))

    mx,my = pygame.mouse.get_pos()

    # DRAW GAME BOARD WITH CURRENT STATE ----------------------------- #
    for i in range(3):
        for j in range(3):
            color = colors[board[i][j]]
            pygame.draw.rect(screen, color , board_rects[i*3+j], 0)
            
            if player == -1:
                if board_rects[i*3+j].collidepoint(mx,my) and click and board[i][j] == 0:
                    board[i][j] = int(player)
                    player = -player
                    
    for rect in board_rects:
         pygame.draw.rect(screen, (255,255,255), rect, 1)
    
    # AI move -------------------------------------------------------- #
    if player == 1:
        _, best_move = minimax(board, player, -999, 999, depth)
        board = best_move
        player = -player
        
    # EVENTS ---------------------------------------------------------- #
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    # Is GAME OVER? ----------------------------------------------------- #
    if check_board_state(board) is not None:
        gameover()
        board, player = reset_board()
        time.sleep(0.5)
        
    pygame.display.update()
    clock.tick(60)
