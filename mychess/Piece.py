import Pos

from base import *

class Piece:
    red_names   = ['N', '车', '马', '相', '仕', '帅', '炮', '兵']
    black_names = ['N', '车', '马', '象', '士', '将', '砲', '卒']
    
    def __init__(self, pt, pos, rb, context):
        self.pos = pos
        self.rb  = rb # 红黑方
        self.pt  = pt
        self.move_list = [pos] # 轨迹
        self.context = context
        if self.rb == Side.red:
            self.name = Piece.red_names[int(self.pt.value)]
        else:
            self.name = Piece.black_names[int(self.pt.value)]

    def sameSide(self, p):
        return p.getSide() == self.rb

    def isDie(self):
        return self.pos.x == 9

    def die(self):
        self.pos.x = 9

        

    def CanMoveList(self):
        '''
        可落子点列表
        '''
        pass
    def isCanMove(self, pos):
        pass

    #  scored by position
    def getScore(self):
        pass

    def isMe(self, x, y):
        return self.pos.x == x and self.pos.y==y
    #def isMe(self, pos):
    #    return self.pos.x == pos.x and self.pos.y==pos.y   
    def MoveTo(self, pos):
        '''
            落子
        '''
        self.pos = pos
        self.move_list.append(pos)
        
    def getPos(self):
        return self.pos
    def getName(self):
        return self.name
    def getSide(self):
        return self.rb
   


