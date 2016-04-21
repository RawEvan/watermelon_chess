# coding:utf-8
# class of control
import pygame
import data
import pdb
import random
import urllib
import urllib2
import json
import time
import copy
from pygame.locals import *


# difficulty of the game 
DEEPEST_LEVEL = 3

def inRect((x, y), rect, game):
    if rect[0][0] < x < rect[0][0] + rect[1]\
            and rect[0][1] < y < rect[0][1] + rect[2]\
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
    x, y = x / (data.SCREEN_WIDTH + 0.0), y / (data.SCREEN_HEIGHT + 0.0)
    for point in range(21):
        if abs(x - gameMap[point][0]) < 0.05 and abs(y - gameMap[point][1]) < 0.05:
            return point
    return None


def getNeighboors(chessman, distance):
    neighboorChessmen = []
    for eachChessman, eachDistance in enumerate(distance[chessman]):
        if eachDistance == 1:
            neighboorChessmen.append(eachChessman)
    return neighboorChessmen


def getScore(pointStatus, distance):
    score = 0
    scoreLevel = [1, 2, 4, 6]
    black = [x for x in distance if x == data.BLACK]
    # if chessman was eaten, sub 8 score for each one
    score -= 8 * (6 - len(black))
    for chessman, color in enumerate(pointStatus):
        advantg = 0
        disadvtg = 0
        neighboors = getNeighboors(chessman, distance)
        for eachNeighboor in neighboors:
            # computer use black chessman as default
            if pointStatus[eachNeighboor] == data.BLACK and color == data.WHITE:
                advantg += 1
                score += scoreLevel[advantg - 1]
            elif pointStatus[eachNeighboor] == data.WHITE and color == data.BLACK:
                disadvtg += 1
                score -= scoreLevel[disadvtg - 1]
            else:
                pass
            # unnecessary
            '''
            elif color == data.WHITE:
                if pointStatus[eachNeighboor] == data.BLACK:
                    score += 2
                elif pointStatus[eachNeighboor] == data.WHITE:
                    score -= 2
            '''
    return score


def computerMove(pointStatus, distance, level):
    move = []
    maxScore = -48
    bestMove = None
    # for convenient, set color = computer color (black) when enter the
    # function firstly
    if level % 2 == 1:
        selfColor = data.BLACK
        opponentColor = data.WHITE
    else:
        selfColor = data.WHITE
        opponentColor = data.WHITE
    # In the deepest level, the best move is itself, replace it with None
    if level > DEEPEST_LEVEL:
        score = getScore(pointStatus, distance)
        return [], score
    else:
        for chessman, color in enumerate(pointStatus):
            if color == selfColor:
                for neighboorChessman in getNeighboors(chessman, distance):
                    if pointStatus[neighboorChessman] == 0:
                        move.append((chessman, neighboorChessman))
        if not move:
            return [], -49
        bakPointStatus = copy.deepcopy(pointStatus)
        for eachMove in move:
            pointStatus[eachMove[1]] = selfColor
            pointStatus[eachMove[0]] = 0
            pointStatus = shiftOutChessman(pointStatus, distance)
            # newMove is useless, just for return the best move in the first
            # level
            newMove, score = computerMove(pointStatus, distance, level + 1)
            if score > maxScore:
                maxScore = score
                bestMove = eachMove
            # revoke the change
            pointStatus = copy.deepcopy(bakPointStatus)
        return bestMove, maxScore


def checkWinner(game):
    game.chessBoard.blackNum = 0
    game.chessBoard.whiteNum = 0
    for color in game.pointStatus:
        if color == data.BLACK:
            game.chessBoard.blackNum += 1
        elif color == data.WHITE:
            game.chessBoard.whiteNum += 1
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


def check(chessman, distance, pointStatus, checkedChessmen):
    checkedChessmen.append(chessman)
    dead = True
    neighboorChessmen = getNeighboors(chessman, distance)
    for neighboorChessman in neighboorChessmen:
        if neighboorChessman not in checkedChessmen:
            # if the neighboor is the same color, check the neighboor to find a
            # empty neighboor
            if pointStatus[neighboorChessman] == pointStatus[chessman]:
                dead = check(neighboorChessman, distance,
                             pointStatus, checkedChessmen)
                if dead == False:
                    return dead
            elif pointStatus[neighboorChessman] == 0:
                dead = False
                return dead
            else:
                pass
    return dead


def shiftOutChessman(pointStatus, distance):
    deadChessmen = []
    bakPointStatus = copy.deepcopy(pointStatus)
    for chessman, color in enumerate(pointStatus):
        checkedChessmen = []
        dead = True
        if color != 0:
            # pdb.set_trace()
            dead = check(chessman, distance, pointStatus, checkedChessmen)
        else:
            pass
        if dead:
            deadChessmen.append(chessman)
        pointStatus = bakPointStatus
    for eachDeadChessman in deadChessmen:
        pointStatus[eachDeadChessman] = 0

    return pointStatus


def setQuery(game, lastStatus, nextStatus, msg):
    game.lastStatus = lastStatus
    game.nextStatus = nextStatus
    game.enableButton = [data.CONFIRM_RECT, data.CANCEL_RECT]
    game.msg = msg
    return game


def post(roomID, action, name, url, pointStatus=None):
    parameters = {'roomID': roomID, 'action': action,
                  'name': name, 'pointStatus': pointStatus}
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
    response = post(game.roomID, 'play', game.name,
                    game.url, json.dumps(game.pointStatus))


def getData(game):
    response = post(game.roomID, 'query', game.name, game.url)
    return response


def resetRoom(game):
    response = post(game.roomID, 'leave', game.name, game.url)

# set a time interval


def clock(game):
    if time.time() - game.time > 0.8:
        return True
    else:
        return False


def checkOpponent(game):
    newPointStatus = game.pointStatus
    if clock(game):
        response = getData(game)
        print response
        game.msg = time.ctime() + "waiting for you opponent's movement"
        game.time = time.time()
        game.turn = response['turn']
        try:
            newPointStatus = json.loads(response['pointStatus'])
        except:
            pass
        if not response['turn']:
            game.status = 'query'
            game = setQuery(game, 'play', 'menu',
                            'Your opponent ran away~ return pls')
            game.enableButton = [data.CONFIRM_RECT]
    return game, newPointStatus


def playControl(event, game):
    color = game.strColor(game.playerColor)
    chessman = None
    button = None
    if event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        button = chosenButton((x, y), game)
        chessman = chosenChessman((x, y), game.gameMap)

    if button:
        if button == 'replay':
            game.status = 'query'
            game = setQuery(game, 'play', 'play', 'Reset the game?')
        elif button == 'back':
            game.status = 'query'
            game = setQuery(game, 'play', 'menu', 'Back to menu?')
        else:
            pass
    else:
        if game.turn == 'none':
            if clock(game):
                response = getData(game)
                game.msg = 'preparing' + time.ctime()
                game.time = time.time()  # reset the clock after connection
                if response['preOK']:
                    game.turn = response['turn']
                    if game.name == response['player1']:
                        game.opponent = response['player2']
                    else:
                        game.opponent = response['player1']
                    game.msg = 'turn:' + game.turn
        elif game.turn == game.name:
            game.msg = "it's your turn to move with " + color
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
                        bakPointStatus = copy.deepcopy(game.pointStatus)
                        game.pointStatus = shiftOutChessman(
                            bakPointStatus, game.distance)
                        game = checkWinner(game)
                        if game.isOnline:
                            game.turn = game.opponent
                            sendData(game)
                            game.time = time.time()
                        else:
                            game.turn = 'computer'
                    else:
                        game.pointStatus[
                            game.chosenChessman] = game.chosenChessmanColor
                        game.msg = 'not a valid choice'
                    game.chessmanInHand = False
            if game.isOnline:
                game, newPointStatus = checkOpponent(game)

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
            bakPointStatus = copy.deepcopy(game.pointStatus)
            move, score = computerMove(bakPointStatus, game.distance, 1)
            game.pointStatus[move[1]] = game.opponentColor
            game.pointStatus[move[0]] = 0
            game.turn = game.name
            bakPointStatus = copy.deepcopy(game.pointStatus)
            game.pointStatus = shiftOutChessman(bakPointStatus, game.distance)
            game = checkWinner(game)

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
            game, newPointStatus = checkOpponent(game)
            if game.turn == game.name:
                game.pointStatus = newPointStatus
            bakPointStatus = copy.deepcopy(game.pointStatus)
            game.pointStatus = shiftOutChessman(bakPointStatus, game.distance)
            game = checkWinner(game)
        else:
            pass
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
            # pdb.set_trace()
            game = initNetworkGame(game)
            game.msg = time.ctime() + '  enter room: ' + game.roomID + \
                ' get name: ' + game.name
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
            if game.nextStatus == 'play':
                game.enableButton = [data.BACK_RECT, data.REPLAY_RECT]
                if game.over:
                    game.resetGame()
            else:
                if game.nextStatus == 'menu':
                    game.enableButton = [data.LOCALGAME_RECT,
                                         data.NETWORKGAME_RECT, data.MENU_QUIT_RECT]
                # if menu or quit
                if game.isOnline:
                    resetRoom(game)
        elif button == 'cancel':
            game.status = game.lastStatus
        else:
            pass

    return game


def eventControl(event, game):
    if event.type == QUIT:
        game.lastStatus = game.status
        game.status = 'query'
        game = setQuery(game, game.lastStatus, 'quit', 'Quit the game?')

    elif event.type == KEYDOWN:
        if event.key == K_q:
            # pdb.set_trace()
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
