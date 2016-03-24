# coding:utf-8 
# watermelon chess
import pygame
import json
import random
from pygame.locals import *
from sys import exit
import pdb

BACKGROUND = 'images/watermelon.png'
BLACKTILE = 'images/black.png'
WHITETILE = 'images/white.png'
HAND = 'images/hand.png'
START_IMAGE = 'images/start.png'
REPLAY_IMAGE = 'images/replay.png'
SCREEN_WIDTH = 580
SCREEN_HEIGHT = 580
FULLSCREENMOD = False 
BLACK = 1
WHITE = 2
COMPUTER = 2
PLAYER = 1

choose = False
source = None
target = None
global checkedTile
checkedTile = []
global computerTileSum
computerTileSum = 6
global playerTileSum
playerTileSum = 6
PLAYER_COLOR = WHITE

pointPos = [] #positions of the 21 points
tilePos = [0] * 21 #whether there is a tile

def move(tile, target):
    pass

def nearPoint((x, y)):
    x, y = x/(SCREEN_WIDTH+0.0),y/(SCREEN_HEIGHT+0.0)
    for point in range(21):
        if abs(x - pointPos[point][0]) < 0.05 and abs(y - pointPos[point][1]) <0.05:
            return point
    return None

def getPointPos():
    f = open('pointPos.txt', 'rb')
    try:
        pointPos = json.loads(f.read())
        return pointPos
    except:
        print 'file open error'
        exit()
    finally:
        f.close()

def getDistance():
    try:
        f = open('distance.txt', 'rb')
        distance = json.loads(f.read())
        return distance 
    except:
        print 'file open error'
        exit()
    finally:
        f.close()

def initTilePos():
    for x in range(21):
        tilePos[x] = 0
    tilePos[0] = tilePos[1] = tilePos[2] = tilePos[3] = tilePos[8] = tilePos[4] = 1 #black
    tilePos[15] = tilePos[13] = tilePos[14] = tilePos[12] = tilePos[7] = tilePos[11] = 2 #white
    return tilePos

def getXY(target):
    x = pointPos[target][0] * SCREEN_WIDTH - mouse_cursor.get_width()*0.7
    y = pointPos[target][1] * SCREEN_HEIGHT - mouse_cursor.get_width()*0.8
    return (x, y)

def goesFirst():
    i = random.randint(0, 1)
    first = [PLAYER, COMPUTER]
    return first[i]

def getNearbyTile(tile):
    nearbyTiles = []
    for index, eachDistance in enumerate(distance[tile]):
        if eachDistance == 1:
            nearbyTiles.append(index)
    return nearbyTiles

def computerMove():
    move = []
    for indexSource, tile in enumerate(tilePos):
        if tile == BLACK:
            for indexTarget in getNearbyTile(indexSource):
                if tilePos[indexTarget] == 0:
                    move.append((indexSource, indexTarget))
    if not move:
        return None
    return random.choice(move) 

def check(tile):
    print 'tile:', tile
    checkedTile.append(tile)
    dead = True
    nearbyTiles = getNearbyTile(tile)
    for nearbyTile in nearbyTiles:
        if nearbyTile not in checkedTile:
            if tilePos[nearbyTile] == tilePos[tile]:
                dead = check(nearbyTile)
                if dead == False:
                    return dead
            elif tilePos[nearbyTile] == 0:
                dead = False
                return dead
            else:
                pass
    return dead

def checkAll():
    deadTile = []
    for index, tileColor in enumerate(tilePos):
        global checkedTile
        checkedTile = []
        dead = True
        print 'index:', index
        if tileColor != 0:
            #pdb.set_trace()
            dead = check(index)
            if dead:
                deadTile.append(index)
                if tileColor == BLACK:
                    global computerTileSum
                    computerTileSum -= 1
                else:
                    global playerTileSum
                    playerTileSum -= 1
                print 'kill', index
        else:
            pass
    for eachDeadTile in deadTile:
        tilePos[eachDeadTile] = 0
def initGame():
    global computerTileSum
    computerTileSum = 6
    global playerTileSum
    playerTileSum = 6
    initTilePos()
    return 'init game ok, player goes first with white chess, press f to fullscreen'

pygame.init()
pointPos = getPointPos()
distance = getDistance()
tilePos = initTilePos()
#turn = goesFirst()
turn = 1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('西瓜棋')
background = pygame.image.load(BACKGROUND).convert()
mouse_cursor = pygame.image.load(BLACKTILE).convert_alpha()
blackTile = pygame.image.load(BLACKTILE).convert_alpha()
whiteTile = pygame.image.load(WHITETILE).convert_alpha()
hand = pygame.image.load(HAND).convert_alpha()
startImage = pygame.image.load(START_IMAGE).convert_alpha()
replayImage = pygame.image.load(REPLAY_IMAGE).convert_alpha()

myFont = pygame.font.SysFont('arial', 18)

message = initGame()

while True:
    if computerTileSum < 3:
        print 'game over'
        message = 'game over, player win!'
        #exit()
    if playerTileSum < 3:
        print 'game over'
        message = 'game over, computer win!'
        #exit()
    if turn == PLAYER:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_f:
                    FULLSCREENMOD = not FULLSCREENMOD
                    if FULLSCREENMOD:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 490 < x < 560 and 300 < y < 330:
                    message = initGame()

            if event.type == MOUSEBUTTONDOWN and turn == PLAYER:
                x, y = pygame.mouse.get_pos()
                if not choose:
                    source = nearPoint((x, y)) #choose source tile
                    if source:
                        if tilePos[source] == PLAYER_COLOR:
                            choose = True
                            chooseColor = tilePos[source]
                            tilePos[source] = 0

                else:
                    target = nearPoint((x, y)) #choose target tile
                    if target:
                        if tilePos[target] == 0 and distance[source][target] == 1:
                            tilePos[target], tilePos[source] = chooseColor, 0
                            turn = COMPUTER

                            tempTilePos = tilePos
                            checkAll()
                            if tempTilePos != tilePos:
                                print 'checked and changed'
                                message = 'white chess was ate'
                        else:
                            tilePos[source] = chooseColor
                            print 'target too far'
                            message = 'target too far'
                    else:
                        print 'target error'
                        message = 'target error'
                        tilePos[source] = chooseColor
                    choose = False

        
    elif turn == COMPUTER:
        move = computerMove()
        if not move:
            print 'game over'
            message = 'game over, player win!'
            #exit()
        (sourceCOM, targetCOM) = move
        tilePos[targetCOM], tilePos[sourceCOM] = BLACK, 0
        tempTilePos = tilePos
        checkAll()
        if tempTilePos != tilePos:
            print 'checked and changed'
            message = 'black chess was ate'
        turn = PLAYER
    else:
        print 'turn error'
        exit()

    handX, handY = pygame.mouse.get_pos()
    handX -= mouse_cursor.get_width() / 2
    handY -= mouse_cursor.get_height() /2
    pygame.mouse.set_visible(False)
    screen.blit(background, (0,0))
    #screen.blit(startImage, (490, 200))
    screen.blit(replayImage, (490, 300))
    for index, tile in enumerate(tilePos):
        if tile != 0:
            (x, y) = getXY(index)
            if tile == 1:
                screen.blit(blackTile, (x, y)) 
            elif tile ==2:
                screen.blit(whiteTile, (x, y))
            else:
                print 'tilePos error'
                exit()
    if choose:
        if chooseColor == 1:
            screen.blit(blackTile, (handX, handY))
        elif chooseColor == 2:
            screen.blit(whiteTile, (handX, handY))
    text_surface = myFont.render(message, True, (0, 0, 0), (102, 204, 255))
    screen.blit(text_surface, (0,500))
    screen.blit(hand, (handX, handY))
    pygame.display.update()
    
