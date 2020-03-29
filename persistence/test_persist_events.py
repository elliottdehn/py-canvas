import unittest
from event.events import Link, Event, SimpleDBv2
import os

class TestEventsDB(unittest.TestCase):
    
    def test_link_as_bytes(self):
        expected = to_bytearray([pos(1000), pos(2000), color(15)])
        result = Link(x=1000, y=2000, c_flag=15).as_bytes()
        self.assertEqual(expected, result)

    def test_link_is_connected_same_color(self):
        first = Link(x=100,y=200,c_flag=5)
        second = Link(x=100,y=200,c_flag=5)
        self.assertTrue(first.is_connected(second))
    
    def test_link_set_next_not_connected(self):
        first = Link(x=100,y=200,c_flag=5)
        expected_first = Link(x=100,y=200,c_flag=255)
        second = Link(x=200,y=400,c_flag=5)
        result = first.set_next(second)
        self.assertTrue(result == expected_first)
        self.assertTrue(result.next == second)

    def test_link_set_next_is_connected(self):
        first = Link(x=100,y=200,c_flag=5)
        expected_first = Link(x=100,y=200,c_flag=5)

        second = Link(x=100,y=200,c_flag=5,next=Link(x=200,y=400,c_flag=5))
        expected_second = second.next

        self.assertTrue(first == expected_first)
        self.assertTrue(first.next == expected_second)

    def test_link_is_connected_diff_color(self):
        first = Link(x=100,y=200,c_flag=5)
        second = Link(x=100,y=200,c_flag=10)
        self.assertFalse(first.is_connected(second))
    
    def test_db_add_event_one(self):
        db = SimpleDBv2("test_events.db")
        event = Event(sx=5, sy=10, ex=100, ey=150, c_flag=10)
        expected = to_bytearray([pos(5), pos(10), color(10), pos(100), pos(150), color(10)])
        result = db.addEvent(event)
        db.close()
        self.assertEqual(expected, result)
    
    def test_db_add_event_two_connected(self):
        db = SimpleDBv2("test_events.db")
        event_1 = Event(sx=5, sy=10, ex=100, ey=150, c_flag=10)
        event_2 = Event(sx=100, sy=150, ex=120, ey=130, c_flag=10)
        expected = to_bytearray([ \
            pos(100), pos(150), color(10), \
            pos(120), pos(130), color(10)])
        db.addEvent(event_1)
        result = db.addEvent(event_2)
        db.close()
        self.assertEqual(expected, result)
    
    def test_db_add_event_two_disconnected(self):
        db = SimpleDBv2("test_events.db")
        event_1 = Event(sx=5, sy=10, ex=100, ey=150, c_flag=10)
        event_2 = Event(sx=101, sy=151, ex=120, ey=130, c_flag=10)
        expected = to_bytearray([ \
            pos(100), pos(150), color(255), \
            pos(101), pos(151), color(10), \
            pos(120), pos(130), color(10)])
        db.addEvent(event_1)
        result = db.addEvent(event_2)
        db.close()
        self.assertEqual(expected, result)
    
        
    def test_db_add_event_two_disconnected_color(self):
        db = SimpleDBv2("test_events.db")
        event_1 = Event(sx=5, sy=10, ex=100, ey=150, c_flag=10)
        event_2 = Event(sx=100, sy=150, ex=120, ey=130, c_flag=11)
        expected = to_bytearray([ \
            pos(100), pos(150), color(255), \
            pos(100), pos(150), color(11), \
            pos(120), pos(130), color(11)])
        db.addEvent(event_1)
        result = db.addEvent(event_2)
        db.close()
        self.assertEqual(expected, result)
    
    @classmethod
    def tearDownClass(cls):
        os.remove("./test_events.db")
    
def pos(i):
    return (i, 2)

def color(i):
    return (i, 1)

def to_bytearray(iterable) -> bytearray:
    b = bytearray()
    for value, length in iterable:
        b += value.to_bytes(length, "big")
    return b

if __name__ == '__main__':
    unittest.main()