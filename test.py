import unittest
import os
import json
from photocolors import PhotoColors
import app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TestAPI(unittest.TestCase):
    TEST_URL = 'http://pcdn.500px.net/13076147/170238409a79c575c116c293fb687cbe482e9196/4.jpg'

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_connect(self):
        resp = self.app.get('/test')
        self.assertEquals(resp.status_code, 200)

    def test_GET(self):
        resp = self.app.get('/?url=%s' % self.TEST_URL)
        self.assertEquals(resp.status_code, 200)
        json_data = json.loads(resp.data)
        self.assertTrue('colors' in json_data)
        self.assertTrue(json_data['colors'])

    def test_POST(self):
        pass


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
