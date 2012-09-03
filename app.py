import requests
from flask import *
from werkzeug import secure_filename
from photocolors import PhotoColors

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def colors():
    if request.method == 'GET':
        # get URL from GET params
        url = request.args.get('url')
        if url is None:
            return render_template('index.html')
        app.logger.info('URL: %s', url)
        # download the url
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Invalid image URL: %s', url)
        # process
        p = PhotoColors()
        p.load_data(r.content)
    else:
        # handle file upload
        f = request.files['image']
        fname = '/tmp/' + secure_filename(f.filename)
        f.save(fname)
        # process
        p = PhotoColors()
        p.load_path(fname)

    # extract colors
    p.distill()
    # render url & color palette
    return render_template('colors.html', imgurl=url, colors=p.colors)

if __name__ == "__main__":
    app.run(debug=True)
