import unittest
import os
from photocolors import PhotoColors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestPhotoColors(unittest.TestCase):
    TEST_PHOTOS = [
        'tiger.jpg',
        'waterfall.jpeg',
        'lenna.jpg'
    ]

    def setUp(self):
        self.image_dir = os.path.join(BASE_DIR, 'photos')

    def _imgpath(self, path):
        return os.path.join(self.image_dir, path)

    def test_image_path(self):
        self.assertTrue(os.path.exists(self.image_dir))

    def test_load_image(self):
        pc = PhotoColors()
        pc.load_path(self._imgpath('lenna.jpg'))
        self.assertTrue(pc.im)

    def test_distill_single(self):
        pc = PhotoColors()
        pc.load_path(self._imgpath('lenna.jpg'))
        pc.distill()
        self.assertTrue(pc.colors)

    def test_distill_multiple(self):
        pc = PhotoColors()
        for p in self.TEST_PHOTOS:
            pc.load_path(self._imgpath(p))
            pc.distill()
            self.assertTrue(pc.colors)

    def test_load_url(self):
        pass

    def test_rgb2hex(self):
        test_colors = [
            ['000000', (0, 0, 0)],
            ['ff0000', (255, 0, 0)],
            ['00ff00', (0, 255, 0)],
            ['0000ff', (0, 0, 255)],
            ['ffff00', (255, 255, 0)],
            ['00ffff', (0, 255, 255)],
            ['ff00ff', (255, 0, 255)],
            ['c0c0c0', (192, 192, 192)],
            ['ffffff', (255, 255, 255)]
        ]
        for h, r in test_colors:
            self.assertEqual(h, PhotoColors.rgb2hex(r))

if __name__ == '__main__':
    unittest.main()
