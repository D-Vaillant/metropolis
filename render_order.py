from enum import auto, Enum



class RenderOrder(Enum):
    FLOOR = auto()
    FURNITURE = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
