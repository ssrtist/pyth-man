import pygame
import random
import sys
import os

# Constants
FPS = 30
PATH = 'c:\\tp\\bgi'
SAME_LEVEL = 2
MAX_LEVEL = 2
BEAN_NUM = [261, 223]
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
ENEMY_COLOR = pygame.Color(253, 253, 253)
BEAN_COLOR = pygame.Color(0, 0, 255)
WALL_COLOR = pygame.Color('lightblue')
DOOR_COLOR = pygame.Color(0, 255, 0)
WALL_WIDTH = 2

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
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Macpan")

# Clock
clock = pygame.time.Clock()

# Global variables
enemy = [None] * 4
edir = [0] * ENEMY_NUM
newedir = [0] * ENEMY_NUM
flag = [0] * ENEMY_NUM
enemyX = [0] * ENEMY_NUM
enemyY = [0] * ENEMY_NUM
control = [0] * ENEMY_NUM
oldenemyX = [0] * ENEMY_NUM
oldenemyY = [0] * ENEMY_NUM

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
eat = 0

count = 0
tone = 0
MBPtr = 0
score = 0
high = 0
level = 1
die = False
MusicOn = True

# Level data
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
    text = font.render('Does this system has a VGA or SVGA card (Y/N)?', True, (255, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 24)
    screen.blit(text, title1xy)
    pygame.display.flip()

    key = None
    while key not in [pygame.K_y, pygame.K_n]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key

    if key == pygame.K_y:
        driver = 0
        mode = 1
        #atom = 40
    else:
        print("Then Get ONE!!!  Step on this cheap computer!!")
        pygame.quit()
        sys.exit()

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

def playmusic(frequency, time, on):
    print ('playing music...')
    if not on:
        # pygame.mixer.music.stop()
        return
    # pygame.mixer.music.play(-1)
    # pygame.time.delay(time)

def addscore(gain):
    print ('adding score...')
    global score, high
    score += gain
    if score > high:
        high = score

def showscore():
    print ('showing score...')
    # screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'YOUR SCORE: {score}', True, PAC_COLOR)
    screen.blit(text, (50, 40))
    text = font.render(f'HIGH SCORE: {high}', True, PAC_COLOR)
    screen.blit(text, (50, 70))
    pygame.display.flip()

def box(xl, xr, yu, yd, bcolor, acolor):
    #print ('drawing box...')
    pygame.draw.rect(screen, acolor, (xl, yu, xr - xl, yd - yu))
    pygame.draw.rect(screen, bcolor, (xl, yu, xr - xl, yd - yu), 1)

def makeenemy():
    print ('making enemy...')
    global enemy
    #x = 320
    #y = 100
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 4
    for count in range(0,3):
        box(x - unit1 - 1, x + unit1 + 1, y - unit1 - 1, y + unit1 + 1, 1, 0)
        #E_COLOR = ((count+1)*30, (count*2+1)*30, (count*2+2)*30)
        E_COLOR = (count+1) * 3000000
        pygame.draw.arc(screen, E_COLOR, (x - unit1, y - unit1, unit1 * 2, unit1 * 2), 0, 3.14, 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1, y), (x - unit1, y + unit1), 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1, y + unit1), (x - unit1 + unit1 * 2 // 5, y + unit1 - unit1 * 2 // 6), 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1 + unit1 * 2 // 5, y + unit1 - unit1 * 2 // 6), (x - unit1 + unit1 * 4 // 5, y + unit1), 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1 + unit1 * 4 // 5, y + unit1), (x - unit1 + unit1 * 6 // 5, y + unit1 - unit1 * 2 // 6), 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1 + unit1 * 6 // 5, y + unit1 - unit1 * 2 // 6), (x - unit1 + unit1 * 8 // 5, y + unit1), 1)
        pygame.draw.line(screen, E_COLOR, (x - unit1 + unit1 * 8 // 5, y + unit1), (x + unit1, y), 1)
        pygame.draw.circle(screen, E_COLOR, (x - unit1 // 2, y), unit1 // 3, 1)
        pygame.draw.circle(screen, E_COLOR, (x + unit1 // 2, y), unit1 // 3, 1)
        pygame.display.flip()
        #enemy[FLEE] = pygame.Surface((unit1 * 2, unit1 * 2), pygame.SRCALPHA)
        #enemy[DEAD] = pygame.Surface((unit1 * 2, unit1 * 2), pygame.SRCALPHA)
        #enemy[FOLLOW] = pygame.Surface((unit1 * 2, unit1 * 2), pygame.SRCALPHA)
        #enemy[AROUND] = pygame.Surface((unit1 * 2, unit1 * 2), pygame.SRCALPHA)
        rect1 = (x - unit1, y - unit1, unit1 * 2, unit1 * 2)
        enemy[count] = screen.subsurface(rect1).copy()
        pygame.time.delay(200)
    #enemy[FLEE] = screen.subsurface(rect1).copy()
    #enemy[DEAD] = screen.subsurface(rect1).copy()
    #enemy[FOLLOW] = screen.subsurface(rect1).copy()
    #enemy[AROUND] = screen.subsurface(rect1).copy()
    #pygame.time.delay(200)
    #box(x - unit1 - 1, x + unit1 + 1, y - unit1 - 1, y + unit1 + 1, 1, 0)

def makepac():
    print ('making pac...')
    pparams = [[135,405,1],[45,315,2],[315,585,3],[225,495,4]]
    # global pac
    #x = 200
    #y = 220
    x = SCREEN_WIDTH / 16 * 5
    y = SCREEN_HEIGHT / 2
    for dir in range(1, 5):
        for count in range(1, 6):
            print ('making pac... ' + str(dir-1) + ' ' + str(count-1))
            x += VX[dir - 1] * 10
            y += VY[dir - 1] * 8
            a1 = (pparams[dir-1][0] - count * 9) /180*3.14
            a2 = (pparams[dir-1][1] + count * 9) /180*3.14
            #print ('drawing arc... x:'+ str(x - unit1) + ' y:' + str(y - unit1) + ' w:' + str(unit1 * 2) + ' h:' + str(unit1 * 2) + ' a1:' + str(pparams[dir-1][0]) + ' r1:' + str(a1) + ' a2:' + str(pparams[dir-1][1]) + ' r2:' + str(a2))
            pygame.draw.arc(screen, PAC_COLOR, (x - unit1, y - unit1, unit1 * 2, unit1 * 2), a1, a2, 1)
            pygame.display.flip()
            print ('capturing pac ' + str(dir-1) + ' ' + str(count-1))
            # pac[dir - 1][count - 1] = pygame.Surface((unit1 * 2, unit1 * 2), pygame.SRCALPHA)
            rect1 = (x - unit1, y - unit1, unit1 * 2, unit1 * 2)
            pac[dir - 1][count - 1] = screen.subsurface(rect1).copy()
            pygame.time.delay(100)
            box(x - unit1 - 1, x + unit1 + 1, y - unit1 - 1, y + unit1 + 1, 1, 0)

def background():
    print ('background...')
    #print (lrows)
    global level
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 48)
    text = font.render('PYTH-MAN', True, PAC_COLOR)
    screen.blit(text, (50, 0))
    #for y in range(atom, maxY, atom):
    #    for x in range(atom, maxX, atom):
    #        box(x - 1, x + 1, y - 1, y + 1, BEAN_COLOR, 0)
    #        print (str(x // atom - 1), str(y // atom - 1))
    #for y in range(atom, maxY-atom*2, atom):
    for iy in range(0, 12, 1):
        mrow = ''
        #for x in range(atom, maxX-atom*3, atom):
        for ix in range(0, 16, 1):
            x = ix * atom
            y = iy * atom
            box(x - 1, x + 1, y - 1, y + 1, BEAN_COLOR, 0)
            #print (str(x // atom - 1), str(y // atom - 1))
            #mcell = (lrows[0][y//atom-1][x//atom-1])
            #print (str(x), str(y))
            mcell = (lrows[0][iy][ix])
            mrow += mcell
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
        print (mrow) #level row data
    pygame.display.flip()

def playpac():
    # print ('playing pac...')
    global PacX, PacY, pdir, newpdir, pose, oldpacX, oldpacY, oldpdir, oldpose, eat, die
    # debug msg below
    # print ('blit pac ' + str(oldpdir -1) + ' ' + str(oldpose - 1), (90, 0))
    # screen.blit(pac[oldpdir - 1][oldpose - 1], (oldpacX - unit1, oldpacY - unit1))
    # pygame.time.delay(500)
    box(oldpacX - unit1, oldpacX + unit1, oldpacY - unit1, oldpacY + unit1, 1, 0)
    pygame.time.delay(30)
    pose = pose + 1 if pose < 5 else 1
    screen.blit(pac[pdir - 1][pose - 1], (PacX - unit1, PacY - unit1))
    pygame.display.flip()
    oldpacX = PacX
    oldpacY = PacY
    oldpdir = pdir
    oldpose = pose
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if not pointisthere(PacX + VX[pdir - 1] * pit, PacY + VY[pdir - 1] * pit, WALL_COLOR):
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
            # if MusicOn:
                # pygame.mixer.music.play(0)
            eat += 1
            addscore(100)
            if pointisthere(PacX + VX[pdir - 1] * (pit - 1) - 2, PacY + VY[pdir - 1] * (pit - 1), BEAN_COLOR):
                for count in range(ENEMY_NUM):
                    if flag[count] != DEAD:
                        addscore(2000)
                        screen.blit(enemy[flag[count]], (oldenemyX[count] - unit1, oldenemyY[count] - unit1))
                        flag[count] = FLEE
                        screen.blit(enemy[flag[count]], (oldenemyX[count] - unit1, oldenemyY[count] - unit1))
                        control[count] = random.randint(0, 5)
            Fcolor = screen.get_at((PacX + VX[pdir - 1] * (pit - 1) - 1, PacY + VY[pdir - 1] * (pit - 1) - 1))
            pygame.draw.rect(screen, (0, 0, 0), (PacX + VX[pdir - 1] * (pit - 1) - 1, PacY + VY[pdir - 1] * (pit - 1) - 1, 2, 2))
            pygame.draw.rect(screen, (0, 0, 0), (PacX + VX[pdir - 1] * (pit - 1) - 2, PacY + VY[pdir - 1] * (pit - 1) - 2, 4, 4))
            screen.set_at((PacX + VX[pdir - 1] * (pit - 1) - 1, PacY + VY[pdir - 1] * (pit - 1) - 1), Fcolor)
            pygame.display.flip()
    if TurnOK(PacX, PacY) and not pointisthere(PacX + VX[newpdir - 1] * pit, PacY + VY[newpdir - 1] * pit, WALL_COLOR) or (newpdir == chdir(pdir, 2)):
        pdir = newpdir

def playenemy():
    # print ('playing enemy...')
    global die
    for num in range(ENEMY_NUM):
        if flag[num] != DEAD:
            #screen.blit(enemy[flag[num]], (oldenemyX[num] - unit1, oldenemyY[num] - unit1))
            box(oldenemyX[num] - unit1, oldenemyX[num] + unit1, oldenemyY[num] - unit1, oldenemyY[num] + unit1, 1, 0)
            screen.blit(enemy[flag[num]], (enemyX[num] - unit1, enemyY[num] - unit1))
            pygame.display.flip()
            oldenemyX[num] = enemyX[num]
            oldenemyY[num] = enemyY[num]
    for num in range(ENEMY_NUM):
        if abs(enemyX[num] - PacX) <= 20 and abs(enemyY[num] - PacY) <= 20:
            if flag[num] != FLEE:
                die = True
            else:
                screen.blit(enemy[flag[num]], (oldenemyX[num] - unit1, oldenemyY[num] - unit1))
                control[num] = 0
                flag[num] = DEAD
                enemyX[num] = atom * 9 - atom // 2
                enemyY[num] = atom * 6 - atom // 2
                oldenemyX[num] = enemyX[num]
                oldenemyY[num] = enemyY[num]
                screen.blit(enemy[flag[num]], (oldenemyX[num] - unit1, oldenemyY[num] - unit1))
                pygame.display.flip()
        if TurnOK(enemyX[num], enemyY[num]):
            control[num] += 1
            if control[num] == 10 and flag[num] == AROUND:
                flag[num] = FOLLOW
                control[num] = 0
            elif control[num] == 60 and flag[num] == FOLLOW:
                flag[num] = AROUND
                control[num] = 0
            elif control[num] == 15 and flag[num] == FLEE:
                screen.blit(enemy[flag[num]], (oldenemyX[num] - unit1, oldenemyY[num] - unit1))
                flag[num] = FOLLOW
                control[num] = 0
                screen.blit(enemy[flag[num]], (oldenemyX[num] - unit1, oldenemyY[num] - unit1))
                pygame.display.flip()
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
    print ('showing pic...')
    #command = f'GIRL{Lvl}.VSF'
    #os.system(f'SVSF.EXE {command}')

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
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 72)
    text = font.render('PYTH-MAN', True, PAC_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 2))
    font = pygame.font.SysFont(None, 36)
    text = font.render('V-Rated', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 7)
    screen.blit(text, title1xy)
    text = font.render('Version 2.0  By SSRTIST', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 8)
    screen.blit(text, title1xy)
    text = font.render('Copyright SillyMelon Corp. 1992-2025.', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 9)
    screen.blit(text, title1xy)
    text = font.render('All Rights Reserved.', True, (0, 255, 255))
    title1xy = (SCREEN_WIDTH // 64, SCREEN_HEIGHT // 12 * 10)
    screen.blit(text, title1xy)
    pygame.display.flip()
    ClrBuffer()
    #MTPtr = 0
    #while MTPtr < 30:
    #    playmusic(MusicT[MTPtr] * 100 + 400, TimeT[MTPtr] * 100 + 50, MusicOn)
    #    MTPtr += 1
    #    for event in pygame.event.get():
    #        if event.type == pygame.KEYDOWN:
    #            break
    # pygame.mixer.music.stop()

def coping():
    print ('coping...')
    # this function is to deal with death or passing level, death can lead to game over
    global life, level, score, eat, die
    outX = atom * 4
    outY = atom * 4
    print ('die: ' + str(die))
    if die:
        life -= 1
        if life == 0:
            # game over
            GameOver()
        else:
            # dying, restart level 
            Dying()
    else:
        # passing level, can lead to game over (win)
        font = pygame.font.SysFont(None, 72)
        text = font.render('You win', True, PAC_COLOR)
        screen.blit(text, (outX, outY))
        pygame.display.flip()
        ClrBuffer()
        WaitKey()
        ShowPic(level)
        level += 1
        if level > MAX_LEVEL * SAME_LEVEL:
            showscore()
            WaitKey()
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 72)
            text = font.render('THE END.', True, (255, 0, 0))
            screen.blit(text, (150, 250))
            pygame.display.flip()
            ClrBuffer()
            WaitKey()
            pygame.quit()
            sys.exit()
        eat = 0
        showscore()
        ClrBuffer()
        WaitKey()
        screen.fill((0, 0, 0))
        background()

def Dying():
    print ('dying...')
    global life
    if life > 0:
        screen.blit(pac[1][0], (15 * atom + SPEED, life * atom))
    for ct in range(1, 5):
        for tone in range(2, 12):
            screen.blit(pac[ct - 1][tone // 2 - 1], (PacX - unit1, PacY - unit1))
            if MusicOn:
                #pygame.mixer.music.play(0)
                pygame.time.delay(10)
            pygame.time.delay(20)
            screen.blit(pac[ct - 1][tone // 2 - 1], (PacX - unit1, PacY - unit1))
    if MusicOn:
        #pygame.mixer.music.play(0)
        pygame.time.delay(10)
    pygame.time.delay(100)
    #pygame.mixer.music.stop()

def GameOver():
    print ('game over...')
    global life, level, score
    font = pygame.font.SysFont(None, 72)
    text = font.render('GAME OVER', True, PAC_COLOR)
    screen.blit(text, (atom * 4 + 20, atom * 4))
    # pygame.display.flip()
    # WaitKey()
    showscore()
    font = pygame.font.SysFont(None, 36)
    text = font.render('CONTINUE(Y/N)? ', True, (255, 255, 255))
    screen.blit(text, (10, 400))
    pygame.display.flip()
    key = None
    while key not in [pygame.K_y, pygame.K_n]:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
    if key == pygame.K_n:
        pygame.quit()
        sys.exit()
    life = 3
    level = 1
    score = 0
    eat = 0
    Title()
    screen.fill((0, 0, 0))
    background()

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
    pygame.time.delay(2000)
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
        # print ('blit enemy ' + str(flag[count]), (90, 0))
        screen.blit(enemy[flag[count]], (oldenemyX[count] - unit1, oldenemyY[count] - unit1))
    pygame.display.flip()

def main():
    print ('main...')
    INIT()
    Title()
    makeenemy()
    makepac()
    screen.fill((0, 0, 0))
    random.seed()
    MBPtr = 1
    life = 3
    level = 1
    score = 0
    high = 0
    eat = 0
    background()
    while True:
        ClrBuffer()
        pacinit()
        enemyinit()
        die = False
        print ('before game loop...')
        print ('die: ' + str(die))
        while not die: # and eat != BEAN_NUM[(level + 1) // SAME_LEVEL - 1]:
            # print ('inside game loop, die: ' + str(die) + ', eat: ' + str(eat))
            # play sprite sfx, not working
            # MBPtr = MBPtr + 1 if MBPtr < 9 else 1
            # playmusic(MUSIC_B[MBPtr - 1] * 100 + 400, 0, MusicOn)
            playpac()
            playenemy()
        print ('after game loop...')
        coping()

if __name__ == "__main__":
    main()