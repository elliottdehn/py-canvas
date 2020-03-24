from typing import List
from mmap import mmap
import os

class Event:
    bytesPerEvent = 9
    def __init__(self, bytes):
        self.bytes = bytes

class EventCR:
    def addEvent(self, e: Event) -> Event:
        """Append the event to the end of the sequence"""
        pass

    def getEvents(self, startId: int, count: int) -> List[Event]:
        """Fetch event #s in sequence"""
        pass

class SimpleDB(EventCR):
    
    def addEvent(self, e: Event) -> Event:
        f = open("events.db", "ab+")
        print(e.bytes)
        f.write(e.bytes)
        f.close()
        return e
    
    def getEvents(self, startId: int, count: int) -> List[Event]:
        if count < 1:
            return None
        f = open("events.db", "rb+")
        mm = mmap(f.fileno(), length=count * Event.bytesPerEvent, offset=startId * Event.bytesPerEvent)
        f.close()
        return list(map(lambda bs: Event(bs), group_per(mm, Event.bytesPerEvent)))

def group_per(source, step):
    return [source[sliceStart:sliceStart+step] for sliceStart in range(0, len(source), step)]