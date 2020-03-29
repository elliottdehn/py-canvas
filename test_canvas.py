from canvas import Canvas, Pixel
import unittest

class TestCanvas(unittest.TestCase):

    def test_set_line_diagonals(self):
        
        start_idx = 100
        end_idx = 200
        top_left = Pixel(x = start_idx, y = start_idx, c_flag=10)
        bottom_left = Pixel(x = start_idx, y = end_idx, c_flag=10)
        top_right = Pixel(x = end_idx, y = start_idx, c_flag=10)
        bottom_right = Pixel(x = end_idx, y = end_idx, c_flag=10)

        with self.subTest("diagonal test"):
            result = Canvas(width=500, height=500).set_line(top_left, bottom_right)
            for i in range(start_idx,end_idx):
                self.assertEqual(result.get_pixel(x=i,y=i).c_flag, 10)

        with self.subTest("diagonal test"):
            result = Canvas(width=500, height=500).set_line(bottom_right, top_left)
            for i in range(start_idx,end_idx):
                self.assertEqual(result.get_pixel(x=i,y=i).c_flag, 10)

        with self.subTest("diagonal test"):
            result = Canvas(width=500, height=500).set_line(bottom_left, top_right)
            for i in range(start_idx,end_idx):
                self.assertEqual(result.get_pixel(x=i,y=end_idx-i).c_flag, 10)

        with self.subTest("diagonal test"):
            result = Canvas(width=500, height=500).set_line(top_right, bottom_left)
            for i in range(start_idx,end_idx):
                self.assertEqual(result.get_pixel(x=i,y=end_idx-i).c_flag, 10)

    def test_set_line_vertical(self):
        start_idx = 100
        end_idx = 200
        top = Pixel(x=start_idx, y=start_idx, c_flag=10)
        bottom = Pixel(x=end_idx, y=start_idx, c_flag=10)
        
        with self.subTest("top down test"):
            result = Canvas(width=500, height=500).set_line(top, bottom)
            for i in range(start_idx, end_idx):
                self.assertEqual(result.get_pixel(x=i,y=i).c_flag, 10)
        
        with self.subTest("bottom up test"):
            result = Canvas(width=500, height=500).set_line(bottom, top)
            for i in range(start_idx, end_idx):
                self.assertEqual(result.get_pixel(x=i,y=i).c_flag, 10)
    
    def test_set_line_horizontal(self):
        start_idx = 100
        end_idx = 200
        left = Pixel(x=start_idx, y=start_idx, c_flag=10)
        right = Pixel(x=start_idx, y=end_idx, c_flag=10)
        
        with self.subTest("left right test"):
            result = Canvas(width=500, height=500).set_line(left, right)
            for i in range(start_idx, end_idx):
                self.assertEqual(result.get_pixel(x=start_idx,y=i).c_flag, 10)
        
        with self.subTest("right left test"):
            result = Canvas(width=500, height=500).set_line(right, left)
            for i in range(start_idx, end_idx):
                self.assertEqual(result.get_pixel(x=start_idx,y=i).c_flag, 10)
    
    def test_set_line_point(self):
        pt = Pixel(x=100,y=100,c_flag=10)
        result = Canvas(width=500, height=500).set_line(pt, pt)
        self.assertEqual(result.get_pixel(x=100,y=100).c_flag, 10)

if __name__ == '__main__':
    unittest.main()