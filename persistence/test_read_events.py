from events import Event, Link, SimpleDBv2
import unittest
import os

class TestEventsDB(unittest.TestCase):

    def test_from_links_nonterminals(self):
        left = Link(x=10,y=20,c_flag=5)
        right = Link(x=34,y=66,c_flag=5)
        expected = Event(sx=10,sy=20,ex=34,ey=66,c_flag=5)
        result = Event.from_link_pair(left, right)
        self.assertTrue(expected == result)

    def test_from_links_terminal_left(self):
        left = Link(x=10,y=20,c_flag=255)
        right = Link(x=34,y=66,c_flag=5)
        result = Event.from_link_pair(left, right)
        self.assertIsNone(result)

    def test_from_links_terminal_right(self):
        left = Link(x=10,y=20,c_flag=5)
        right = Link(x=34,y=66,c_flag=255)
        expected = Event(sx=10,sy=20,ex=34,ey=66,c_flag=5)
        result = Event.from_link_pair(left, right)
        self.assertTrue(expected == result)

    def test_from_links_different_colors(self):
        left = Link(x=10,y=20,c_flag=5)
        right = Link(x=34,y=66,c_flag=6)
        result = Event.from_link_pair(left, right)
        self.assertIsNone(result)
    
    def test_from_link_list_nonterminals(self):
        left = Link(x=10,y=20,c_flag=5)
        right = Link(x=34,y=66,c_flag=5)
        expected = Event(sx=10,sy=20,ex=34,ey=66,c_flag=5)
        result = list(Event.from_links([left, right]))

        count = 0
        for ev in result:
            count += 1
            self.assertTrue(expected == result[0])
        self.assertEqual(1, count)
    
    def test_from_link_list_three(self):
        first = Link(x=10,y=20,c_flag=5)
        second = Link(x=34,y=66,c_flag=5)
        third = Link(x=55,y=96,c_flag=5)
        expected_first = Event(sx=10,sy=20,ex=34,ey=66,c_flag=5)
        expected_second = Event(sx=34,sy=66,ex=55,ey=96,c_flag=5)
        result = list(Event.from_links([first, second, third]))

        count = 0
        for ev in result:
            count += 1
        self.assertEqual(2, count)
        self.assertTrue(expected_first == result[0])
        self.assertTrue(expected_second == result[1])
    
    def test_from_link_list_four_terminal_second(self):
        first = Link(x=10,y=20,c_flag=5)
        second = Link(x=34,y=66,c_flag=255)
        third = Link(x=55,y=96,c_flag=6)
        fourth = Link(x=72,y=61,c_flag=6)
        expected_first = Event(sx=10,sy=20,ex=34,ey=66,c_flag=5)
        expected_second = Event(sx=55,sy=96,ex=72,ey=61,c_flag=6)
        result = list(Event.from_links([first, second, third, fourth]))

        count = 0
        for ev in result:
            count += 1
        self.assertEqual(2, count)
        self.assertTrue(expected_first == result[0])
        self.assertTrue(expected_second == result[1])
    
    def test_getAllEvents_oneEvent(self):
        db = get_db()
        expected = Event(sx=10,sy=15,ex=20,ey=25,c_flag=10)
        db.addEvent(expected)
        events = list(db.getAllEvents(500))
        db.close()
        self.assertEqual(expected, events[0])
    
    def test_getAllEvents_twoEvent_connected(self):
        db = get_db()
        expected_first = Event(sx=10,sy=15,ex=20,ey=25,c_flag=10)
        expected_second = Event(sx=20,sy=25,ex=50,ey=75,c_flag=10)
        db.addEvent(expected_first)
        db.addEvent(expected_second)
        events = list(db.getAllEvents(500))
        db.close()
        self.assertEqual(expected_first, events[0])
        self.assertEqual(expected_second, events[1])
    
    def test_getAllEvents_threeEvent_twoBlocks(self):
        db = get_db()
        expected_first = Event(sx=10,sy=15,ex=20,ey=25,c_flag=10)
        expected_second = Event(sx=20,sy=25,ex=50,ey=75,c_flag=10)
        expected_third = Event(sx=50,sy=75,ex=100,ey=200,c_flag=10)
        db.addEvent(expected_first)
        db.addEvent(expected_second)
        db.addEvent(expected_third)
        events = list(db.getAllEvents(2))
        db.close()
        self.assertEqual(expected_first, events[0])
        self.assertEqual(expected_second, events[1])
        self.assertEqual(expected_third, events[2])
    
    def test_getAllEvents_threeEvent_pointDraws(self):
        db = get_db()
        expected_first = Event(sx=10,sy=15,ex=10,ey=15,c_flag=10)
        expected_second = Event(sx=20,sy=25,ex=20,ey=25,c_flag=10)
        expected_third = Event(sx=100,sy=200,ex=100,ey=200,c_flag=10)
        db.addEvent(expected_first)
        db.addEvent(expected_second)
        db.addEvent(expected_third)
        events = list(db.getAllEvents(2))
        db.close()
        self.assertEqual(expected_first, events[0])
        self.assertEqual(expected_second, events[1])
        self.assertEqual(expected_third, events[2])

    def test_getAllEvents_zeroEvents(self):
        db = get_db()
        events = list(db.getAllEvents(2))
        db.close()
        self.assertEqual(0, len(events))

    @classmethod
    def tearDownClass(cls):
        kill_db()

def get_db():
    return SimpleDBv2("test_events.db", "wb+")

def kill_db():
    os.remove("test_events.db")

if __name__ == '__main__':
    unittest.main()