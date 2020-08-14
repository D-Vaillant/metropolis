""" Implement some of the square_treemap stuff. """
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import tcod

from game_map import GameMap
from procgen import RectangularRoom
import tile_types

if TYPE_CHECKING:
    from engine import Engine


def generate_apartment(
    room_min_size: int,
    room_max_size: int,
    engine: Engine,
) -> RectangularRoom:
    rooms: List[RectangularRoom] = []

    pass


def generate_apartment_floor(
    max_apartments: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    hallway_width: int,
    engine: Engine,
) -> GameMap:
    # Generate a hallway and an entrance.
    midpoint = (map_width//2, map_height//2)
    top_left = (0, hallway_width // 2)
    
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    hallway = RectangularRoom(
        x = 0,
        y = map_height // 2,
        width = map_width-1,
        height = hallway_width,
      )

    dungeon.tiles[hallway.inner] = tile_types.floor
    player.place(*hallway.center, dungeon)

    return dungeon

