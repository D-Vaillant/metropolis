""" testing grounds for using squarify """
from typing import Iterator, Tuple
import numpy as np
import squarify
import itertools


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + width

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) /2 )
        center_y = int((self.y1 + self.y2) /2 )

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
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



#if R.width > R.height:
    # horizontal split
#    pass
#else:
    # vertical split
#    pass
# How to account for wall thickness? 
if __name__ == "__main__":
    room_areas = [150,50,30,20,15,35]
    room_areas.sort(reverse=True)
    
    #R = Rectangle(width=30, height=10)
    width = 30
    height = 10
    wall_char = '#'
    floor_char = '.'

    R = np.full((width, height), wall_char, order='F')
    assert sum(room_areas) == width*height

    f = squarify.squarify(room_areas, 0, 0, width, height)

    # f is an array of "descriptions" of squares we made
    # they don't account for the flattening to integers particularly well
    x_flipflop = itertools.cycle([-1, +1])
    y_flipflop = itertools.cycle([-1, +1])
    for rectangle in f:
        for k, v in rectangle.items():
            if k in ['x', 'y']:
                rectangle[k] = int(v)+1
            else:
                rectangle[k] = int(v)-1

#     for r in f:
#         R[(slice(r['x'], r['x']+r['dx']), slice(r['y'], r['y']+r['dy']))] = floor_char
#     # Make sure we have perimeter walls
#     for outside_boundary in perimeter(R):
#         x, y = outside_boundary
#         R[x, y] = wall_char
