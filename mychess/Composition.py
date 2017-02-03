from base import *
from PieceFactory import PieceFactory
from Pos import Pos
from Move import Move
import random

class Composition:
    def __init__(self):
        self.children = []
        self.move_list = []
        context = self
        self.pieces = [
            PieceFactory.create(PieceType.tank,      Pos(0, 0), Side.black, context),
            PieceFactory.create(PieceType.horse,     Pos(1, 0), Side.black, context),
            PieceFactory.create(PieceType.minister,  Pos(2, 0), Side.black, context),
            PieceFactory.create(PieceType.scholar,   Pos(3, 0), Side.black, context),
            PieceFactory.create(PieceType.commander, Pos(4, 0), Side.black, context),
            PieceFactory.create(PieceType.scholar,   Pos(5, 0), Side.black, context),
            PieceFactory.create(PieceType.minister,  Pos(6, 0), Side.black, context),
            PieceFactory.create(PieceType.horse,     Pos(7, 0), Side.black, context),
            PieceFactory.create(PieceType.tank,      Pos(8, 0), Side.black, context),
            PieceFactory.create(PieceType.cannon,    Pos(1, 2), Side.black, context),
            PieceFactory.create(PieceType.cannon,    Pos(7, 2), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(0, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(2, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(4, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(6, 3), Side.black, context),
            PieceFactory.create(PieceType.soldier,   Pos(8, 3), Side.black, context),
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
            PieceFactory.create(PieceType.soldier,   Pos(8, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(6, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(4, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(2, 6), Side.red, context),
            PieceFactory.create(PieceType.soldier,   Pos(0, 6), Side.red, context)
            
            
        ]
        
    def __str__(self):
        s = 'composition\n'
        for p in self.pieces:
            s = s + str(p.getPos())
        s = s + "\nscroce: red-{0} black-{1}".format(self.getScore(Side.red), self.getScore(Side.black))
        
        return s
    
    def cloneFrom(self, c):
        piece_count = 32
        for i in range(0,32):
            self.pieces[i].setPos(c.pieces[i].getPos())
    
    def vertPieceCount(self, x, y1, y2):
        r = 0
        step = 1
        if y1>y2:
            step = -1
        y1 = y1+step
        for y in range(y1, y2, step):
            for p in self.pieces:
                if p.isMe(x,y):
                    r = r+1
                    break
        return r
    
    def horzPieceCount(self, y, x1, x2):
        r = 0
        step = 1
        if x1>x2:
            step = -1
        x1 = x1+step
        for x in range(x1, x2, step):
            for p in self.pieces:
                if p.isMe(x,y):
                    r = r + 1
                    break
        return r

    def getPiece(self, x, y):
        for p in self.pieces:
            if p.isMe(x,y):
                return p
        return None
    
    def getScore(self, side):
        score = 0
        if side == Side.black:
            for i in range(0, 16):
                score = score + self.pieces[i].getScore()
        else:
            for i in range(16, 32):
                score = score + self.pieces[i].getScore()
        return score

    def getCanMoveList(self, side):
        live_list = []
        if side == Side.black:
            for i in range(0, 16):
                if self.pieces[i].isDie():
                    continue
                ml = self.pieces[i].CanMoveList()
                for m in ml:
                    live_list.append((self.pieces[i], m))
        else:
            for i in range(16, 32):
                if self.pieces[i].isDie():
                    continue
                ml = self.pieces[i].CanMoveList()
                for m in ml:
                    live_list.append((self.pieces[i], m))
        return live_list

    def getMove(self, side):
        live_list = self.getCanMoveList(side)
        live_count = len(live_list)
        if live_count == 0:
            return None
        i = random.randint(0, live_count-1)
        return live_list[i];

    def getCommaner(self, side):
        if side == Side.red:
            return self.pieces[20];
        return self.pieces[4];

    def checked(self, side):
        opp_side = Side.opposite(side)
        opp_movelist = getCanMoveList(opp_side)
        commander = getCommaner(side)
        for m in opp_movelist:
            if m[1].getPos() == commander.getPos():
                return True
        return False
    def checkmated(self, side):
        opp_side = Side.opposite(side)
        opp_movelist = getCanMoveList(opp_side)
        commander = getCommaner(side)
        # move commander to avoid attck
        for m in commander.CanMoveList():
            find = False
            for oppm in opp_movelist:
                if m == oppm[1]:
                    find = True
                    break
            
            if not find:
                return False

        # move other to block attack

        return True

        
    def moveTo(self, piece, pos):
        print("moveTo:"+str(pos))
        if not piece.isCanMove(pos):
            return False
        eated_piece = None
        for p in self.pieces:
            #print(p.getPos())
            #the_pos = p.getPos()
            #if pos.x == the_pos.x and pos.y == the_pos.y:
            if pos == p.getPos():
                eated_piece = p
                break
        first = (piece, piece.getPos().clone(), pos.clone())
        second = None
        if eated_piece is not None:
            second = (eated_piece, pos.clone(), Pos(9, pos.y))
            eated_piece.die()

        move = Move(first, second)  
        self.move_list.append(move)
        piece.MoveTo(pos)
        
        return True

    def regret(self):
        if len(self.move_list)==0:
            return

        move = self.move_list.pop()
        move.first[0].MoveTo(move.first[1])
        if move.second is not None:
            move.second[0].MoveTo(move.second[1])
