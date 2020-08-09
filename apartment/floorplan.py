# Drawn from an academic paper
from enum import Enum
from typing import Callable, List, TYPE_CHECKING

import numpy as np

from game_map import GameMap
from procgen import RectangularRoom


# Figure out a tile/distance ratio.

class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        # Topleft is 0, 0.
        self.contents = np.full((width, height), fill_value=True, order="F")
        self.width = width
        self.height = height

        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    
AreaType = Enum("private", "public", "hallway")

class RoomArea:
    name: str
    area_type: AreaType
    ratio: float  # calculated as width / height


def place_rooms(x, y, room_width, room_height, room_areas: List[RoomArea]):
    new_building = RectangularRoom(x, y, room_width, room_height)




    
