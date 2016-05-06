# coding:utf-8
# class of chessboard
#from chessman import chessman
import data
import json


class ChessBoard():

    def __init__(self):
        self.gameMap = []
        self.pointStatus = []
        self.distance = []
        self.status = None
        self.whiteNum = 6
        #self.whiteChessmen = chessman(WHITE)[6]
        self.blackNum = 6
        #self.blackChessmen = chessman(BLACK)[6]
        self.msg = None
        self.initDistance()
        self.initPointStatus()
        self.initGameMap()

    def getGameMap(self):
        return self.gameMap

    def getPointStatus(self):
        return self.pointStatus

    def getDistance(self):
        return self.distance

    def initDistance(self):
        try:
            f = open(data.DISTANCEPATH, 'rb')
            self.distance = json.loads(f.read())
        except Exception, e:
            print 'file open error', e
        finally:
            f.close()

    def initPointStatus(self):
        self.pointStatus = []
        black = [0,1,2,3,4,8]
        white = [7,11,12,13,14,15]
        for x in range(21):
            self.pointStatus.append(0)
        for x in black:
            self.pointStatus[x] = data.BLACK
        for x in white:
            self.pointStatus[x] = data.WHITE

    def initChessmanNum(self):
        self.whiteNum = 6
        self.blackNum = 6

    def initGameMap(self):
        try:
            f = open(data.MAPPATH, 'rb')
            pointPos = json.loads(f.read())
            self.gameMap = pointPos
        except Exception, e:
            print 'file open error', e
        finally:
            f.close()
