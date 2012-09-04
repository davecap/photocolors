# PhotoColors
# Generates color schemes from photos
# Author: David Caplan <dcaplan@gmail.com>
import os
from StringIO import StringIO

try:
    from PIL import Image
except:
    import Image


class PhotoColors(object):

    def __init__(self, data=None, path=None):
        if data:
            self.load_data(data)
        elif path:
            self.load_path(path)

    @staticmethod
    def rgb2hex(rgb):
        return format((rgb[0] << 16) | (rgb[1] << 8) | rgb[2], '06x')

    def load_data(self, data):
        self.im = Image.open(StringIO(data))

    def load_path(self, path):
        """Load an image to PIL Image from path"""
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise Exception('Invalid photo file path: %s', self.path)
        self.im = Image.open(self.path)

    def filter_palette(self):
        def is_not_a_shade(c):
            """returns true if rgb color is black/white/gray"""
            rgb = c[1]
            return not (abs(rgb[0] - rgb[1]) < 15
                    and abs(rgb[1] - rgb[2]) < 15
                    and abs(rgb[0] - rgb[2]) < 15)
        return filter(is_not_a_shade, self.palette)

    def process(self):
        """Convert the loaded image to a 3 or 5 color palette"""
        # quantize to a smaller 256 color image
        p = self.im.convert("P", palette=Image.ADAPTIVE, colors=256)
        p.save('outbig.gif')
        # resize to shrink the number of pixels to analyze
        p = p.resize((64, 64))
        p.save('outsmall.gif')
        # convert back to RGB to get RGB data
        p = p.convert("RGB").getdata()
        # get all the colors
        self.palette = p.getcolors(p.size[0] * p.size[1])
        # filter greys
        self.palette = self.filter_palette()
        # sort by frequency
        self.palette = sorted(self.palette, key=lambda x: x[0], reverse=1)
        # if the first 3 colors are 75% of all colors... use top 3
        # if sum([c[0] for c in self.palette[:3]]) / 256.00 >= 0.75:
        #     self.palette = self.palette[:3]
        # else:
        #     self.palette = self.palette[:4]
        self.colors = [PhotoColors.rgb2hex(c[1]) for c in self.palette[:5]]
