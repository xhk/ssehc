from Piece import Piece
from Pos import Pos
from base import *

class Commander(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.commander, pos, rb, context)
    def CanMoveList(self):
        l = []
        ml = [
             Pos(self.pos.x-1, self.pos.y), Pos(self.pos.x-1, self.pos.y),
             Pos(self.pos.x, self.pos.y-1), Pos(self.pos.x, self.pos.y+1)
        ]

        for m in ml:
            ym = m.y%7
            if m.x>=3 and m.x<=5 and ym>=0 and ym<=2 and self.isCanMove(m):
                l.append(m)
        return l

    def getScore(self):
        if self.isDie():
            return 0
        return 2
    
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        
        dx = self.pos.x - pos.x
        dy = self.pos.y - pos.y
        
        absdx = abs(dx)
        absdy = abs(dy)
        
        if pos.x<2 or pos.x>5:
            return False
        
        if self.rb == Side.red and pos.y<7:
            return False
        
        if self.rb == Side.black and pos.y>2:
            return False
        
        if absdx==0 and absdy!=1:
            return False
        
        if absdx==1 and absdy!=0:
            return False
        if p is None:
            return True
        return p.getSide()!=self.getSide()
