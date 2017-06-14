import random, time, pygame, sys, datetime, webbrowser
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
BOXSIZE = 20 # 블럭크기
BOARDWIDTH = 10 # 가로블럭갯수 
BOARDHEIGHT = 20 # 세로블럭갯수
BLANK = '.' # 빈칸

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 3) # 전체창중 테트리스 게임창과 양 옆의 떨어진거리
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5 # 전체창중 테트리스 게임창과 위부분과 떨어진거리

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
PURPLE      = ( 97,  28, 161)
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)
ORANGE      = (255, 187,   0)
SKYBLUE      = (  0, 216, 255)

BORDERCOLOR = SKYBLUE
BGCOLOR = WHITE
TEXTCOLOR = BLACK
TEXTSHADOWCOLOR = GREEN
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW,    ORANGE,   BLACK,  PURPLE, GRAY)

TEMPLATEWIDTH = 5  # 5X5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '..O..',
                     '..O..',
                     '..O..'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.OO..',
                     '.OO..',
                     '.....',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.OOO.',
                     '...O.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.OOO.',
                     '..O..',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

Img = pygame.image.load('blackhole.png')
Img2 = pygame.image.load('Humangreed.jpg')
Img3 = pygame.image.load('fish.jpg')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MIDDLE
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #게임화면 크기
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18) #폰트파일로딩과 글씨 크기
    BIGFONT = pygame.font.Font('freesansbold.ttf', 90)
    MIDDLE = pygame.font.Font('freesansbold.ttf', 30)
    pygame.display.set_caption('Tetris') #타이틀 화면의 제목
    DISPLAYSURF.fill(WHITE)

    showTextScreen('Tetris',BIGFONT,BASICFONT,TEXTCOLOR,TEXTSHADOWCOLOR)
    while True: #while을 통해서 다시시작 가능
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('Time Trials.mp3')
        else:
            pygame.mixer.music.load('SURV1V3.mp3')
        pygame.mixer.music.play(-1, 0.0) #음악재생
        runGame() #메인함수 시작
        pygame.mixer.music.stop() #음악중지
        finish = pygame.mixer.Sound('final.wav')
        finish.play()
        showTextScreen('Game over', BIGFONT, BASICFONT, TEXTCOLOR, TEXTSHADOWCOLOR)

def runGame(): # 게임의 메인이 되는 함수
    global Img, Img2, Img3
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    musicplay = 0
    dummy = 1
    play = 0
    hole = 0
    MUSICVOLUME = 0.5
    pygame.mixer.music.set_volume(MUSICVOLUME)
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: #죽지 않으면 계속해서 블럭이 생성되어 내려옴
        if fallingPiece == None: # 떨어지는 블럭이 없으면 생성
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # 시간초기화

            if not isValidPosition(board, fallingPiece):
                return # 보드에 새로운 블럭을 놓을 수 없으면 게임종료

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if (event.key == K_r):
                    pygame.mixer.music.stop()
                    return main()
                if (event.key == K_p):
                    hole += 1
                    if hole >= 3:
                        pygame.mixer.music.stop()
                        zzz = pygame.mixer.Sound('smile.wav')
                        zzz.play()
                        DISPLAYSURF.blit(Img, [0, 0])
                        showTextScreen1('Press a Enter',BIGFONT,RED,WHITE)
                        DISPLAYSURF.blit(Img2, [0, 0])
                        showTextScreen1('One More Press a Enter',MIDDLE,RED,WHITE)
                        DISPLAYSURF.blit(Img3, [0, 0])
                        showTextScreen2('Big Fish!!!',BIGFONT,RED,WHITE)


                    pygame.mixer.music.pause()
                    showTextScreen('Paused', BIGFONT, BASICFONT, TEXTCOLOR, TEXTSHADOWCOLOR) #일시정지
                    if play == 0:
                        pygame.mixer.music.unpause()
                    lastFallTime = time.time() #정지 후 시간이 지나가므로 현재시간으로 설정
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT):
                    movingLeft = False
                elif (event.key == K_RIGHT):
                    movingRight = False
                elif (event.key == K_DOWN):
                     movingDown = False

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                #위 방향키로 블럭의 방향 바꿈
                elif (event.key == K_UP):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                

                #아래 방향키로 블럭을 내려오는 속도보다 빠르게 내릴수 있음
                elif (event.key == K_DOWN):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                #스페이스나 엔터로 블럭을 한번에 바닥에 내림
                elif (event.key == K_SPACE or event.key == 13):
                    Boo = pygame.mixer.Sound('Attack.wav')
                    Boo.play()
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

                elif (event.key == K_q):
                    if play == 0:
                        play = 1
                        pygame.mixer.music.pause()
                    else:
                        play = 0
                        pygame.mixer.music.unpause()

                elif (event.key == K_0):
                    if MUSICVOLUME < 0.5:
                        MUSICVOLUME += 0.1
                    pygame.mixer.music.set_volume(MUSICVOLUME)
                elif (event.key == K_MINUS):
                    if MUSICVOLUME > 0:
                        MUSICVOLUME -= 0.1
                    pygame.mixer.music.set_volume(MUSICVOLUME)

        # 사용자의 입력에 따라 블럭을 움직임
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # 떨어질 시간이 되면 블럭을 떨어뜨린다
        if time.time() - lastFallTime > fallFreq:
            # 블럭이 바닥에 도착했는지 검사
            if not isValidPosition(board, fallingPiece, adjY=1):
                # 바닥에 블럭이 도착하면 보드에 생성
                fallingPiece['color'] = 7
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                # 점수에 따라서 음악이 바뀌고 속도가 순간적으로 증가
                if score > 0 and score > dummy * 7 :
                    dummy += 1
                if score > 5 * dummy and score < 7 * dummy:
                    if musicplay == 0 and play == 0:
                        pygame.mixer.music.load('fire.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        musicplay += 1
                    level, fallFreq = calculateLevelAndFallFreq2(score)
                else:
                    if musicplay == 1:
                        pygame.mixer.music.stop()
                        if play == 0:
                            if random.randint(0, 1) == 0:
                                pygame.mixer.music.load('Time Trials.mp3')
                            else:
                                pygame.mixer.music.load('SURV1V3.mp3')
                            pygame.mixer.music.play(-1, 0.0)
                            musicplay -= 1
                    level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
                    
            else:
                # 블럭이 땅에 마주치지않으면 한칸씩 떨어진다
                fallingPiece['y'] += 1
                lastFallTime = time.time()


        # 화면에 모두 그리기
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate(): #종료
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    #KEYUP 이벤트가 발생했는지 찾는다.
    #KEYDOWN 이벤트를 찾아제거
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text,font1, font2 ,textcolor,shadowcolor):
    # 글씨 그림자 출력
    titleSurf, titleRect = makeTextObjs(text, font1, shadowcolor)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 글씨 출력
    titleSurf, titleRect = makeTextObjs(text, font1, textcolor)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    #"Press a key to play." 출력
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', font2, textcolor)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen1(text,font1,textcolor,shadowcolor):

    titleSurf, titleRect = makeTextObjs(text, font1, shadowcolor)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, font1, textcolor)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    while checkForKeyPress() != 13:
        pygame.display.update()
        FPSCLOCK.tick()

def showTextScreen2(text,font1,textcolor,shadowcolor):

    titleSurf, titleRect = makeTextObjs(text, font1, shadowcolor)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, font1, textcolor)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    fff =  pygame.mixer.Sound('fish.wav')
    fff.play()
    seconds = 0
    while checkForKeyPress() == None:
        seconds += 1
        pygame.display.update()
        FPSCLOCK.tick()
        if seconds == 200:
            url = 'www.kangtaegong.com'
            webbrowser.open(url)
            terminate()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def calculateLevelAndFallFreq(score): #블록 다운 속도
    level = int(score / 10) + 1
    fallFreq = 0.40 - (level * 0.02)
    return level, fallFreq

def calculateLevelAndFallFreq2(score):
    level = int(score / 10) + 1
    fallFreq = 0.20 - (level * 0.02)
    return level, fallFreq

def getNewPiece(): # 랜덤으로 블럭 생성
    shape = random.choice(list(PIECES.keys()))
    if shape == 'S':
        color = 0
    elif shape == 'Z':
        color = 1
    elif shape == 'J':
        color = 2
    elif shape == 'L':
        color = 3
    elif shape == 'I':
        color = 4
    elif shape == 'O':
        color = 5
    else:
        color = 6
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # 화면 밖에서 부터 떨어지도록
                'color': color}
    return newPiece


def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    #맨처음에 빈보드 생성
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # 충돌검사
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # 한줄이 완변하게됬는지
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 #바닥에서 시작
    while y >= 0:
        if isCompleteLine(board, y):
            # 한줄이 완변하게 됬으면
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            pop = pygame.mixer.Sound('Boom.wav')
            pop.play()
        else:
            y -= 1 # 한줄씩 올라가면서 확인
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    for i in range(0,9):
        pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (153 + BOXSIZE * i, 66), (153 + BOXSIZE * i, 477), 3)

    #pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    now = datetime.datetime.now()
    nowTime = now.strftime('%H:%M:%S')

    #화면에 시간 출력
    timeSurf = BASICFONT.render('Time: %s' % nowTime, True, TEXTCOLOR)
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (WINDOWWIDTH - 170, 30)
    DISPLAYSURF.blit(timeSurf, timeRect)
    #화면에 점수 출력
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 170, 60)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    #화면에 레벨 출력
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 170, 90)
    DISPLAYSURF.blit(levelSurf, levelRect)

    #화면에 사용키 출력
    useSurf = BASICFONT.render('    ^        : Shift', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 300)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('<      >    : Left / Right', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 325)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('    V        : Slow down', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 350)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('Space : Fast down', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 375)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('R : Restart', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 400)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('P : Paused', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 425)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('ESC : Quit', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (WINDOWWIDTH - 195, 450)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('Q : Pause Music / UnPause Music', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (0, 0)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render('0 : Volume Up', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (0, 25)
    DISPLAYSURF.blit(useSurf, useRect)
    useSurf = BASICFONT.render(' - : Volume Down', True, TEXTCOLOR)
    useRect = useSurf.get_rect()
    useRect.topleft = (0, 50)
    DISPLAYSURF.blit(useSurf, useRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    #화면에 next 출력
    nextSurf = BASICFONT.render('Next: =========', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 170, 120)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 135)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 150)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 165)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 180)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 195)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('|                  |', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 210)
    DISPLAYSURF.blit(nextSurf, nextRect)
    nextSurf = BASICFONT.render('=========', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 225)
    DISPLAYSURF.blit(nextSurf, nextRect)
    #화면에 다음 블럭 출력
    drawPiece(piece, pixelx=WINDOWWIDTH-114, pixely=130)

if __name__ == '__main__':
    main()