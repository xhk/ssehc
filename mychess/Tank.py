from Piece import Piece
from Pos import Pos
from base import *

class Tank(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.tank, pos, rb, context)
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        if self.pos.x == pos.x: # on the same vertical line
            if ( self.context.vertPieceCount(pos.x, self.pos.y, pos.y) == 0 ):
                if p==None: # no piece in the end
                    return True
                else :
                    return p.getSide() != self.getSide() # only eat other side 
            else:
                return False
        
        elif self.pos.y == pos.y: # on the same horizontal line
            if self.context.horzPieceCount(pos.y, self.pos.x, pos.x)==0:
                if p==None: # no piece in the end
                    return True
                else:
                    return p.getSide() != self.getSide()
            else:
                return False
        else:
            return False
        
        return False
    
    def getScore(self):
        if self.isDie():
            return 0
        
        if self.pos.x is 3 or self.pos.x is 5:
            return 6
        return 5
    def CanMoveList(self):
        l = []
        # left horz
        for x in range(self.pos.x-1, -1, -1):
            p = self.context.getPiece(x, self.pos.y)
            if p is None:
                l.append(Pos(x, self.pos.y))
            else:
                if p.getSide()!=self.getSide():
                    l.append(Pos(x, self.pos.y))
                break

        # right horz 
        for x in range(self.pos.x+1, 8+1):
            p = self.context.getPiece(x, self.pos.y)
            if p is None:
                l.append(Pos(x, self.pos.y))
            else:
                if p.getSide()!=self.getSide():
                    l.append(Pos(x, self.pos.y))
                break

        # up vertical
        for y in range(self.pos.y-1, -1, -1):
            p = self.context.getPiece(self.pos.x, y)
            if p is None:
                l.append(Pos(self.pos.x, y))
            else:
                if not self.sameSide(p):
                    l.append(Pos(self.pos.x, y))
                break
        # down vertical
        for y in range(self.pos.y+1, 9+1, 1):
            p = self.context.getPiece(self.pos.x, y)
            if p is None:
                l.append(Pos(self.pos.x, y))
            else:
                if not self.sameSide(p):
                    l.append(Pos(self.pos.x, y))
                break
        return l