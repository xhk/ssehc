from enum import Enum

# 棋子类型
class PieceType(Enum):
    unknown   = 0
    tank      = 1
    horse     = 2
    minister  = 3
    scholar   = 4
    commander = 5
    cannon    = 6
    soldier   = 7
    
    
'''
    红、黑方
''' 
class Side(Enum):
    red   = 1
    black = 2

class Pos:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
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
        
    def CanMoveList(self):
        '''
        可落子点列表
        '''
        pass
    def isCanMove(self, pos):
        pass
    
    def isMe(self, x, y):
        return self.pos.x == x and self.pos.y==y
        
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
     
class Tank(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.tank, pos, rb, context)
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        if self.pos.x == pos.x: # on the same vertical line
            if ( self.context.vertPieceCount(x, self.pos.y, pos.y) == 0 ):
                if p==None: # no piece in the end
                    return True
                else :
                    return p.getSide() != self.getSide() # only eat other side 
            else:
                return False
        
        elif self.pos.y == pos.y: # on the same horizontal line
            if self.context.horzPieceCount(y, self.pos.x, pos.x)==0:
                if p==None: # no piece in the end
                    return True
                else:
                    return p.getSide() != self.getSide()
            else:
                return False
        else:
            return False
        
        return False
        
class Horse(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.horse, pos, rb, context)
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
                lame = (self.context.getPiece(self.pos.x+1, self.y)!=None)
            elif dy==1:
                lame = (self.context.getPiece(self.pos.x+1, self.y)!=None)
            else:
                return False
        
        if lame :
            return False
        
        if p == None:
            return True
        
        return p.getSide() != self.getSide()
        
    
class Minister(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.minister, pos, rb, context)
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
        
        return p.getSide()!=self.getSide()
            
        
class Scholar(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.scholar, pos, rb, context)
        
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
        
        return p.getSide()!=self.getSide()
            
class Commander(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.commander, pos, rb, context)
        
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
        
        return p.getSide()!=self.getSide()
        
class Cannon(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.cannon, pos, rb, context)
    def isCanMove(self, pos):
        p = self.context.getPiece(pos.x, pos.y)
        
        dx = self.pos.x - pos.x
        dy = self.pos.y - pos.y
        
        if self.pos.x == pos.x:
            across_count = self.context.vertPieceCount(pos.x, self.pos.y, pos.y)
            if across_count == 0:
                return p==None
            elif across_count==1:
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
class Pawn(Piece):
    def __init__(self, pos, rb, context):
        Piece.__init__(self, PieceType.soldier, pos, rb, context)        
    
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
        
        if dy is not 0 or dy is not 1:
            return False
        
        across = self.isAcrossRiver()
        if (not across) and ( dx is not 0 ):
            return False
        
        if across :
            if (dx is 0) and (dy is not 1):
                return False
            if (dy is 0) and (abs(dx) is not 1):
                return False
                
        return p.getSide() != self.getSide()
class PieceFactory:
    def create(pt, pos, rb, context):
        if pt == PieceType.tank:
            return Tank(pos, rb, context)
        elif pt == PieceType.horse:
            return Horse(pos, rb, context)
        elif pt == PieceType.minister:
            return Minister(pos, rb, context)
        elif pt == PieceType.scholar:
            return Scholar(pos, rb, context)
        elif pt == PieceType.commander:
            return Commander(pos, rb, context)
        elif pt == PieceType.cannon:
            return Cannon(pos, rb, context)
        elif pt == PieceType.soldier:
            return Pawn(pos, rb, context)
        else:
            return None
            
        return None


class Composition:
    def __init__(self):
        context = self
        self.pieces = [
            PieceFactory.create(PieceType.tank,      Pos(8, 9), Side.red, context),
            PieceFactory.create(PieceType.horse,     Pos(7, 9), Side.red, context),
            PieceFactory.create(PieceType.minister,  Pos(6, 9), Side.red, context),
            PieceFactory.create(PieceType.scholar,   Pos(5, 9), Side.red, context),
            PieceFactory.create(PieceType.commander, Pos(4, 9), Side.red, context),
            PieceFactory.create(PieceType.scholar,   Pos(3, 9), Side.red, context),
            PieceFactory.create(PieceType.minister,  Pos(2, 9), Side.red, context),
            PieceFactory.create(PieceType.horse,     Pos(1, 9), Side.red, context),
            PieceFactory.create(PieceType.tank,      Pos(0, 9), Side.red, context),
            PieceFactory.create(PieceType.cannon,    Pos(7, 7), Side.red, context),
            PieceFactory.create(PieceType.cannon,    Pos(1, 7), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(0, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(2, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(4, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(6, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(8, 6), Side.red, context),
            
            PieceFactory.create(PieceType.tank,      Pos(8, 0), Side.black, context),
            PieceFactory.create(PieceType.horse,     Pos(7, 0), Side.black, context),
            PieceFactory.create(PieceType.minister,  Pos(6, 0), Side.black, context),
            PieceFactory.create(PieceType.scholar,   Pos(5, 0), Side.black, context),
            PieceFactory.create(PieceType.commander, Pos(4, 0), Side.black, context),
            PieceFactory.create(PieceType.scholar,   Pos(3, 0), Side.black, context),
            PieceFactory.create(PieceType.minister,  Pos(2, 0), Side.black, context),
            PieceFactory.create(PieceType.horse,     Pos(1, 0), Side.black, context),
            PieceFactory.create(PieceType.tank,      Pos(0, 0), Side.black, context),
            PieceFactory.create(PieceType.cannon,    Pos(7, 2), Side.black, context),
            PieceFactory.create(PieceType.cannon,    Pos(1, 2), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(0, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(2, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(4, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(6, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(8, 3), Side.black, context)
        ]
    def vertPieceCount(self, x, y1, y2):
        r = 0
        step = 1
        if y1>y2:
            step = -1
        for y in range(y1, y2, step):
            for p in pieces:
                if p.isMe(x,y):
                    r = r+1
                    break
        return r
    
    def horzPieceCount(self, y, x1, x2):
        r = 0
        step = 1
        if x1>x2:
            step = -1
        for x in range(x1, x2, step):
            for p in pieces:
                if p.isMe(x,y):
                    r = r + 1
                    break
        return r

    def getPiece(self, x, y):
        for p in pieces:
            if p.isMe(x,y):
                return p
        return None
    
        