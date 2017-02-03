from Piece import Piece
from Pos import Pos
from base import *

class Minister(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.minister, pos, rb, context)

    def CanMoveList(self):
        l = []
        ml = [
            Pos(self.pos.x-2, self.pos.y-2),
            Pos(self.pos.x-2, self.pos.y+2),
            Pos(self.pos.x+2, self.pos.y-2),
            Pos(self.pos.x+2, self.pos.y+2)
        ]
        for m in ml:
            if m.x>=0 and m.x<=8 and m.y>=0 and m.y<=9 and self.isCanMove(m):
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
        
        if abs(dx)!=2 or abs(dy)!=2:
            return False
        
        if self.rb == Side.red and pos.y<5:
            return False
        
        if self.rb == Side.black and pos.y>4:
            return False
            
        lame_pos_piece = self.context.getPiece((self.pos.x+pos.x)/2, (self.pos.y+pos.y)/2)
        if( lame_pos_piece != None):
            return False
        
        if p is None:
            return True

        return p.getSide()!=self.getSide()
