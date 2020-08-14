""" testing grounds for using squarify """
from typing import Iterator, Tuple, Optional
import math
import random
import numpy as np
import squarify
import itertools

from procgen import RectangularRoom

def add_connection(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """ Add a door. """
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Get coordinates.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def find_slice_midpoint(s: slice,) -> int:
    """ if it's not even, just random it up """
    return s.start + int((s.stop - s.start)/2) + random.choice([-1,0])


def find_door(
    start: RectangularRoom,
    end: RectangularRoom,
) -> Optional[Tuple[int, int]]:
    """ Get the midpoint of the adjacency wall. """
    wall = start.adjacency_wall(end)
    if wall is None:
        return None
    # check horizontally
    # TODO: Make this division random.
    #midpoint = lambda sliced: sliced.start + int(sliced.stop - sliced.start) + random.choice([0, 1])
    if wall[0].start == wall[0].stop - 1:
        x = wall[0].start
        y = find_slice_midpoint(wall[1])
        # horizontal
        # care about vertical
        # find y
    else:  # it's vertical
        y = wall[1].start
        x = find_slice_midpoint(wall[0])
    return (x, y)


def print_floor(arr):
    out_arr = []
    for row in arr.transpose():
        out_arr.append(''.join(row))
    # Can make this a return as well.
    print("\n".join(out_arr))

def perimeter(arr: np.ndarray) -> Iterator[slice]:
    """ Returns a slice for the perimeter, so we can make sure it's filled in. """
    width, height = arr.shape
    out_arr = []
    # Adding each of the sides.
    out_arr.append((slice(0, width-1), 0))  # Top
    out_arr.append((slice(0, width-1), height-1))  # Bottom
    out_arr.append((0, slice(0, height-1)))  # Left
    out_arr.append((width-1, slice(0, height-1)))  # Right
    return out_arr


def carve_dungeon(dungeon,
                  room_x,
                  room_y,
                  width,
                  height,
                  room_areas,
                  wall_char='.',
                  floor_char='#'):
    assert sum(room_areas) == width*height
    assert dungeon.shape >= (width, height)

    room_areas.sort(reverse=True)
    R = np.full((width, height), wall_char, order='F')

    f = squarify.squarify(room_areas, 0, 0, width, height)
    # f is an array of "descriptions" of squares we made
    # they don't account for the flattening to integers particularly well
    for rectangle in f:
        for k, v in rectangle.items():
            if k in ['x', 'y']:
                rectangle[k] = round(v)
            else:
                rectangle[k] = round(v)

    return [RectangularRoom(x = room_x + r['x'],
                             y = room_y + r['y'],
                             width=r['dx'],
                             height=r['dy']) for r in f]



# How to account for wall thickness? 
if __name__ == "__main__":
    room_x = 2
    room_y = 2

    width = 14
    height = 10
    room_areas = [50,25,20,45]

    wall_char = '#'
    floor_char = '.'

    dungeon = np.full((20, 20), fill_value=wall_char, order="F")
    rooms = carve_dungeon(dungeon,
                            room_x=room_x,
                            room_y=room_y,
                            width=width,
                            height=height,
                            room_areas=room_areas,
                            wall_char='#',
                            floor_char='.')
    for index, room in enumerate(rooms):
        dungeon[room.inner] = floor_char
        if index > 0:
            door_loc = find_door(rooms[index-1], room)
            if door_loc is not None:
                dungeon[door_loc] = 'D'


    print_floor(dungeon)
