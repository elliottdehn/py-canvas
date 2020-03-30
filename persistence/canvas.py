from typing import List
from threading import Lock
import itertools

class Pixel:

    def __init__(self, x: int, y: int, c_flag: int):
        self.x = x
        self.y = y
        self.c_flag = c_flag

class Canvas:

    def __init__(self, width: int, height: int, db = None):
        self.arr = list(Canvas.__chunks([0]*width*height, width))
        self.width = width
        self.height= height
        self.lock = Lock()
        if db:
            evs = db.getAllEvents(blocklength=500)
            for ev in evs:
                start_pixel = Pixel(x=ev.get_sx(),y=ev.get_sy(),c_flag=ev.get_c_flag())
                end_pixel = Pixel(x=ev.get_ex(),y=ev.get_ey(),c_flag=ev.get_c_flag())
                self.set_line(start_pixel, end_pixel)
    
    # Top left is 0,0 // for tests only
    def get_pixel(self, x: int, y: int):
        self.lock.acquire()
        res = Pixel(x, y, self.arr[y][x])
        self.lock.release()
        return res
    
    def set_line(self, start: Pixel, end: Pixel) -> 'Canvas':
        self.lock.acquire()
        self.__render_line( \
            start.x, start.y, end.x, end.y, \
            lambda x,y: self.__set_pixel_pos(x, y, start.c_flag))
        self.lock.release()
        return self
    
    def as_bytes(self):
        self.lock.acquire()
        bytearr = bytearray()
        for c_flag in itertools.chain.from_iterable(self.arr):
            bytearr += c_flag.to_bytes(1, "big")
        self.lock.release()
        return bytes(bytearr)
    
    def __set_pixel_pos(self, x, y, c_flag):
        return self.__set_pixel(Pixel(x, y, c_flag))
    
    def __set_pixel(self, p: Pixel) -> 'Canvas':
        self.arr[p.y][p.x] = p.c_flag
        return self

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
    
    def __into_boundary(self, n: int, mi: int, mx: int) -> int:
        n = min(mx, n)
        return max(mi, n)
    
    def __set_pixels(self, pixels: List[Pixel]) -> 'Canvas':
        for pixel in pixels:
            self.__set_pixel(pixel)
        return self
    
    @staticmethod
    def __chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
