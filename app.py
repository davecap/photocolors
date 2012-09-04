import os
from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import BadRequest
import requests
import colorific

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
        index accepts GET or POST at '/'

        GET parameters:
            url: the URL for an image
        POST parameters:
            image: an uploaded image file

        returns:
            jsonified data with 3 or 5 hex colors
    """
    app.logger.info('Request received at /')
    if request.method == 'GET':
        app.logger.debug('GET request')
        url = request.args.get('url', False)
        if not url:
            raise BadRequest('Missing url parameter.')
        app.logger.info('Image URL: %s', url)
        r = requests.get(url)
        if r.status_code != 200:
            raise BadRequest('Invalid image URL: %s', url)
        im = colorific.load_image(data=r.content)
    else:
        # handles an image upload
        f = request.files['image']
        im = colorific.load_image(data=f.stream)
    # extract colors
    colors = colorific.extract_colors(im)
    return jsonify({'colors': colors})


@app.route('/url')
def url():
    """Interactive test view for any URL"""
    return render_template('url.html')


@app.route('/test')
def test():
    """Shows the test image palettes"""
    from test import TestPhotoColors, BASE_DIR
    images = []
    for img in TestPhotoColors.TEST_PHOTOS:
        path = os.path.join(BASE_DIR, 'static/photos/', img)
        im = colorific.load_image(path=path)
        colors = colorific.extract_colors(im)
        images.append({'url': '/static/photos/%s' % img, 'colors': colors})
    return render_template('test.html', images=images)


if __name__ == "__main__":
    app.run(debug=True)
