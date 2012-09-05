     ____  _           _         ____      _                
    |  _ \| |__   ___ | |_ ___  / ___|___ | | ___  _ __ ___ 
    | |_) | '_ \ / _ \| __/ _ \| |   / _ \| |/ _ \| '__/ __|
    |  __/| | | | (_) | || (_) | |__| (_) | | (_) | |  \__ \
    |_|   |_| |_|\___/ \__\___/ \____\___/|_|\___/|_|  |___/
                                                            

# API to obtain a HEX color scheme from an image.

## Python usage

    import requests
    import json

    photocolors_url = 'http://127.0.0.1:5000/'
    image_url = 'http://upload.wikimedia.org/wikipedia/en/2/24/Lenna.png'
    res = requests.get(photocolors_url, params={'url': image_url})

    print json.loads(res.content)

## JQuery usage

    var url = 'http://upload.wikimedia.org/wikipedia/en/2/24/Lenna.png';
    var photocolors_url = 'http://127.0.0.1:5000/'
    $.get(photocolors_url, {
        url: url
    }, function(data) {
        console.log(data.colors);
    });
