from enum import Enum

class base(object):
    """description of class"""

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
 
''' 
class Side(Enum):
    red   = 1
    black = 2
    def opposite(side):
        if side == red:
            return black
        return red


