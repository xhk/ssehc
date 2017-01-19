from tkinter import *
from chess import *

class GuiPiece:
    def __init__(self, piece, cp):
        self.piece = piece
        pos = piece.getPos()
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
        
    def move(self, x,y):
        xindex = int((x-self.cp.startx)/self.cp.size_unit)
        yindex = int((y-self.cp.starty)/self.cp.size_unit)
        if x>(self.cp.startx + (xindex+1)*self.cp.size_unit-10):
            xindex = xindex+1
        if y>(self.cp.starty + (yindex+1)*self.cp.size_unit-10):
            yindex = yindex + 1
        print('xindex={0},yindex={1}'.format(xindex,yindex))
        
        if not self.piece.isCanMove(Pos(xindex, yindex)):
            return False
        
        p = None
        for gp in self.cp.guipieces:
            if gp.isIn(x, y) :
                p = gp
                break
        if p is not None:
            self.eat(p)

        self.piece.MoveTo(Pos(xindex,yindex))
        x = self.cp.startx + xindex*self.cp.size_unit
        y = self.cp.starty + yindex*self.cp.size_unit
        self.cp.canvas.coords(self.circle, x-10, y-10, x+10, y+10)
        self.cp.canvas.coords(self.text  , x, y)
        return True
    
    def isIn(self, x,y):
        pos = self.piece.getPos()
        xx = self.cp.startx+pos.x*self.cp.size_unit
        yy = self.cp.starty+pos.y*self.cp.size_unit
        #print('xx={0},yy={1}, pos.x={2}, pos.y={3}'.format(xx,yy, pos.x, pos.y))
        return x>xx-10 and x<xx+10 and y>yy-10 and y<yy+10
    
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

    def eat(self, p):
        p.piece.die()
        p.hide()

class ChessPanal(Frame):
    def createWidgets(self):
        self.QUIT = Button(self, text='QUIT', foreground='red',
                           command=self.quit)
        self.QUIT.pack(side=BOTTOM, fill=BOTH)
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
        x = 0
        self.line = self.canvas.create_line(x,563,x+50,563, width=1, fill='BLACK', tags='linex')
        self.drawPanel()
        self.drawPieces()
        self.drawMoveTips()
        self.select_piece = None
        self.canvas.create_text(100, 10, text='Text', fill='red')
        self.canvas.pack(side=LEFT)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.pieces = []
        self.main_composition = Composition()
        
        
        
        Pack.config(self)
        self.createWidgets()
    
    def index2Coorinate(self, pos):
        c = Pos()
        c.x = self.startx + (pos.x*self.size_unit)
        c.y = self.starty + (pos.y*self.size_unit)
        return c
    
    def drawPieces(self):
        for p in self.main_composition.pieces:
            self.drawPiece(p)
    
    def drawPiece(self, piece):
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
        
        

    def leftButtonDown(self, event):
        print('{0},{1}'.format(event.x, event.y))
        if self.select_piece == None:
            for p in self.guipieces:
                if p.isIn(event.x, event.y):
                    self.select_piece = p
                    self.select_piece.check()
                    break
        else:
            self.select_piece.move(event.x, event.y)
            self.select_piece.normal()
            self.select_piece = None
    def leftButtonUp(self, event):
        print('mouse up')
        print(self.main_composition)
        
if __name__=='__main__':
    cp = ChessPanal()
    cp.mainloop()