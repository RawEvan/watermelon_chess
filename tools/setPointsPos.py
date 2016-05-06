# coding:utf-8
# watermelon chess
import pygame
import json
from pygame.locals import *
from sys import exit
BACKGROUND = '../resources/images/watermelon.png'
BLACKTILE = '../resources/images/black.png'
WHITETILE = '../resources/images/white.png'
HAND = '../resources/images/hand.png'
SCREEN_WIDTH = 580
SCREEN_HEIGHT = 580
FULLSCREENMOD = False
count = 0
pointPos = []  # positions of the 21 points

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(u'watermelon chess')
background = pygame.image.load(BACKGROUND).convert()
mouse_cursor = pygame.image.load(BLACKTILE).convert_alpha()
blackTile = pygame.image.load(BLACKTILE).convert_alpha()
whiteTile = pygame.image.load(WHITETILE).convert_alpha()
hand = pygame.image.load(HAND).convert_alpha()


def move(tile, target):
    pass


def nearPoint((x, y)):
    x, y = x / (SCREEN_WIDTH + 0.0), y / (SCREEN_HEIGHT + 0.0)
    for point in range(21):
        if abs(x - pointPos[point][0]) < 0.1 and abs(y - pointPos[point][1]) < 0.1:
            return point
    return None


def getPointsPosition():
        # get 21 point of the chess
    '''
    if event.type == MOUSEBUTTONDOWN and count < 21:
        x, y = pygame.mouse.get_pos()
        x, y = (x / (SCREEN_WIDTH+0.0), y / (SCREEN_HEIGHT+0.0))
        temp = [x, y]
        pointPos.append(temp)
        count = count + 1
        print list
    if count >= 21:
        f.write(json.dumps(list))
        '''
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                FULLSCREENMOD = not FULLSCREENMOD
                if FULLSCREENMOD:
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        if event.type == MOUSEBUTTONDOWN and count < 21:
            x, y = pygame.mouse.get_pos()
            x, y = (x / (SCREEN_WIDTH + 0.0), y / (SCREEN_HEIGHT + 0.0))
            temp = [x, y]
            pointPos.append(temp)
            count = count + 1
            print pointPos
        if count == 21:
            try:
                f = open('../resources/pointPos.txt', 'wb')
            except:
                print 'file open error'
            f.write(json.dumps(pointPos))
            f.close()
            print 'write!'
    x, y = pygame.mouse.get_pos()
    x -= mouse_cursor.get_width() / 2
    y -= mouse_cursor.get_height() / 2
    pygame.mouse.set_visible(False)
    screen.blit(background, (0, 0))
    screen.blit(blackTile, (100, 10))
    screen.blit(whiteTile, (100, 100))
    screen.blit(hand, (x, y))
    pygame.display.update()
