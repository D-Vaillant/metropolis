""" Implement some of the square_treemap stuff. """
from __future__ import annotations

from collections import NamedTuple, List, Optional

import tcod

from game_map import GameMap
import tile_types


def generate_apartment(
    room_min_size: int,
    room_max_size: int,
) -> RectangularRoom:
    rooms: List[RectangularRoom] = []

    pass


def generate_apartment_floor(
    max_apartments: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
) -> GameMap:
    pass


