from typing import List

class Pixel:

    def __init__(self, x: int, y: int, c_flag: int):
        self.x = x
        self.y = y
        self.c_flag = c_flag

class Canvas:

    def __init__(self, width: int, height: int):
        self.arr = [[0]*width]*height
        self.width = width
        self.height = height
    
    # Top left is 0,0
    def get_pixel(self, x: int, y: int):
        return Pixel(x, y, self.arr[y][x])
    
    def set_pixel_pos(self, x, y, c_flag):
        return self.set_pixel(Pixel(x, y, c_flag))
    
    def set_pixel(self, p: Pixel) -> 'Canvas':
        self.arr[p.y][p.x] = p.c_flag
        return self
    
    def set_line(self, start: Pixel, end: Pixel) -> 'Canvas':
        self.__render_line( \
            start.x, start.y, end.x, end.y, \
            lambda x,y: self.set_pixel_pos(x, y, start.c_flag))
        return self
    
    def __into_boundary(self, n: int, mi: int, mx: int) -> int:
        n = min(mx, n)
        return max(mi, n)

    # Bresenham's algorithm implemented from wikipedia
    def __render_line(self, x0: int, y0: int, x1: int, y1: int, f):
        x0 = self.__into_boundary(n=x0, mi=0, mx=self.width-1)
        x1 = self.__into_boundary(n=x1, mi=0, mx=self.width-1)
        y0 = self.__into_boundary(n=y0, mi=0, mx=self.height-1)
        y1 = self.__into_boundary(n=y1, mi=0, mx=self.height-1)
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1 # sign
        dy = -1 * abs(y1 - y0)
        sy = 1 if y0 < y1 else -1 # sign
        err = dx + dy
        while True:
            f(x0, y0)
            if x0 == x1 and y0==y1: break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
    
    def set_pixels(self, pixels: List[Pixel]) -> 'Canvas':
        for pixel in pixels:
            self.set_pixel(pixel)
        return self
