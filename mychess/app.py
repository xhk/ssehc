from tkinter import *
#from chess import *

from Composition import Composition
from base import *
from Pos import Pos

class GuiPiece:
    def __init__(self, piece, cp):
        self.piece = piece
        pos = piece.getPos()
        self.pos = Pos(pos.x, pos.y)
        name = piece.getName()
        side = piece.getSide()
        self.cp = cp
        
        self.bgColor = 'red'
        if side == Side.black:
            self.bgColor = 'black'
        
        x = pos.x * cp.size_unit + cp.startx
        y = pos.y * cp.size_unit + cp.starty
        self.circle = cp.canvas.create_oval(x-10,y-10,x+10,y+10, fill=self.bgColor, width=1, stipple="gray25")
        self.text   = cp.canvas.create_text(x, y, text=name, fill='white', activefill='yellow')
        
    def isIn(self, x,y):
        pos = self.piece.getPos()
        xx = self.cp.startx+pos.x*self.cp.size_unit
        yy = self.cp.starty+pos.y*self.cp.size_unit
        #print('xx={0},yy={1}, pos.x={2}, pos.y={3}'.format(xx,yy, pos.x, pos.y))
        return x>xx-10 and x<xx+10 and y>yy-10 and y<yy+10
    
    def isMe(self, pos):
        return self.piece.isMe(pos.x, pos.y)

    def check(self):
        #print(str(self.piece.CanMoveList()))
        self.cp.lightMoveTips(self.piece.CanMoveList())
        self.cp.canvas.itemconfig(self.circle, outline="yellow", width=2)
    def normal(self):
        self.cp.hideMoveTips()
        self.cp.canvas.itemconfig(self.circle, outline="", width=1)
    def hide(self):
        self.cp.canvas.itemconfig(self.circle, state="hidden")
        self.cp.canvas.itemconfig(self.text, state="hidden")
    def show(self):
        self.cp.canvas.itemconfig(self.circle, state="normal")
        self.cp.canvas.itemconfig(self.text, state="normal")
    
    def updateUI(self):
        pos = self.piece.getPos()
        #print('{0},{1}'.format(self.pos, pos))
        #if self.pos.x == pos.x and self.pos.y == pos.y:
        if self.pos == pos:
            return

        self.pos.x = pos.x
        self.pos.y = pos.y
        
        xindex = pos.x
        yindex = pos.y
            
        if self.piece.isDie():
            #print(self.piece.getName())
            self.hide()
            return
        
        #print(self.piece.getName())
        x = self.cp.startx + xindex*self.cp.size_unit  
        y = self.cp.starty + yindex*self.cp.size_unit
        self.cp.canvas.coords(self.circle, x-10, y-10, x+10, y+10)
        self.cp.canvas.coords(self.text  , x, y)
        self.show()
        
class MoveMark:
    def __init__(self, cp, pos, color):
        self.cp = cp
        c = self.cp.index2Coorinate(pos)
        self.left_top_line     = self.cp.canvas.create_line(c.x-12, c.y-7, c.x-12, c.y-12, c.x-7, c.y-12, width="1", fill=color, state="hidden")
        self.left_bottom_line  = self.cp.canvas.create_line(c.x-12, c.y+7, c.x-12, c.y+12, c.x-7, c.y+12, width="1", fill=color, state="hidden")
        self.right_top_line    = self.cp.canvas.create_line(c.x+12, c.y-7, c.x+12, c.y-12, c.x+7, c.y-12, width="1", fill=color, state="hidden")
        self.right_bottom_line = self.cp.canvas.create_line(c.x+12, c.y+7, c.x+12, c.y+12, c.x+7, c.y+12, width="1", fill=color, state="hidden")
    def show(self):
        self.cp.canvas.itemconfig(self.left_top_line,     state="normal")
        self.cp.canvas.itemconfig(self.left_bottom_line,  state="normal")
        self.cp.canvas.itemconfig(self.right_top_line,    state="normal")
        self.cp.canvas.itemconfig(self.right_bottom_line, state="normal")
    def hide(self):
        self.cp.canvas.itemconfig(self.left_top_line,     state="hidden")
        self.cp.canvas.itemconfig(self.left_bottom_line,  state="hidden")
        self.cp.canvas.itemconfig(self.right_top_line,    state="hidden")
        self.cp.canvas.itemconfig(self.right_bottom_line, state="hidden")
    def move(self, pos):
        c = self.cp.index2Coorinate(pos)
        self.cp.canvas.coords(self.left_top_line,    c.x-12, c.y-7, c.x-12, c.y-12, c.x-7, c.y-12) 
        self.cp.canvas.coords(self.left_bottom_line, c.x-12, c.y+7, c.x-12, c.y+12, c.x-7, c.y+12)
        self.cp.canvas.coords(self.right_top_line,   c.x+12, c.y-7, c.x+12, c.y-12, c.x+7, c.y-12)
        self.cp.canvas.coords(self.right_bottom_line,c.x+12, c.y+7, c.x+12, c.y+12, c.x+7, c.y+12)

class ChessPanal(Frame):
    def createWidgets(self):
        self.QUIT = Button(self, text='QUIT', foreground='red',
                           command=self.quit)
        self.QUIT.pack(side=BOTTOM, fill=BOTH)
        
        self.regret_btn = Button(self, text="悔棋", command=self.regret)
        self.regret_btn.pack(side=TOP)
        #self.name=Entry(self, width=60, fg='black')
        #self.name.pack(side=BOTTOM, fill=BOTH)
        #self.namev=StringVar()
        #self.name['textvariable'] = self.namev
        self.startx = 30
        self.starty = 50
        self.size_unit = 30
        self.guipieces = []
        self.canvas = Canvas(self, width=300, height=400, bg='white')
        self.canvas.bind('<ButtonPress-1>'  , self.leftButtonDown)
        self.canvas.bind('<ButtonRelease-1>', self.leftButtonUp)
        self.move_side = Side.red # 走子方 红先
        x = 0
        self.line = self.canvas.create_line(x,563,x+50,563, width=1, fill='BLACK', tags='linex')
        self.drawPanel()
        self.createPieces()
        self.drawMoveTips()
        self.begin_mark = MoveMark(self, Pos(0, 0), 'blue')
        self.end_mark   = MoveMark(self, Pos(0, 0), 'red')
        self.select_piece = None
        #self.canvas.create_text(100, 10, text='Text', fill='red')

        self.canvas.pack(side=LEFT)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.pieces = []
        self.main_composition = Composition()
        
        Pack.config(self)
        self.createWidgets()
    
    def regret(self):
        self.main_composition.regret()
        self.updateUI()
    
    def updateUI(self):
        for gp in self.guipieces:
            gp.updateUI()

    def index2Coorinate(self, pos):
        c = Pos()
        c.x = self.startx + (pos.x*self.size_unit)
        c.y = self.starty + (pos.y*self.size_unit)
        return c
    
    def coorindate2Index(self, c):
        p = Pos(-1,-1)
        rx = c.x - self.startx
        mx = rx % self.size_unit
        xindex = int(rx/self.size_unit)
        if mx>10 and mx<20:
            return p
        
        ry = c.y-self.starty
        my = ry%self.size_unit
        yindex = int(ry/self.size_unit)

        if my>10 and my<20:
            return p

        if mx>=20 and xindex>0:
            xindex = xindex+1
        if my>=20 and yindex>0:
            yindex = yindex+1

        p.x = xindex
        p.y = yindex
        return p

    def createPieces(self):
        for p in self.main_composition.pieces:
            self.createPiece(p)
    
    def createPiece(self, piece):
        self.guipieces.append(GuiPiece(piece, self))
    def drawRiceShape(self, x, y):
        dot_list = [
        [x-5-2, y-2, x-2, y-2, x-2, y-5-2],
        [x-5-2, y+2, x-2, y+2, x-2, y+5+2],
        [x+5+2, y-2, x+2, y-2, x+2, y-5-2],
        [x+5+2, y+2, x+2, y+2, x+2, y+5+2]
        ]
        
        minx = self.startx
        maxx = self.startx+8*self.size_unit
        for l in dot_list:
            if l[0]>minx and l[0]<maxx:
                self.canvas.create_line(l, width=1, fill='black')
    
    def drawMoveTips(self):
        self.mv_tips = []
        for i in range(0, 10):
            for j in range(0, 9):
                c = self.index2Coorinate(Pos(j,i))
                o = self.canvas.create_oval(c.x-4, c.y-4, c.x+4, c.y+4, fill="yellow", state="hidden")
                self.mv_tips.append(o)
    def hideMoveTips(self):
        for o in self.mv_tips:
            self.canvas.itemconfig(o, state="hidden")
    def lightMoveTips(self, pos_list):
        for p in pos_list:
            self.canvas.itemconfig( self.mv_tips[p.x+9*p.y], state="normal")
    

    def drawPanel(self):
        size_unit = 30
        width  = 8 * size_unit
        height = 9 *size_unit
        x = self.startx 
        y = self.starty
        
        self.canvas.create_line(x-4, y-3, x+width+4, y-3, x+width+4, y+height+4, x-4, y+height+4, x-3, y-3, width=2, fill='red')

        # draw the border
        self.canvas.create_line(x, y, x+width, y, x+width, y+height, x, y+height, x, y, width=1, fill='BLACK', tags='linex')
        
        # hozr
        for i in range(8):
            self.canvas.create_line(x, y+(i+1)*size_unit, x+width, y+(i+1)*size_unit,  width=1, fill='BLACK', tags='linex')
        
        # vector
        for i in range(7):
            self.canvas.create_line(x+(i+1)*size_unit, y, x+(i+1)*size_unit, y+4*size_unit,  width=1, fill='black', tags='linex')
            self.canvas.create_line(x+(i+1)*size_unit, y+5*size_unit, x+(i+1)*size_unit, y+9*size_unit,  width=1, fill='BLACK', tags='linex')
        
        self.canvas.create_line(x+3*size_unit,y, x+5*size_unit, y+2*size_unit)
        self.canvas.create_line(x+5*size_unit,y, x+3*size_unit, y+2*size_unit)
        self.canvas.create_line(x+3*size_unit,y+7*size_unit, x+5*size_unit, y+9*size_unit)
        self.canvas.create_line(x+5*size_unit,y+7*size_unit, x+3*size_unit, y+9*size_unit)
        self.canvas.create_text(x+4*size_unit,y+4*size_unit+size_unit/2, text="river")
        
        rice_list = [
            Pos(7, 7),
            Pos(1, 7),
            Pos(0, 6),
            Pos(2, 6),
            Pos(4, 6),
            Pos(6, 6),
            Pos(8, 6),
            Pos(7, 2),
            Pos(1, 2),
            Pos(0, 3),
            Pos(2, 3),
            Pos(4, 3),
            Pos(6, 3),
            Pos(8, 3)
        ]
        for r in rice_list:
            c = self.index2Coorinate(r)
            self.drawRiceShape(c.x, c.y)
    def guiPiecePosStr(self):
        s = ''
        for p in self.guipieces:
            s = s + str(p.pos)
        return s
            
    def moveFromTo(self, piece, to):
        fr = piece.getPos()
        self.main_composition.moveTo(piece, to)
        self.begin_mark.show()
        self.end_mark.show()
        self.begin_mark.move(fr)
        self.end_mark.move(to)

    def leftButtonDown(self, event):
        print('mouse down1')
        print(self.main_composition)
        #print(self.guiPiecePosStr())
        pos = self.coorindate2Index(Pos(event.x, event.y))
        print('{0},{1}->{2},{3}'.format(event.x, event.y, pos.x, pos.y))
        if pos.x == -1:
            return 

        if self.select_piece == None:
            for p in self.guipieces:
                if p.isMe(pos):
                    self.select_piece = p
                    self.select_piece.check()
                    
                    break
        else:
            moved = self.main_composition.moveTo(self.select_piece.piece, pos)
            self.select_piece.normal()
            self.select_piece = None
            if moved:
                mv = self.main_composition.getMove(Side.black)
                if mv is not None:
                    self.moveFromTo(mv[0], mv[1])
            self.updateUI()
        print('mouse down2')
        #print(self.main_composition)
        print(self.guiPiecePosStr())
        
    def leftButtonUp(self, event):
        print('mouse up')
        #print(self.main_composition)
        self.updateUI()
        
if __name__=='__main__':
    cp = ChessPanal()
    cp.mainloop()