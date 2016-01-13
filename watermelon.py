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
SCREEN_WIDTH = 423
SCREEN_HEIGHT = 424
FULLSCREENMOD = False 
BLACK = 1
WHITE = 2
COMPUTER = 2
PLAYER = 1

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
    try:
        f = open('pointPos.txt', 'rb')
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
    tilePos[0] = tilePos[1] = tilePos[2] = tilePos[3] = tilePos[8] = tilePos[4] = 1 #black
    tilePos[15] = tilePos[13] = tilePos[14] = tilePos[12] = tilePos[7] = tilePos[11] = 2 #white
    return tilePos

def getXY(target):
    x = pointPos[target][0] * SCREEN_WIDTH - mouse_cursor.get_width()*0.8
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
        tilePos(eachDeadTile) = 0

pointPos = getPointPos()
distance = getDistance()
tilePos = initTilePos()
#turn = goesFirst()
turn = 1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(u'watermelon chess')
background = pygame.image.load(BACKGROUND).convert()
mouse_cursor = pygame.image.load(BLACKTILE).convert_alpha()
blackTile = pygame.image.load(BLACKTILE).convert_alpha()
whiteTile = pygame.image.load(WHITETILE).convert_alpha()
hand = pygame.image.load(HAND).convert_alpha()

choose = False
source = None
target = None
global checkedTile
checkedTile = []
global computerTileSum
computerTileSum = 6
global playerTileSum
playerTileSum = 6

while True:
    if computerTileSum < 3:
        print 'game over'
        exit()
    if playerTileSum < 3:
        print 'game over'
        exit()
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
                        else:
                            tilePos[source] = chooseColor
                            print 'target error'
                    else:
                        print 'target error'
                        tilePos[source] = chooseColor
                    choose = False

        
    elif turn == COMPUTER:
        move = computerMove()
        if not move:
            print 'game over'
            exit()
        (sourceCOM, targetCOM) = move
        tilePos[targetCOM], tilePos[sourceCOM] = BLACK, 0
        tempTilePos = tilePos
        checkAll()
        if tempTilePos != tilePos:
            print 'checked and changed'
        turn = PLAYER
    else:
        print 'turn error'
        exit()

    handX, handY = pygame.mouse.get_pos()
    handX -= mouse_cursor.get_width() / 2
    handY -= mouse_cursor.get_height() /2
    pygame.mouse.set_visible(False)
    screen.blit(background, (0,0))
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
    screen.blit(hand, (handX, handY))
    pygame.display.update()
    
