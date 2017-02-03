from Piece import Piece
from Pos import Pos
from base import *

class Pawn(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.soldier, pos, rb, context)        

    def CanMoveList(self):
        l = []
        ml =[]
        attack = 1
        if self.rb == Side.red:
            attack = -1
        ml = [Pos(self.pos.x-1, self.pos.y),Pos(self.pos.x+1, self.pos.y), Pos(self.pos.x, self.pos.y+attack) ]
        for m in ml:
            if m.x>=0 and m.x<=8 and m.y>=0 and m.y<=9 and self.isCanMove(m):
                l.append(m)
        return l

    def inPalace(self):
        if self.rb == Side.red:
            return self.pos.x>=3 and self.pos.x<= 5 and self.pos.y>=0 and self.pos.y<=2    
        return self.pos.x>=3 and self.pos.x<= 5 and self.pos.y>=7 and self.pos.y<=9
    
    def getScore(self):
        if self.isDie():
            return 0
        
        across = self.isAcrossRiver()
        if across :
            if inPalace() : 
                return 3
            return 2
        
        return 1
    
    def isAcrossRiver(self):
        if self.rb == Side.red:
            return self.pos.y<5
        return self.pos.y>4
    
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        
        dx = self.pos.x - pos.x
        if self.rb == Side.red: 
            dy = self.pos.y - pos.y
        else:
            dy = pos.y - self.pos.y
        
        if not (dy>=0 and dy<=1):
            return False
        
        across = self.isAcrossRiver()
        if (not across) and ( dx is not 0 ):
            return False
        
        if across :
            absx = abs(dx)
            if dy is 0:
                # absx must be 1
                if absx is not 1:
                    return False
            elif dy is 1:
                if absx is not 0:
                    return False
            else:
                return False
            
        if p is None:
            return True        
        return p.getSide() != self.getSide()
