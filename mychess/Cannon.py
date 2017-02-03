from Piece import Piece
from Pos import Pos
from base import *

class Cannon(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.cannon, pos, rb, context)

    def CanMoveList(self):
        l = []

                 
        # left x
        have_shelf = False
        for x in range(self.pos.x-1, -1, -1):
            p = self.context.getPiece(x, self.pos.y)
            if p is None:
                if not have_shelf:
                    l.append(Pos(x, self.pos.y))
            else:
                if have_shelf:
                    if not self.sameSide(p):
                        l.append(Pos(x, self.pos.y))
                    break
                else:
                    have_shelf = True
        # right x
        have_shelf = False
        for x in range(self.pos.x+1, 8+1):
            p = self.context.getPiece(x, self.pos.y)
            if p is None:
                if not have_shelf:
                    l.append(Pos(x, self.pos.y))
            else:
                if have_shelf:
                    if not self.sameSide(p):
                        l.append(Pos(x, self.pos.y))
                    break
                else:
                    have_shelf = True
        # up vertical
        have_shelf = False
        for y in range(self.pos.y-1, -1, -1):
            p = self.context.getPiece(self.pos.x, y)
            if p is None:
                if not have_shelf:
                    l.append(Pos(self.pos.x, y))
            else:
                if have_shelf:
                    if not self.sameSide(p):
                        l.append(Pos(self.pos.x, y))
                    break
                else:
                    have_shelf = True
        # down vertical
        have_shelf = False
        for y in range(self.pos.y+1, 9+1, 1):
            p = self.context.getPiece(self.pos.x, y)
            if p is None:
                if not have_shelf:
                    l.append(Pos(self.pos.x, y))
            else:
                if have_shelf:
                    if not self.sameSide(p):
                        l.append(Pos(self.pos.x, y))
                    break
                else:
                    have_shelf = True
        return l

    def getScore(self):
        if self.isDie():
            return 0
        return 3

    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        
        dx = self.pos.x - pos.x
        dy = self.pos.y - pos.y
        
        if self.pos.x == pos.x:
            across_count = self.context.vertPieceCount(pos.x, self.pos.y, pos.y)
            if across_count == 0:
                return p==None
            elif across_count==1:
                if p is None:
                    return False
                else:
                    return p.getSide()!=self.getSide() # eat or not
            else:
                return False
                
        if self.pos.y == pos.y:
            across_count = self.context.horzPieceCount(pos.y, self.pos.x, pos.x)
            if across_count == 0:
                return p==None
            elif across_count==1:
                return p.getSide()!=self.getSide() # eat or not
            else:
                return False
                
        return False
