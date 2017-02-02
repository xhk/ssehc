
class Pos:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return '{0}{1}'.format(self.x, self.y)
    def __repr__(self, **kwargs):
        return self.__str__()
    def __cmp__(self, pos):
        print('__cmp__')
        dot = self.y*9+self.x
        other = pos.y*9+pos.x
        return dot-other
    def __eq__(self, pos):
        print('__eq__')
        return self.x == pos.x and self.y==pos.y
if __name__ == '__main__':
	p1 = Pos(1,1)
	p2 = Pos(1,1)
	p3 = Pos(1,2)
	
	print(p1==p2)
	print(p1==p3)
	