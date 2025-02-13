import pygame
import random
import sys
import os
import math

# Constants
FPS = 30
PATH = 'c:\\tp\\bgi'
MAX_LEVEL = 4
ENEMY_NUM = 4
MUSIC_B = [1, 2, 3, 4, 1, 2, 3, 4, 1]

# Status
DEAD = 0
FOLLOW = 1
AROUND = 2
FLEE = 3

# Directions
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# Colors
PAC_COLOR = pygame.Color('yellow')
ENEMY_COLOR = pygame.Color('red')
ENEMY_FLEE_COLOR = pygame.Color('green')
BEAN_COLOR = pygame.Color('gold')
WALL_COLOR = pygame.Color('lightblue')
DOOR_COLOR = pygame.Color(0, 255, 0)
WALL_WIDTH = 3
BEAN_SIZE = 3

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
atom = SCREEN_WIDTH // 16
print ('atom is ' + str(atom))
unit1 = atom // 2 - 7
SPEED = atom // 8
print ('speed is ' + str(SPEED))
pit = atom // (SPEED * 2)
print ('pit is ' + str(pit))
maxX = SCREEN_WIDTH - atom
maxY = SCREEN_HEIGHT - atom
minX = 0
minY = 0

# Directions
VX = [0, SPEED, 0, -SPEED]
VY = [-SPEED, 0, SPEED, 0]

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pyth-Man")

# Clock
clock = pygame.time.Clock()

# Global variables
enemy = [None] * 4
enemyback = [None] * 4
edir = [0] * ENEMY_NUM
newedir = [0] * ENEMY_NUM
flag = [0] * ENEMY_NUM
enemyX = [0] * ENEMY_NUM
enemyY = [0] * ENEMY_NUM
control = [0] * ENEMY_NUM
oldenemyX = [0] * ENEMY_NUM
oldenemyY = [0] * ENEMY_NUM
background = None
backgroundnopac = None

pac = [[None for _ in range(5)] for _ in range(4)]
pdir = RIGHT
newpdir = RIGHT
oldpdir = RIGHT
PacX = 0
PacY = 0
oldpacX = 0
oldpacY = 0
life = 3
pose = 5
oldpose = 5
chomp = 0
eat = 0

count = 0
tone = 0
MBPtr = 0
score = 0
high = 0
die = False
newgame = True
newlevel = True
continuegame = True
MusicOn = True

# Level data
SAME_LEVEL = 2
BEAN_NUM = [261, 223]
#BEAN_NUM = [10, 10] # Test data
lrows = [['0000000000000000',
'2311111311111330',
'2120111001112030',
'2232301311232320',
'2212231003320320',
'2022222132222020',
'1030110010112101',
'3200330312310221',
'2013011001121120',
'2212013131120320',
'2020110200112020',
'0111111111111110'],
['0000000000000000',
'2311111311111330',
'2122113221132030',
'2210111001110320',
'2023230112323020',
'2211222132201320',
'1223010010123201',
'3022230312322021',
'2212203021220320',
'2032011201122120',
'2301230112301230',
'0111111111111110']]
lsides = [[
[1,2,1,2],
[14,15,1,2],
[2,3,3,4],
[2,3,3,4],
[13,14,3,4],
[4,5,3,6],
[11,12,3,6],
[5,6,4,6],
[10,11,4,6],
[5,6,7,8],
[10,11,7,8],
[7,9,5,6],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1],
[-1,-1,-1,-1]],
[[1,2,1,2],
[14,15,1,2],
[4,7,2,3],
[9,12,2,3],
[3,4,4,5],
[5,6,4,6],
[10,11,4,6],
[12,13,4,5],
[2,3,8,9],
[3,4,6,10],
[5,6,7,9],
[6,7,8,9],
[9,10,8,9],
[10,11,7,9],
[12,13,6,10],
[13,14,8,9],
[1,2,10,11],
[5,6,10,11],
[10,11,10,11],
[7,9,5,6]]]
bigbean = [[5,5], [27,5], [5,21], [27,21]]

def chdir(direction, by):
    return (direction + by - 1) % 4 + 1

def pointisthere(x, y, color):
    if x < minX or x > maxX or y < minY or y > maxY:
        return False
    return screen.get_at((x, y)) == color

def TurnOK(x, y):
    return (x % atom - atom // 2 == 0) and (y % atom - atom // 2 == 0)

def ClrBuffer():
    pygame.time.delay(500)
    pygame.event.clear()

def WaitKey():
    print ('waiting for key...')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                print ('key pressed')
                return

def INIT():
    print ('initializing...')
    global driver, mode, atom, unit1, pit, MusicOn
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36)
    text = font.render('DO YOU WANT MUSIC DURING GAME (Y/N)?', True, (255, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 24 + 50)
    screen.blit(text, title1xy)
    pygame.display.flip()
    key = None
    while key not in [pygame.K_y, pygame.K_n]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
    MusicOn = key == pygame.K_y

def addscore(gain):
    #print ('adding score...')
    global score, high
    score += gain
    if score > high:
        high = score

def showscore():
    #print ('showing score...')
    global score, high
    box(SCREEN_WIDTH - SCREEN_WIDTH // 7, SCREEN_WIDTH, SCREEN_HEIGHT // 64, SCREEN_HEIGHT // 16,  0, 0)
    font = pygame.font.SysFont(None, 48)
    text = font.render(str(score), True, PAC_COLOR, 0)
    screen.blit(text, (SCREEN_WIDTH - SCREEN_WIDTH // 7, SCREEN_HEIGHT // 64))

def showfinalscore():
    print ('showing final score...')
    global score, high
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'YOUR SCORE: {score}', True, PAC_COLOR)
    screen.blit(text, (50, 40))
    text = font.render(f'HIGH SCORE: {high}', True, PAC_COLOR)
    screen.blit(text, (50, 70))

def showlives():
    box(0, SCREEN_WIDTH, 11*atom + WALL_WIDTH, 12*atom, 1, 0)
    if life > 0:
        for ct in range(1, life):
            screen.blit(pac[1][1], (ct*atom, 11*atom + SPEED))

def box(xl, xr, yu, yd, bcolor, acolor):
    #print ('drawing box...')
    pygame.draw.rect(screen, acolor, (xl, yu, xr - xl, yd - yu))
    pygame.draw.rect(screen, bcolor, (xl, yu, xr - xl, yd - yu), WALL_WIDTH)

def drawenemy(x, y, color):
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 4
    box(x - unit1 - 1, x + unit1 + 1, y - unit1 - 1, y + unit1 + 1, 0, 0)
    pygame.draw.arc(screen, color, (x - unit1, y - unit1, unit1 * 2, unit1 * 2), 0, 3.14, 1)
    pygame.draw.line(screen, color, (x - unit1, y), (x - unit1, y + unit1), 1)
    pygame.draw.line(screen, color, (x - unit1, y + unit1), (x - unit1 + unit1 * 2 // 5, y + unit1 - unit1 * 2 // 6), 1)
    pygame.draw.line(screen, color, (x - unit1 + unit1 * 2 // 5, y + unit1 - unit1 * 2 // 6), (x - unit1 + unit1 * 4 // 5, y + unit1), 1)
    pygame.draw.line(screen, color, (x - unit1 + unit1 * 4 // 5, y + unit1), (x - unit1 + unit1 * 6 // 5, y + unit1 - unit1 * 2 // 6), 1)
    pygame.draw.line(screen, color, (x - unit1 + unit1 * 6 // 5, y + unit1 - unit1 * 2 // 6), (x - unit1 + unit1 * 8 // 5, y + unit1), 1)
    pygame.draw.line(screen, color, (x - unit1 + unit1 * 8 // 5, y + unit1), (x + unit1, y), 1)
    pygame.draw.circle(screen, color, (x - unit1 // 2, y), unit1 // 3, 1)
    pygame.draw.circle(screen, color, (x + unit1 // 2, y), unit1 // 3, 1)
    pygame.display.flip()
    rect1 = (x - unit1, y - unit1, unit1 * 2, unit1 * 2)
    return screen.subsurface(rect1).copy()

def makeenemy():
    print ('making enemy...')
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 4
    enemy[FLEE] = drawenemy(x, y, ENEMY_FLEE_COLOR)
    enemy[DEAD] = drawenemy(x, y, ENEMY_COLOR)
    enemy[FOLLOW] = drawenemy(x, y, ENEMY_COLOR)
    enemy[AROUND] = drawenemy(x, y, ENEMY_COLOR)
    pygame.time.delay(200)

def point_on_circle(center, radius, angle_radians):
    # Calculate the coordinates
    x = center[0] + radius * math.cos(angle_radians)
    y = center[1] - radius * math.sin(angle_radians)
    return (x, y)

def makepac():
    print ('making pac...')
    pparams = [[135,405,1],[45,315,2],[315,585,3],[225,495,4]]
    x = SCREEN_WIDTH / 16 * 5
    y = SCREEN_HEIGHT / 2
    for dir in range(1, 5):
        print ('capturing pac direction ' + str(dir-1) + '...')
        for count in range(1, 6):
            # draw pac using pygame drawing functions
            x += VX[dir - 1] * 10
            y += VY[dir - 1] * 8
            a1 = (pparams[dir-1][0] - count * 9) /180*3.14
            a2 = (pparams[dir-1][1] + count * 9) /180*3.14
            pygame.draw.arc(screen, PAC_COLOR, (x - unit1, y - unit1, unit1 * 2, unit1 * 2), a1, a2, 1)
            p1 = point_on_circle((x, y), unit1, a1)
            p2 = point_on_circle((x, y), unit1, a2)
            pygame.draw.line(screen, PAC_COLOR, (x, y), p1, 1)
            pygame.draw.line(screen, PAC_COLOR, (x, y), p2, 1)
            pygame.display.flip()
            # capture pac graphics of current direction and posture
            rect1 = (x - unit1, y - unit1, unit1 * 2, unit1 * 2)
            pac[dir - 1][count - 1] = screen.subsurface(rect1).copy()
            pygame.time.delay(100)
            # erase pac after capture
            box(x - unit1 - 1, x + unit1 + 1, y - unit1 - 1, y + unit1 + 1, 0, 0)
            pygame.display.flip()

def makebackground():
    print ('background...')
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 48)
    text = font.render('PYTH-MAN', True, PAC_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 20, SCREEN_HEIGHT // 64))
    # make the small beans
    dY = atom
    while True:
        dY += atom // 2
        dX = atom
        while True:
            dX += atom // 2
            box(dX - 1, dX + 1, dY - 1, dY + 1, BEAN_COLOR, BEAN_COLOR)
            if dX == atom * 15 - atom // 2:
                break
        if dY == atom * 11 - atom // 2:
            break    
    # make the big beans
    for i in range(4):
        print ('bigbean ' + str(i) + ': ' + str(bigbean[i][0]) + ', ' + str(bigbean[i][1]))
        box(bigbean[i][0]*atom//2 - BEAN_SIZE, bigbean[i][0]*atom//2 + BEAN_SIZE, bigbean[i][1]*atom//2 - BEAN_SIZE, bigbean[i][1]*atom//2 + BEAN_SIZE, BEAN_COLOR, BEAN_COLOR)
    # make the walls
    for iy in range(0, 12, 1):
        for ix in range(0, 16, 1):
            x = ix * atom
            y = iy * atom
            mcell = (lrows[level % SAME_LEVEL -1][iy][ix])
            match mcell:
                case '0':
                    1 == 1
                    #print ('(0:none)')
                case '1':
                    #print ('(1:roof)')
                    pygame.draw.line(screen, WALL_COLOR, (x, y), (x + atom, y), WALL_WIDTH)
                case '2':
                    #print ('(2:wall)')
                    pygame.draw.line(screen, WALL_COLOR, (x + atom, y), (x + atom, y + atom), WALL_WIDTH)
                case '3':
                    #print ('(3:both)')
                    pygame.draw.line(screen, WALL_COLOR, (x, y), (x + atom, y), WALL_WIDTH)
                    pygame.draw.line(screen, WALL_COLOR, (x + atom, y), (x + atom, y + atom), WALL_WIDTH)
    # clear boxes
    for BoxNo in range(1, 20):
        sl = lsides[level % SAME_LEVEL - 1][BoxNo - 1][0]
        sr = lsides[level % SAME_LEVEL - 1][BoxNo - 1][1]
        su = lsides[level % SAME_LEVEL - 1][BoxNo - 1][2]
        sd = lsides[level % SAME_LEVEL - 1][BoxNo - 1][3]
        print ('clean box ' + str(BoxNo) + ': ' + str(sl) + ', ' + str(sr) + ', ' + str(su) + ', ' + str(sd))
        box(sl * atom, sr * atom, su * atom, sd * atom, WALL_COLOR, 0)

    # make door for enemy
    pygame.draw.line(screen, DOOR_COLOR, (atom*7, atom*6), (atom*8, atom*6), WALL_WIDTH)

def playpac():
    # print ('playing pac...')
    global PacX, PacY, pdir, newpdir, pose, oldpacX, oldpacY, oldpdir, oldpose, eat, die, enemy, flag, chomp, MusicOn, background, backgroundnopac
    # repaint background with pac to erase enemies
    screen.blit(backgroundnopac, (0,0)) 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                newpdir = UP
            elif event.key == pygame.K_DOWN:
                newpdir = DOWN
            elif event.key == pygame.K_LEFT:
                newpdir = LEFT
            elif event.key == pygame.K_RIGHT:
                newpdir = RIGHT
            elif event.key == pygame.K_s:
                MusicOn = not MusicOn
                if not MusicOn:
                    pygame.mixer.stop()
                    chomp = 0
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if not pointisthere(PacX + VX[pdir - 1] * pit, PacY + VY[pdir - 1] * pit, WALL_COLOR) and not pointisthere(PacX + VX[pdir - 1] * pit, PacY + VY[pdir - 1] * pit, DOOR_COLOR):
        PacX += VX[pdir - 1]
        PacY += VY[pdir - 1]
        if PacX > maxX:
            PacX = 0
        if PacX < 0:
            PacX = maxX
        if PacY > maxY:
            PacY = 0
        if PacY < 0:
            PacY = maxY
        if pointisthere(PacX + VX[pdir - 1] * (pit - 1) - 1, PacY + VY[pdir - 1] * (pit - 1), BEAN_COLOR):
            # print ('eat bean...')
            eat += 1
            addscore(100)
            if pointisthere(PacX + VX[pdir - 1] * (pit - 1) - 2, PacY + VY[pdir - 1] * (pit - 1), BEAN_COLOR):
                print ('eat big bean...')
                if MusicOn:
                    pygame.mixer.Sound('assets/fruit.mp3').play()
                for count in range(ENEMY_NUM):
                    if flag[count] != DEAD:
                        addscore(2000)
                        flag[count] = FLEE
                        control[count] = random.randint(0, 5)
            pygame.draw.rect(screen, (0, 0, 0), (PacX + VX[pdir - 1] * (pit - 1) - 2, PacY + VY[pdir - 1] * (pit - 1) - 2, 4, 4))
    if TurnOK(PacX, PacY) and not pointisthere(PacX + VX[newpdir - 1] * pit, PacY + VY[newpdir - 1] * pit, WALL_COLOR) or (newpdir == chdir(pdir, 2)):
        pdir = newpdir
    showscore()
    showlives()
    #paint new pac...
    box(oldpacX - unit1, oldpacX + unit1, oldpacY - unit1, oldpacY + unit1, 1, 0) # erase oldpac
    backgroundnopac = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)).copy() # capture background
    screen.blit(pac[pdir - 1][pose - 1], (PacX - unit1, PacY - unit1))
    #play sound fx...
    if MusicOn:
        chomp = chomp + 1 if chomp < 18 else 1
        if chomp == 1: 
            pygame.mixer.Sound('assets/chomp.mp3').play()
    pose = pose + 1 if pose < 5 else 1
    oldpacX = PacX
    oldpacY = PacY
    oldpdir = pdir
    oldpose = pose

def playenemy():
    # print ('playing enemy...')
    global die, PacX, PacY
    for num in range(ENEMY_NUM):
        if flag[num] != DEAD:
            screen.blit(enemy[flag[num]], (enemyX[num] - unit1, enemyY[num] - unit1))
            oldenemyX[num] = enemyX[num]
            oldenemyY[num] = enemyY[num]
    #pygame.display.flip()
    for num in range(ENEMY_NUM):
        if abs(enemyX[num] - PacX) <= 20 and abs(enemyY[num] - PacY) <= 20:
            print ('enemy ' + str(num) + ' flag: ' + str(flag[num]) + ' x: ' + str(enemyX[num]) + ' y: ' + str(enemyY[num]))
            print ('pac die:' + str(die) + ' x: ' + str(PacX) + ' y: ' + str(PacY))
            if flag[num] != FLEE:
                die = True
                pygame.mixer.stop()
            else:
                #enemy dies
                if MusicOn:
                    pygame.mixer.Sound('assets/ghost.mp3').play()
                control[num] = 0
                flag[num] = DEAD
                enemyX[num] = atom * 9 - atom // 2
                enemyY[num] = atom * 6 - atom // 2
                oldenemyX[num] = enemyX[num]
                oldenemyY[num] = enemyY[num]
        if TurnOK(enemyX[num], enemyY[num]):
            control[num] += 1
            if control[num] == 10 and flag[num] == AROUND:
                flag[num] = FOLLOW
                control[num] = 0
            elif control[num] == 60 and flag[num] == FOLLOW:
                flag[num] = AROUND
                control[num] = 0
            elif control[num] == 15 and flag[num] == FLEE:
                flag[num] = FOLLOW
                control[num] = 0
            elif control[num] == 20 and flag[num] == DEAD:
                flag[num] = FOLLOW
                control[num] = 0
            if flag[num] != DEAD:
                if not pointisthere(enemyX[num] + VX[newedir[num] - 1] * pit, enemyY[num] + VY[newedir[num] - 1] * pit, WALL_COLOR):
                    edir[num] = newedir[num]
                    getnewedir(num)
                    enemyX[num] += VX[edir[num] - 1]
                    enemyY[num] += VY[edir[num] - 1]
                    if enemyX[num] > maxX:
                        enemyX[num] = 0
                    if enemyX[num] < 0:
                        enemyX[num] = maxX
                elif not pointisthere(enemyX[num] + VX[edir[num] - 1] * pit, enemyY[num] + VY[edir[num] - 1] * pit, WALL_COLOR):
                    enemyX[num] += VX[edir[num] - 1]
                    enemyY[num] += VY[edir[num] - 1]
                    if enemyX[num] > maxX:
                        enemyX[num] = 0
                    if enemyX[num] < 0:
                        enemyX[num] = maxX
                else:
                    if newedir[num] == edir[num]:
                        newedir[num] = chdir(newedir[num], random.randint(0, 1) * 2 + 1)
                    else:
                        edir[num] = chdir(newedir[num], 2)
                        getnewedir(num)
        else:
            enemyX[num] += VX[edir[num] - 1]
            enemyY[num] += VY[edir[num] - 1]
            if enemyX[num] > maxX:
                enemyX[num] = 0
            if enemyX[num] < 0:
                enemyX[num] = maxX

def getnewedir(num):
    if flag[num] == FOLLOW:
        if abs(enemyX[num] - PacX) <= abs(enemyY[num] - PacY):
            if enemyY[num] < PacY:
                newedir[num] = DOWN
            else:
                newedir[num] = UP
        else:
            if enemyX[num] > PacX:
                newedir[num] = LEFT
            else:
                newedir[num] = RIGHT
    elif flag[num] == FLEE or flag[num] == AROUND:
        newedir[num] = chdir(newedir[num], random.randint(0, 1) * 2 + 1)
    if newedir[num] == chdir(edir[num], 2):
        newedir[num] = edir[num]

def ShowPic(Lvl):
    print ('showing picture for reward...')

def Menu():
    print ('menu...')
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36)
    text = font.render('Keys Defined', True, (255, 255, 255))
    screen.blit(text, (150, 1))
    text = font.render('UP ARROW', True, (255, 255, 255))
    screen.blit(text, (10, 50))
    text = font.render('---- UP', True, (255, 255, 255))
    screen.blit(text, (200, 50))
    text = font.render('DOWN ARROW', True, (255, 255, 255))
    screen.blit(text, (10, 80))
    text = font.render('---- DOWN', True, (255, 255, 255))
    screen.blit(text, (200, 80))
    text = font.render('LEFT ARROW', True, (255, 255, 255))
    screen.blit(text, (10, 110))
    text = font.render('---- LEFT', True, (255, 255, 255))
    screen.blit(text, (200, 110))
    text = font.render('RIGHT ARROW', True, (255, 255, 255))
    screen.blit(text, (10, 140))
    text = font.render('---- RIGHT', True, (255, 255, 255))
    screen.blit(text, (200, 140))
    text = font.render('S', True, (255, 255, 255))
    screen.blit(text, (10, 170))
    text = font.render('---- MUSIC', True, (255, 255, 255))
    screen.blit(text, (200, 170))
    text = font.render('ESC', True, (255, 255, 255))
    screen.blit(text, (10, 200))
    text = font.render('---- QUIT', True, (255, 255, 255))
    screen.blit(text, (200, 200))
    pygame.display.flip()
    ClrBuffer()
    WaitKey()

def Title():
    print ('title...')
    MusicT = [2, 3, 4, 6, 6, 7, 6, 4, 2, 3, 4, 4, 3, 2, 3, 2, 3, 4, 6, 6, 7, 6, 4, 2, 3, 4, 4, 3, 3, 2]
    TimeT = [0, 0, 2, 2, 4, 1, 3, 3, 4, 1, 3, 3, 3, 3, 5, 1, 0, 1, 2, 4, 1, 3, 3, 4, 1, 3, 3, 3, 3, 7]
    Menu()
    if MusicOn:
        pygame.mixer.music.load('assets/intro.mp3')
        pygame.mixer.music.play(0)
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 72)
    text = font.render('PYTH-MAN', True, PAC_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 2))
    font = pygame.font.SysFont(None, 36)
    text = font.render('Not Rated', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 7)
    screen.blit(text, title1xy)
    text = font.render('Version 2.0  By ssrtist', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 8)
    screen.blit(text, title1xy)
    text = font.render('Copyright SillyMelon Inc. 1992-2025.', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 9)
    screen.blit(text, title1xy)
    text = font.render('All Rights Reserved.', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 10)
    screen.blit(text, title1xy)
    pygame.display.flip()

def coping():
    print ('coping...')
    # this function is to deal with death or passing level, death can lead to game over
    global life, level, score, eat, die, newlevel, MAX_LEVEL
    outX = atom * 4
    outY = atom * 4
    print ('die: ' + str(die) + ', eat: ' + str(eat))
    if die:
        life -= 1
        if life == 0:
            # game over
            GameOver()
        else:
            # dying, restart level 
            Dying()
    else:
        # cleared level, can lead to game over (win)
        font = pygame.font.SysFont(None, 72)
        text = font.render('LEVEL CLEARED', True, PAC_COLOR)
        screen.blit(text, (atom * 5, atom * 6))
        font = pygame.font.SysFont(None, 48)
        text = font.render('Press Any Key to Continue...', True, (255, 255, 255), (0, 0, 0))
        screen.blit(text, (atom, atom * 11 + WALL_WIDTH))
        pygame.display.flip()
        ClrBuffer()
        WaitKey()
        ShowPic(level)
        level += 1
        newlevel = True
        print ('level: ' + str(level))
        if level > MAX_LEVEL:
            #showfinalscore()
            #WaitKey()
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 72)
            text = font.render('YOU WIN!', True, PAC_COLOR)
            screen.blit(text, (atom * 5, atom * 6))
            font = pygame.font.SysFont(None, 48)
            text = font.render('Press Any Key to Exit...', True, (255, 255, 255))
            screen.blit(text, (atom, atom * 11 + WALL_WIDTH))
            pygame.display.flip()
            pygame.time.delay(2000)
            ClrBuffer()
            WaitKey()
            pygame.quit()
            sys.exit()

def Dying():
    print ('dying...')
    global life
    global PacX, PacY, pdir, newpdir, pose, oldpacX, oldpacY, oldpdir, oldpose, eat, die, enemy, flag, MusicOn, backgroundnopac
    #pygame.time.delay(30)
    if MusicOn:
        pygame.mixer.Sound('assets/death.mp3').play()
        pygame.time.delay(10)
    print ('blit pac dying sequence...')
    for ct in range(1, 5):
        for tone in range(2, 12):
            pygame.time.delay(20)
            screen.blit(pac[ct - 1][tone // 2 - 1], (oldpacX - unit1, oldpacY - unit1))
            pygame.display.flip()
    print ('clean background after dying...')
    screen.fill((0,0,0))
    screen.blit(backgroundnopac, (0,0))
    pygame.time.delay(100)

def GameOver():
    print ('game over...')
    global life, level, score, continuegame, newgame
    font = pygame.font.SysFont(None, 72)
    text = font.render('GAME OVER', True, PAC_COLOR)
    screen.blit(text, (atom * 5, atom * 6))
    font = pygame.font.SysFont(None, 48)
    text = font.render('CONTINUE(Y/N)? ', True, (255, 255, 255), 0)
    screen.blit(text, (atom, atom * 11 + WALL_WIDTH))
    pygame.display.flip()
    key = None
    while key not in [pygame.K_y, pygame.K_n]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
    if key == pygame.K_n:
        pygame.quit()
        sys.exit()
        continuegame = False
    else:
        continuegame = True
        newgame = True

def pacinit():
    print ('pac init...')
    global die, MBPtr, tone, PacX, PacY, oldpacX, oldpacY, pdir, newpdir, oldpdir, oldpose, pose
    die = False
    MBPtr = 0
    tone = 0
    PacX = atom * 8
    PacY = atom * 9 - atom // 2
    oldpacX = PacX
    oldpacY = PacY
    pdir = RIGHT
    newpdir = RIGHT
    oldpdir = RIGHT
    oldpose = 5
    pose = 5
    screen.blit(pac[1][4], (PacX - unit1, PacY - unit1))
    pygame.display.flip()

def enemyinit():
    print ('enemy init...')
    global enemyX, enemyY, oldenemyX, oldenemyY, edir, newedir, flag, control
    for count in range(ENEMY_NUM):
        enemyX[count] = atom * 9 - atom // 2
        enemyY[count] = atom * 6 - atom // 2
        oldenemyX[count] = enemyX[count]
        oldenemyY[count] = enemyY[count]
        edir[count] = random.randint(0, 1) * 2 + 2
        newedir[count] = DOWN
        flag[count] = random.randint(0, 1) + 1
        control[count] = random.randint(0, 2) + 1
    for count in range(ENEMY_NUM):
        screen.blit(enemy[flag[count]], (oldenemyX[count] - unit1, oldenemyY[count] - unit1))
    pygame.display.flip()

def main():
    global background, backgroundnopac, die, life, level, score, high, eat, MBPtr, continuegame, newgame, newlevel
    print ('main...')
    #INIT()
    newgame = True
    while continuegame:
        if newgame:
            print ('process new game...')
            Title()
            makeenemy()
            makepac()
            screen.fill((0, 0, 0))
            random.seed()
            MBPtr = 1
            life = 4
            level = 1
            score = 0
            high = 0
            eat = 1
            makebackground()
            background = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)).copy()
            backgroundnopac = background
            showlives()
            pygame.time.delay(1000) 
            life = 3
            newgame = False
            newlevel = False
        elif newlevel:
            print ('process new level...')
            #screen.fill((0, 0, 0))
            eat = 1
            makebackground()
            background = screen.subsurface((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)).copy()
            backgroundnopac = background
            showlives()
            pygame.time.delay(1000)
            newlevel = False
        ClrBuffer()
        pacinit()
        enemyinit()
        die = False
        print ('before game loop...')
        print ('die: ' + str(die))
        while not die and eat != BEAN_NUM[(level + 1) // SAME_LEVEL - 1]:
            timer = 0
            screen.fill((0,0,0))
            screen.blit(backgroundnopac, (0,0)) #repaint background with pac to erase enemies
            playpac()
            playenemy()
            pygame.display.flip()
            timer += clock.tick(FPS)
        print ('after game loop...')
        coping()

if __name__ == "__main__":
    main()
