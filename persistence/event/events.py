from typing import List
from collections import namedtuple
from itertools import chain
import os

"""
Why not just use a SQL implementation?

I'm learning Python and would like the experience.
Using a SQL library will come later.
"""

# Made as immutable as possible
class Link:
    bytes_per = 5
    def __init__(self, bytearr: bytes = None, x: int = None, y: int = None, c_flag: int = None, prev: 'Link' = None, next: 'Link' = None):
        if not bytearr:
            bytearr = bytearray()
            bytearr += x.to_bytes(2, "big")
            bytearr += y.to_bytes(2, "big")
            bytearr += c_flag.to_bytes(1, "big")
        self.bs = bytearr
        self.next = None
        self.prev = None

    def __eq__(self, value):
        if not isinstance(value, Link):
            return False
        return self.as_tuple().__eq__(value.as_tuple())
    
    def __str__(self):
        curr = self
        s_arr = []
        while curr:
            s_arr.append(str(curr.as_tuple()))
            curr = curr.next
        return " -> ".join(s_arr)

    def get_x(self):
        return int.from_bytes(self.bs[0:2], "big")

    def get_y(self):
        return int.from_bytes(self.bs[2:4], "big")

    def get_c_flag(self):
        return int.from_bytes(self.bs[4:], "big")

    def as_tuple(self):
        link_tuple = namedtuple('LinkTuple', 'x y c_flag')
        return link_tuple(self.get_x(), self.get_y(), self.get_c_flag())
    
    def as_bytes(self):
        curr = self
        b_arr = bytearray()
        while curr:
            b_arr += curr.bs
            curr = curr.next
        return b_arr
        
    def clone(self) -> 'Link':
        return Link(x=self.get_x(), y=self.get_y(), c_flag=self.get_c_flag(), prev=self.prev, next=self.next)
    
    def clone_as_terminal(self) -> 'Link':
        return Link(x=self.get_x(), y=self.get_y(), c_flag=255, prev=self.prev, next=self.next)
    
    def is_connected(self, next_link: 'Link') -> bool:
        return self == next_link
    
    def set_next(self, next_link: 'Link') -> 'Link':
        new_self = self.clone() if self.is_connected(next_link) else self.clone_as_terminal()
        new_next = next_link.next if self.is_connected(next_link) else next_link
        new_self.next = new_next
        if new_next: new_next.prev = new_self
        if new_self.prev: new_self.prev.set_next(new_self)
        return new_self

class Event:
    def __init__(self, bs: bytes = None, sx: int = None, sy: int = None, ex: int = None, ey: int = None, c_flag: int = None):
        if(bs):
            self.bs = bs
        else:
            b_arr = bytearray()
            b_arr += sx.to_bytes(2, "big")
            b_arr += sy.to_bytes(2, "big")
            b_arr += ex.to_bytes(2, "big")
            b_arr += ey.to_bytes(2, "big")
            b_arr += c_flag.to_bytes(1, "big")
            self.bs = b_arr

    def __eq__(self, value):
        return self.as_tuple().__eq__(value)
    
    def __str__(self):
        return str(self.as_tuple())

    def get_sx(self):
        return int.from_bytes(self.bs[0:2], "big")

    def get_sy(self):
        return int.from_bytes(self.bs[2:4], "big")

    def get_ex(self):
        return int.from_bytes(self.bs[4:6], "big")

    def get_ey(self):
        return int.from_bytes(self.bs[6:8], "big")

    def get_c_flag(self):
        return int.from_bytes(self.bs[8:], "big")

    def get_start_link(self) -> Link:
        return Link(x=self.get_sx(), y=self.get_sy(), c_flag=self.get_c_flag())

    def get_end_link(self) -> Link:
        return Link(x=self.get_ex(), y=self.get_ey(), c_flag=self.get_c_flag())
    
    def as_link(self) -> Link:
        self_link = self.get_start_link()
        next_link = self.get_end_link()
        self_link.next = next_link
        next_link.prev = self_link
        return self_link

    def as_tuple(self):
        event_tuple = namedtuple('EventTuple', 'sx sy ex ey c_flag')
        return event_tuple(sx=self.get_sx(), sy=self.get_sy(), ex=self.get_ex(), ey=self.get_ey(), c_flag=self.get_c_flag())

class EventCR:
    def addEvent(self, e: Event) -> Event:
        """Append the event to the end of the sequence"""
        pass

    def getEvents(self, startId: int, count: int) -> List[Event]:
        """Fetch event #s in sequence"""
        pass

class SimpleDBv2(EventCR):
    def __init__(self, fname: str):
        self.db = open(fname, "wb+")
        self.fname = os.path.basename(self.db.name)

    def addEvent(self, e: Event) -> bytearray:
        tail = self.__get_tail()
        next_link = e.as_link()
        last_link_head = tail.set_next(next_link) if tail else next_link
        return self.__write_link(last_link_head, commit=True)

    def __get_tail(self, count=1) -> Link:
        fsize = os.stat(self.fname).st_size
        tailsize = count * Link.bytes_per
        if fsize < tailsize:
            return None
        off = fsize - tailsize
        self.db.seek(-1 * tailsize, os.SEEK_END)
        res = self.db.read()
        return Link(bytearr=res)

    def __write_link(self, link: Link, commit=True):
        link_as_bytes = link.as_bytes()
        self.db.seek(0, os.SEEK_END)
        seek_start = max(0, self.db.tell() - len(link_as_bytes))
        self.db.seek(-1*seek_start, os.SEEK_END)
        self.db.write(link_as_bytes)
        if commit:
            self.db.flush()
            os.fsync(self.db.fileno())
        return link_as_bytes

    def close(self):
        self.db.close()
