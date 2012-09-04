from flask import Flask, request, render_template, jsonify
from werkzeug.exceptions import BadRequest
import requests
from photocolors import PhotoColors

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
        p = PhotoColors(data=r.content)
    else:
        # handles an image upload
        f = request.files['image']
        p = PhotoColors(data=f.stream)
    # extract colors
    p.process()
    return jsonify({'colors': p.colors})


@app.route('/test')
def test():
    """Interactive test view"""
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)
