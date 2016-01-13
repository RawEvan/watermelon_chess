# coding:utf-8 
# watermelon chess
import pygame
import json
from pygame.locals import *
from sys import exit

BACKGROUND = 'images/watermelon.png'
BLACKTILE = 'images/black.png'
WHITETILE = 'images/white.png'
HAND = 'images/hand.png'
SCREEN_WIDTH = 423
SCREEN_HEIGHT = 424
FULLSCREENMOD = False 
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

def getXY(target):
    x = pointPos[target][0] * SCREEN_WIDTH - mouse_cursor.get_width()*0.8
    y = pointPos[target][1] * SCREEN_HEIGHT - mouse_cursor.get_width()*0.8
    return (x, y)

pygame.init()
pointPos = getPointPos()
distance = getDistance()
initTilePos()
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
while True:
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
            if not choose:
                source = nearPoint((x, y)) #source tile
                if source:
                    if tilePos[source] == 1 or tilePos[source] ==2:
                        choose = True
                        chooseColor = tilePos[source]
                        tilePos[source] = 0

            else:
                target = nearPoint((x, y)) #target tile
                if target:
                    if tilePos[target] == 0 and distance[source][target] == 1:
                        tilePos[target], tilePos[source] = chooseColor, 0
                    else:
                        print 'target error'
                        tilePos[source] = chooseColor
                else:
                    print 'target error'
                    tilePos[source] = chooseColor
                choose = False
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
