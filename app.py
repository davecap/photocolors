from functools import wraps
from flask import Flask, request, current_app, render_template, jsonify
from werkzeug.exceptions import BadRequest
import requests
from photocolors import PhotoColors

app = Flask(__name__)


def handle_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function


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
    if request.method == 'GET':
        url = request.args.get('url', False)
        if not url:
            raise BadRequest('Missing url parameter.')
        app.logger.info('URL: %s', url)
        r = requests.get(url)
        if r.status_code != 200:
            raise BadRequest('Invalid image URL: %s', url)
        p = PhotoColors(data=r.content)
    else:
        # handles an image upload
        f = request.files['image']
        p = PhotoColors(data=f.stream)
    # extract colors
    p.distill()
    return jsonify({'colors': p.colors})


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)
