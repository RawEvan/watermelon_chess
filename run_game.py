# coding:utf-8
# display
import pygame
import sys
import data
import pdb
from control import eventControl
from game import Game
from pygame.locals import *


class UI():

    def __init__(self, name):
        pygame.init()
        self.playerName = name
        self.game = Game()
        self.setScreen()
        pygame.display.set_caption('西瓜棋')
        pygame.mouse.set_visible(False)
        self.background = pygame.image.load(data.BACKGROUND).convert()
        self.mouse_cursor = pygame.image.load(data.BLACKTILE).convert_alpha()
        self.blackTile = pygame.image.load(data.BLACKTILE).convert_alpha()
        self.whiteTile = pygame.image.load(data.WHITETILE).convert_alpha()
        self.hand = pygame.image.load(data.HAND).convert_alpha()
        self.menuImage = pygame.image.load(data.MENU).convert()
        self.startImage = pygame.image.load(data.START).convert_alpha()
        self.replayImage = pygame.image.load(data.REPLAY).convert_alpha()
        self.backImage = pygame.image.load(data.BACK).convert_alpha()
        self.localGameImage = pygame.image.load(data.LOCALGAME).convert_alpha()
        self.networkGameImage = pygame.image.load(
            data.NETWORKGAME).convert_alpha()
        self.quitImage = pygame.image.load(data.QUIT).convert_alpha()
        self.msgFont = pygame.font.Font(data.FONT, 20)
        self.queryFont = pygame.font.Font(data.FONT, 30)
        self.queryBkgImage = pygame.image.load(data.QUERY_BKG).convert()
        self.confirmImage = pygame.image.load(data.CONFIRM).convert_alpha()
        self.cancelImage = pygame.image.load(data.CANCEL).convert_alpha()
        self.displayMenu()

    def eventManagement(self):
        while True:
            if self.game.status == 'quit':
                return
            else:
                for event in pygame.event.get():
                    self.game = eventControl(event, self.game)
                    if self.game.status == 'menu':
                        self.displayMenu()
                    elif self.game.status == 'play':
                        self.displayPlay()
                    elif self.game.status == 'query':
                        self.displayQuery()
                    elif self.game.status == 'over':
                        self.displayGameOver()

    def displayMenu(self):
        self.setScreen()
        self.screen.blit(self.menuImage, (0, 0))
        self.screen.blit(self.localGameImage, data.LOCALGAME_RECT[0])
        self.screen.blit(self.networkGameImage, data.NETWORKGAME_RECT[0])
        self.screen.blit(self.quitImage, data.MENU_QUIT_RECT[0])
        self.blitMouse()
        pygame.display.update()

    def displayPlay(self):
        self.setScreen()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.backImage, data.BACK_RECT[0])
        self.screen.blit(self.replayImage, data.REPLAY_RECT[0])
        self.text_surface = self.msgFont.render(
            self.game.msg, True, (102, 204, 255), (255, 255, 255))

        color = self.game.strColor(self.game.playerColor)
        sideText = ['your name:' + str(self.game.name),
                    'your color:' + color,
                    'turn:' + str(self.game.turn),
                    'room:' + str(self.game.roomID),
                    "'q' to quit",
                    "'f' to fullscreen"]
        sideY = 5
        for text in sideText:
            self.sideSurface = self.msgFont.render(
                text, True, (102, 204, 255), (255, 255, 255))
            self.screen.blit(self.sideSurface, (430, sideY))
            sideY += 25
        self.screen.blit(self.text_surface, (10, 500))
        self.blitChessmen()
        self.blitMouse()
        pygame.display.update()

    def displayQuery(self):
        self.setScreen()
        self.screen.blit(self.queryBkgImage, (0, 0))
        self.text_surface = self.queryFont.render(
            self.game.msg, True, (102, 204, 255), (255, 255, 255))
        self.screen.blit(self.text_surface, (160, 200))
        self.screen.blit(self.confirmImage, data.CONFIRM_RECT[0])
        self.screen.blit(self.cancelImage, data.CANCEL_RECT[0])
        self.blitMouse()
        pygame.display.update()

    def setScreen(self):
        if self.game.fullScreenModChanged:
            self.screen = pygame.display.set_mode(
                (data.SCREEN_WIDTH, data.SCREEN_HEIGHT), self.game.fullScreenMod, 32)
            self.game.fullScreenModChanged = False

    def blitChessmen(self):
        for index, point in enumerate(self.game.pointStatus):
            if point != 0:
                (x, y) = self.fixXY(index)
                if point == 1:
                    self.screen.blit(self.blackTile, (x, y))
                elif point == 2:
                    self.screen.blit(self.whiteTile, (x, y))
                else:
                    self.game.msg = 'pointPos error'
        if self.game.chessmanInHand:
            if self.game.chosenChessmanColor == 1:
                self.screen.blit(self.blackTile, (self.handX, self.handY))
            else:
                self.screen.blit(self.whiteTile, (self.handX, self.handY))

    def blitMouse(self):
        self.handX, self.handY = pygame.mouse.get_pos()
        self.handX -= self.mouse_cursor.get_width() / 2
        self.handY -= self.mouse_cursor.get_height() / 2
        self.screen.blit(self.hand, (self.handX, self.handY))

    def fixXY(self, target):
        x = self.game.gameMap[target][0] * \
            data.SCREEN_WIDTH - data.CHESSMAN_WIDTH * 0.5
        y = self.game.gameMap[target][1] * \
            data.SCREEN_HEIGHT - data.CHESSMAN_HEIGHT * 1
        return (x, y)


def main():
    name = 'player1'
    ui = UI(name)
    ui.eventManagement()

if __name__ == '__main__':
    main()
