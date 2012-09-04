import unittest
import os
import json
import app
import colorific

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
        im = colorific.load_image(path=self._imgpath('lenna.jpg'))
        self.assertTrue(im)

    def test_extract_colors(self):
        im = colorific.load_image(path=self._imgpath('lenna.jpg'))
        colors = colorific.extract_colors(im)
        self.assertTrue(colors)

    def test_load_url(self):
        pass


if __name__ == '__main__':
    unittest.main()
