from Piece import Piece
from Pos import Pos
from base import *

class Horse(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.horse, pos, rb, context)
    def getScore(self):
        if self.isDie():
            return 0
        return 3
    def CanMoveList(self):
        l = []
        ml = [
            Pos(self.pos.x-2, self.pos.y-1),
        Pos(self.pos.x-2, self.pos.y+1),
        Pos(self.pos.x+2, self.pos.y-1),
        Pos(self.pos.x+2, self.pos.y+1),
        Pos(self.pos.x-1, self.pos.y-2),
        Pos(self.pos.x-1, self.pos.y+2),
        Pos(self.pos.x+1, self.pos.y-2),
        Pos(self.pos.x+1, self.pos.y+2)
        ]        
        for m in ml:
            if m.x>=0 and m.x<=8 and m.y>=0 and m.y<=9 and self.isCanMove(m):
                l.append(m)
        return l

    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        dx = pos.x-self.pos.x
        dy = pos.y-self.pos.y
        lame = False
        if dx==-1:
            if dy==-2:
                lame = (self.context.getPiece(self.pos.x, self.pos.y-1) != None) # is lame horse?
            elif dy==2:
                lame = (self.context.getPiece(self.pos.x, self.pos.y+1) != None)
            else:
                return False
        elif dx==1:
            if dy==-2:
                lame = (self.context.getPiece(self.pos.x, self.pos.y-1) != None) # is lame horse?
            elif dy==2:
                lame = (self.context.getPiece(self.pos.x, self.pos.y+1) != None)
            else:
                return False
        elif dx==-2:
            if dy==-1:
                lame = (self.context.getPiece(self.pos.x-1, self.pos.y) != None)
            elif dy==1:
                lame = (self.context.getPiece(self.pos.x-1, self.pos.y) != None)
            else:
                return False
        elif dx==2:
            if dy==-1:
                lame = (self.context.getPiece(self.pos.x+1, self.pos.y)!=None)
            elif dy==1:
                lame = (self.context.getPiece(self.pos.x+1, self.pos.y)!=None)
            else:
                return False
        else:
            return False

        if lame :
            return False
        
        if p == None:
            return True
        
        return p.getSide() != self.getSide()
