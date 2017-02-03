from base import *
from Tank import Tank
from Horse import Horse
from Minister import Minister
from Scholar import Scholar
from Commander import Commander
from Cannon import Cannon
from Pawn import Pawn

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