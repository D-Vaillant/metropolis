""" testing grounds for using squarify """
from typing import Iterator
import numpy as np
import squarify
import itertools


# class Rectangle:
#     def __init__(self, width, height, char="#"):
#         self.width=width
#         self.height=height
#         self.char=char
#         self.arr = np.full((width, height), char, order='C')

#     @property
#     def inner(self):
#         return slice(1, self.width-1), slice(1, self.height-1)

#     @property
#     def aspect_ratio(self):
#         return self.width / self.height

#     def __str__(self):
#         arr = []
#         for row in self.arr.transpose():
#             arr.append(''.join(row))
#         return "\n".join(arr)


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

    for r in f:
        R[(slice(r['x'], r['x']+r['dx']), slice(r['y'], r['y']+r['dy']))] = floor_char
    # Make sure we have perimeter walls
    for outside_boundary in perimeter(R):
        x, y = outside_boundary
        R[x, y] = wall_char
    print_floor(R)
