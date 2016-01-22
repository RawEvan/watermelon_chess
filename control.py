#coding:utf-8
#class of control
import pygame
import data
import pdb
import random
import urllib
import urllib2
import json
import time
from pygame.locals import *

def inRect((x, y), rect, game):
    if rect[0][0] < x < rect[0][0]+rect[1]\
            and rect[0][1] < y < rect[0][1]+rect[2]\
            and rect in game.enableButton:
        return True
    else:
        return False

def chosenButton((x, y), game):
    if inRect((x, y), data.LOCALGAME_RECT, game):
        return 'localGame'
    elif inRect((x, y), data.NETWORKGAME_RECT, game):
        return 'networkGame'
    elif inRect((x, y), data.MENU_QUIT_RECT, game):
        return 'quit'
    elif inRect((x, y), data.BACK_RECT, game):
        return 'back'
    elif inRect((x, y), data.REPLAY_RECT, game):
        return 'replay'
    elif inRect((x, y), data.CONFIRM_RECT, game):
        return 'confirm'
    elif inRect((x, y), data.CANCEL_RECT, game):
        return 'cancel'
    else:
        return None

def chosenChessman((x, y), gameMap):
    x, y = x/(data.SCREEN_WIDTH+0.0),y/(data.SCREEN_HEIGHT+0.0)
    for point in range(21):
        if abs(x - gameMap[point][0]) < 0.05 and abs(y - gameMap[point][1]) <0.05:
            return point
    return None

def getNeighboors(chessman, game):
    neighboorChessmen= []
    for eachChessman, eachDistance in enumerate(game.distance[chessman]):
        if eachDistance == 1:
            neighboorChessmen.append(eachChessman)
    return neighboorChessmen 

def computerMove(game):
    move = []
    for chessman, color in enumerate(game.pointStatus):
        if color == game.opponentColor:
            for neighboorChessman in getNeighboors(chessman, game):
                if game.pointStatus[neighboorChessman] == 0:
                    move.append((chessman, neighboorChessman))
    if not move:
        return None
    return random.choice(move) 


def check(chessman, game):
    game.checkedChessmen.append(chessman)
    dead = True
    neighboorChessmen = getNeighboors(chessman, game)
    for neighboorChessman in neighboorChessmen:
        if neighboorChessman not in game.checkedChessmen:
            #if the neighboor is the same color, check the neighboor to find a empty neighboor
            if game.pointStatus[neighboorChessman] == game.pointStatus[chessman]:
                dead = check(neighboorChessman, game)
                if dead == False:
                    return dead
            elif game.pointStatus[neighboorChessman] == 0:
                dead = False
                return dead
            else:
                pass
    return dead

def checkAll(game):
    if game.chessBoard.blackNum < 3 or game.chessBoard.whiteNum < 3:
        game.status = 'query'
        game.over = True
        if game.chessBoard.blackNum < 3:
            winner = data.WHITE
        else:
            winner = data.BLACK
        if game.playerColor == winner:
            game = setQuery(game, 'play', 'menu', 'You win!')
        else:
            game = setQuery(game, 'play', 'menu', 'You lose~')
        return game
    game.deadChessmen = []
    for chessman, color in enumerate(game.pointStatus):
        game.checkedChessmen = []
        dead = True
        if color != 0:
            #pdb.set_trace()
            dead = check(chessman, game)
            if dead:
                game.deadChessmen.append(chessman)
                if color == data.BLACK:
                    game.chessBoard.blackNum -= 1
                else:
                    game.chessBoard.whiteNum -= 1
        else:
            pass
    for eachDeadChessman in game.deadChessmen:
        game.pointStatus[eachDeadChessman] = 0

    return game

def setQuery(game, lastStatus, nextStatus, msg):
    game.lastStatus = lastStatus
    game.nextStatus = nextStatus
    game.enableButton = [data.CONFIRM_RECT, data.CANCEL_RECT]
    game.msg = msg
    return game

def post(roomID, action, name, url, pointStatus = None):  
    parameters = {'roomID': roomID, 'action': action, 'name': name, 'pointStatus': pointStatus}
    postData = urllib.urlencode(parameters)  
    req = urllib2.Request(url, postData)
    req.add_header('Content-Type', "application/x-www-form-urlencoded")
    response = urllib2.urlopen(req)  
    jsonData = response.read()  
    return json.loads(jsonData) 

def initNetworkGame(game):
    response = post('', 'enter', '', game.url)
    if response['playerNum'] == '1':
        game.name = response['player1']
        game.playerColor = data.WHITE
        game.opponentColor = data.BLACK
    else:
        game.name = response['player2']
        game.playerColor = data.BLACK
        game.opponentColor = data.WHITE
    game.roomID = response['roomID']
    post(game.roomID, 'pre', game.name, game.url)
    return game

def sendData(game):
    response = post(game.roomID, 'play', game.name, game.url, json.dumps(game.pointStatus))

def getData(game):
    response = post(game.roomID, 'query', game.name, game.url)
    return response

def resetRoom(game):
    response = post(game.roomID, 'leave', game.name, game.url)

#set a time interval
def clock(game):
    if time.time() - game.time > 0.8:
        return True
    else:
        return False

def playControl(event, game):
    if game.turn == 'none':
        if clock(game):
            response= getData(game)
            game.msg = 'preparing' + time.ctime()
            game.time = time.time()#reset the clock after connection
            if response['preOK']:
                game.turn = response['turn']
                if game.name == response['player1']:
                    game.opponent = response['player2']
                else:
                    game.opponent = response['player1']
                game.msg = 'turn:' + game.turn
    elif game.turn == game.name:
        #for temp
        if game.playerColor == data.BLACK:
            color = 'BLACK'
        else:
            color = 'WHITE'
        game.msg = "it's your turn to move with " + color 
        chessman = None
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            button = chosenButton((x, y), game)
            chessman = chosenChessman((x, y), game.gameMap)
            if button == 'replay':
                game.status = 'query'
                game = setQuery(game, 'play', 'play', 'Reset the game?')
            elif button == 'back':
                game.status = 'query'
                game = setQuery(game, 'play', 'menu', 'Back to menu?')
            else:
                pass
        if chessman != None:
            if game.chessmanInHand == False:
                if game.pointStatus[chessman] == game.playerColor:
                        game.chosenChessmanColor = game.pointStatus[chessman]
                        game.pointStatus[chessman] = 0
                        game.chessmanInHand = True
                        game.chosenChessman = chessman
                        game.msg = 'Chessman was chose'
            else:
                if game.pointStatus[chessman] == 0 and\
                        game.distance[game.chosenChessman][chessman] == 1:
                    game.pointStatus[chessman] = game.chosenChessmanColor
                    game.msg = 'Chessman was moved'
                    if game.isOnline:
                        game.turn = game.opponent
                        sendData(game)
                        game.time = time.time()
                    else:
                        game.turn = 'computer'
                else:
                    game.pointStatus[game.chosenChessman] = game.chosenChessmanColor
                    game.msg = 'not a valid choice'
                game.chessmanInHand = False
            
    elif game.turn == 'computer':
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            button = chosenButton((x, y), game)
            chessman = chosenChessman((x, y), game.gameMap)
            if button == 'replay':
                game.status = 'query'
                game = setQuery(game, 'play', 'play', 'Reset the game?')
            elif button == 'back':
                game.status = 'query'
                game = setQuery(game, 'play', 'menu', 'Back to menu?')
            else:
                pass
        move = computerMove(game)
        if move:
            source, target = computerMove(game)
            game.pointStatus[move[1]] = game.opponentColor
            game.pointStatus[move[0]] = 0
            game.turn = game.name

    elif game.turn == game.opponent:
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            button = chosenButton((x, y), game)
            chessman = chosenChessman((x, y), game.gameMap)
            if button == 'replay':
                game.status = 'query'
                game = setQuery(game, 'play', 'play', 'Reset the game?')
            elif button == 'back':
                game.status = 'query'
                game = setQuery(game, 'play', 'menu', 'Back to menu?')
            else:
                pass
        if clock(game):
            response = getData(game)
            game.msg = time.ctime() + "  waiting for you opponent's movement"
            game.time = time.time()
            if response['turn'] == game.name:
                game.pointStatus = json.loads(response['pointStatus'])
                game.turn = game.name
    else:
        pass 
    game = checkAll(game)
    return game

def menuControl(event, game):
    if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        button = chosenButton((x, y), game)
        if button == 'localGame':
            game.resetGame()
            game.status = 'play'
            game.isOnline = False
            game.name = 'local'
            game.turn = game.name
            game.opponentColor = data.BLACK
            game.enableButton = [data.BACK_RECT, data.REPLAY_RECT]
        elif button == 'networkGame':
            game.resetGame()
            game.status = 'play'
            game.isOnline = True
            game = initNetworkGame(game)
            game.msg =  time.ctime() + '  enter room: ' + game.roomID + ' get name: ' + game.name
            game.time = time.time()
            game.enableButton = [data.BACK_RECT, data.REPLAY_RECT]

        elif button == 'quit':
            game.status = 'query'
            game = setQuery(game, 'menu', 'quit', 'Quit the game?')
        else:
            pass
    return game

def queryControl(event, game):
    if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        button = chosenButton((x, y), game)
        if button == 'confirm':
            game.resetGame()
            game.status = game.nextStatus
        elif button == 'cancel':
            if game.over:
                game.resetGame()
            game.status = game.lastStatus
        else:
            pass

        if game.status == 'menu':
            game.enableButton = [data.LOCALGAME_RECT, data.NETWORKGAME_RECT, data.MENU_QUIT_RECT]
            if game.isOnline:
                resetRoom(game)
        elif game.status == 'play':
            game.enableButton = [data.BACK_RECT, data.REPLAY_RECT]
    return game

def eventControl(event, game): 
    if event.type == QUIT:
        pdb.set_trace()
        game.lastStatus = game.status
        game.status = 'query'
        game = setQuery(game, game.lastStatus, 'quit', 'Quit the game?')

    elif event.type == KEYDOWN:
        if event.key == K_q:
            #pdb.set_trace()
            game.lastStatus = game.status
            game.status = 'query'
            game = setQuery(game, game.lastStatus, 'quit', 'Quit the game?')
        elif event.key == K_f:
            if game.fullScreenMod == 0:
                game.fullScreenMod = FULLSCREEN
            else:
                game.fullScreenMod = 0
            game.fullScreenModChanged = True

    else:
        if game.status == 'menu':
            game = menuControl(event, game)
        elif game.status == 'play':
            game = playControl(event, game)
        elif game.status == 'query':
            game = queryControl(event, game)
        else:
            pass
    
    return game
