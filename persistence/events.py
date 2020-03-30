from typing import List, Iterable
from collections import namedtuple
from itertools import chain
from threading import Lock
import os

"""
Why not just use a SQL implementation?

I'm learning Python and would like the experience.
Using a SQL library will come later.
"""

# Made as immutable as possible
class Link:
    bytes_per = 5
    terminal_flag = 255
    def __init__(self, bytearr: bytes = None, x: int = None, y: int = None, c_flag: int = None, prev: 'Link' = None, nxt: 'Link' = None):
        if not bytearr:
            bytearr = bytearray()
            bytearr += x.to_bytes(2, "big", signed=True)
            bytearr += y.to_bytes(2, "big", signed=True)
            bytearr += c_flag.to_bytes(1, "big")
        self.bs = bytearr
        self.next = nxt
        self.prev = prev

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
        return int.from_bytes(self.bs[0:2], "big", signed=True)

    def get_y(self):
        return int.from_bytes(self.bs[2:4], "big", signed=True)

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
        return Link(x=self.get_x(), y=self.get_y(), c_flag=self.get_c_flag(), prev=self.prev, nxt=self.next)
    
    def clone_as_terminal(self) -> 'Link':
        return Link(x=self.get_x(), y=self.get_y(), c_flag=Link.terminal_flag, prev=self.prev, nxt=self.next)
    
    def is_terminal(self) -> bool:
        return self.get_c_flag() == Link.terminal_flag
    
    def is_connected(self, next_link: 'Link') -> bool:
        return self == next_link
    
    def set_next(self, next_link: 'Link') -> 'Link':
        new_self = self.clone()
        new_next = next_link.clone()
        if(not next_link.is_terminal() and self.is_connected(next_link)):
            new_next = next_link.next
        elif not self.is_connected(next_link):
            new_self = new_self.clone_as_terminal()
        new_self.next = new_next
        if new_next: new_next.prev = new_self
        if new_self.prev: new_self.prev.next = new_self
        return new_self

class Event:
    def __init__(self, bs: bytes = None, sx: int = None, sy: int = None, ex: int = None, ey: int = None, c_flag: int = None):
        if(bs):
            self.bs = bs
        else:
            b_arr = bytearray()
            b_arr += sx.to_bytes(2, "big", signed=True)
            b_arr += sy.to_bytes(2, "big", signed=True)
            b_arr += ex.to_bytes(2, "big", signed=True)
            b_arr += ey.to_bytes(2, "big", signed=True)
            b_arr += c_flag.to_bytes(1, "big")
            self.bs = b_arr

    def __eq__(self, value):
        if not isinstance(value, Event):
            return False
        return self.as_tuple().__eq__(value.as_tuple())
    
    def __str__(self):
        return str(self.as_tuple())

    def get_sx(self):
        return int.from_bytes(self.bs[0:2], "big", signed=True)

    def get_sy(self):
        return int.from_bytes(self.bs[2:4], "big", signed=True)

    def get_ex(self):
        return int.from_bytes(self.bs[4:6], "big", signed=True)

    def get_ey(self):
        return int.from_bytes(self.bs[6:8], "big", signed=True)

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
    
    @staticmethod
    def from_link_pair(left: Link, right: Link) -> 'Event':
        if left.is_terminal(): return None
        if left.get_c_flag() == right.get_c_flag() or right.is_terminal():
            return Event(sx=left.get_x(), sy=left.get_y(), ex=right.get_x(), ey=right.get_y(), c_flag=left.get_c_flag())
        if left.get_c_flag() != right.get_c_flag(): return None

    
    @staticmethod
    def from_links(links: Iterable[Link]) -> Iterable['Event']:
        def event_gen():
            iterator = iter(links)
            try:
                curr_left = next(iterator)
                curr_right = next(iterator)
                while True:
                    try:
                        ev = Event.from_link_pair(curr_left, curr_right)
                        if ev: yield ev
                        curr_left = curr_right
                        curr_right = next(iterator)  
                    except StopIteration:
                        break
            except StopIteration:
                pass
        return event_gen()

class EventCR:
    def addEvent(self, e: Event) -> Event:
        """Append the event to the end of the sequence"""
        pass

    def getLinks(self, startId: int, count: int) -> List[Link]:
        """Fetch event #s in sequence"""
        pass

    def getAllEvents(self, blocklength: int) -> List[Link]:
        """Get all events, block-by-block"""
        pass

class SimpleDBv2(EventCR):
    def __init__(self, fname: str, mode: str):
        self.db = open(fname, mode)
        self.fname = os.path.basename(self.db.name)
        self.lock = Lock()

    def addEvent(self, e: Event) -> bytearray:
        self.lock.acquire()
        tail = self.get_tail(count=1)
        next_link = e.as_link()
        last_link_head = tail[0].set_next(next_link) if tail else next_link
        written = self.__write_link(last_link_head)
        self.lock.release()
        return written
    
    def __fsize(self):
        return os.stat(self.fname).st_size
    
    # Read the links and convert them into Events
    # This is all done lazily by reading blocks of links
    # So the entire file doesn't need to load into memory
    def getAllEvents(self, blocklength: int) -> Iterable[Event]:
        self.lock.acquire()
        fsize = os.stat(self.fname).st_size
        self.lock.release()
        # By using a lock, we can create a closure synchronizing on fsize
        # fsize will never decrease due to a write
        # Only the last byte of the file can change, which is a byte we ignore here
        def link_gen():
            startId = 0
            while (startId * Link.bytes_per) < fsize:
                yield self.__get_links_block(startId=startId, count=blocklength)
                startId += blocklength
        
        return Event.from_links(chain.from_iterable(link_gen()))
    
    # Since only the last byte can change during a write
    # and we aren't concerned with it, we don't need to lock
    def __get_links_block(self, startId: int, count: int) -> Iterable[Link]:
        if count == 0:
            return []
        fsize = self.__fsize()
        blocksize = count * Link.bytes_per
        if fsize < blocksize:
            return self.__get_links_block(startId=startId, count=(fsize // Link.bytes_per) - startId)
        self.db.seek(startId * Link.bytes_per)
        res = self.db.read(blocksize)
        return list(map(lambda link_bytes: Link(link_bytes), chunks(res, Link.bytes_per)))

    def get_tail(self, count=1) -> Link:
        fsize = self.__fsize()
        if fsize < Link.bytes_per:
            return None
        startByte = fsize - (count * Link.bytes_per)
        return self.__get_links_block(startId=(startByte // Link.bytes_per), count=count)

    def __write_link(self, link: Link):
        link_as_bytes = link.as_bytes()
        seek_start = max(0, self.__fsize() - Link.bytes_per)
        self.db.seek(seek_start)
        self.db.write(link_as_bytes)
        self.db.flush()
        os.fsync(self.db.fileno())
        return link_as_bytes

    def close(self):
        self.db.close()
    
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
