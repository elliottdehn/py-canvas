from typing import List
from mmap import mmap
import os

class Event:
    bytesPerEvent = 9
    def __init__(self, bs: bytes):
        self.bs = bs

class EventCR:
    def addEvent(self, e: Event) -> Event:
        """Append the event to the end of the sequence"""
        pass

    def getEvents(self, startId: int, count: int) -> List[Event]:
        """Fetch event #s in sequence"""
        pass

class SimpleDB(EventCR):

    def __init__(self):
        self.db = open("events.db", "ab+")
    
    def addEvent(self, e: Event) -> Event:
        self.db.write(e.bs)
        self.db.flush()
        os.fsync(self.db.fileno())
        return e
    
    def getEvents(self, startId: int, count: int) -> List[Event]:
        if count < 1:
            return None
        mm = mmap(self.db.fileno(), length=count * Event.bytesPerEvent, offset=startId * Event.bytesPerEvent)
        return list(map(lambda bs: Event(bs), group_per(mm, Event.bytesPerEvent)))

def group_per(source, step):
    return [source[sliceStart: sliceStart + step] for sliceStart in range(0, len(source), step)]