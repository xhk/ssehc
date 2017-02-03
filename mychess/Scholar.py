from Piece import Piece
from Pos import Pos
from base import *

class Scholar(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.scholar, pos, rb, context)

    def CanMoveList(self):
        l = []
        ml = []
        # 在四个角的时候，只能往中心走
        if self.pos.y is 0 or self.pos.y is 2 or self.pos.y is 7 or self.pos.y is 9:
            ml = [Pos(4,1)]
        elif self.pos.x is 4:
            if self.rb == Side.red:
                ml = [Pos(3,7), Pos(5,7), Pos(3,9), Pos(5,9)]
            else:
                ml = [Pos(3,0), Pos(5,0), Pos(3,2), Pos(5,2)]

        for m in ml:
            if self.isCanMove(m):
                l.append(m)
        return l    
            

    def getScore(self):
        if self.isDie():
            return 0
        return 3    
    
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        
        dx = self.pos.x - pos.x
        dy = self.pos.y - pos.y
        
        if abs(dx)!=1 or abs(dy)!=1:
            return False   
        
        if self.rb == Side.red and pos.y<7:
            return False

        if self.rb == Side.black and pos.y>2:
            return False
        
        if p is None:
            return True
        return p.getSide()!=self.getSide()
