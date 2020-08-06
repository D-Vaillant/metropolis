""" testing grounds for using squarify """
import numpy as np
import squarify


class Rectangle:
    def __init__(self, width, height, char="#"):
        self.width=width
        self.height=height
        self.char=char
        self.arr = np.full((width, height), char, order='C')

    @property
    def inner(self):
        return slice(1, self.width-1), slice(1, self.height-1)

    @property
    def aspect_ratio(self):
        return self.width / self.height

    def __str__(self):
        arr = []
        for row in self.arr.transpose():
            arr.append(''.join(row))
        return "\n".join(arr)


areas = [6, 6, 4, 3, 2, 2, 1]

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
    
    R = Rectangle(width=30, height=10)
    assert sum(room_areas) == R.width*R.height

    f = squarify.padded_squarify(room_areas, 0, 0, R.width, R.height)

    for rectangle in f:
        for k, v in rectangle.items():
            rectangle[k] = round(v)

    for r in f:
        R.arr[(slice(r['x'], r['x']+r['dx']), slice(r['y'], r['y']+r['dy']))] = "."
    print(R)

    #R.arr[R.inner] = "."
    #print(R)

