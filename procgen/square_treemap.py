""" testing grounds for using squarify """
from typing import Iterator, Tuple
import math
import numpy as np
import squarify
import itertools


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) /2 )
        center_y = int((self.y1 + self.y2) /2 )

        return center_x, center_y

    @property
    def outer(self) -> Tuple[slice, slice]:
        """ Returns the whole room, walls including. """
        return slice(self.x1, self.x2+1), slice(self.y1, self.y2+1)

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        """ Returns true if rooms overlap. """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    def get_random_point(self):
        x = random.randint(self.x1 + 1, self.x2 - 1)
        y = random.randint(self.y1 + 1, self.y2 - 1)
        return x, y


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



#if R.width > R.height:
    # horizontal split
#    pass
#else:
    # vertical split
#    pass
# How to account for wall thickness? 
if __name__ == "__main__":
    room_x = 2
    room_y = 2

    width = 14
    height = 10
    room_areas = [50,25,25,40]

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
    for room in rooms:
        dungeon[room.inner] = floor_char

    #for side in perimeter(dungeon):
    #    dungeon[side] = wall_char
    print_floor(dungeon)

#     R = np.full((width, height), wall_char, order='F')
#     assert sum(room_areas) == width*height

#     f = squarify.squarify(room_areas, 0, 0, width, height)
#     # f is an array of "descriptions" of squares we made
#     # they don't account for the flattening to integers particularly well
#     for rectangle in f:
#         for k, v in rectangle.items():
#             if k in ['x', 'y']:
#                 rectangle[k] = int(v)
#             else:
#                 rectangle[k] = int(v)

#     rooms = [RectangularRoom(x = room_x + r['x'],
#                              y = room_y + r['y'],
#                              width=r['dx'],
#                              height=r['dy']) for r in f]

#     for r in f:
#          R[(slice(r['x'], r['x']+r['dx']), slice(r['y'], r['y']+r['dy']))] = floor_char
#     # Make sure we have perimeter walls
#     for outside_boundary in perimeter(R):
#          x, y = outside_boundary
#          R[x, y] = wall_char

#     for room in rooms:
#         dungeon[room.inner] = floor_char

#     for side in perimeter(dungeon):
#         dungeon[side] = wall_char

