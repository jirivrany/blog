# -*- coding: utf8 -*-    
'''
#todo
štítky - přes kategorie?
cache - https://github.com/thadeusb/flask-cache/ ?

#done
minimalistický systém  - mám
markdown pro zápis - mám
syntax highlite pro zdrojáky - mám
permalinky jeden-clanek-jaro-nedela - mám

#vyřazeno
vyzkoušet si mongoDB ? - to je overkill na tohle
frozen flask ? statická stránka - lepší necha to na fw

ch
'''

import flask
import markdown
import codecs
import os
import io
import json
import blogdata

app = flask.Flask(__name__)
app.debug = True

ROOT = os.path.join(app.root_path, u'pages')


@app.route('/')
def home():
    name = 'index.markdown'
    filename = os.path.join(ROOT, name)
    try:
        input_file = io.open(filename, encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text, extensions=['codehilite'])
    except IOError:
        flask.abort(404)
    else:
        title = u'Jirka Vraný - texty o programování'
        return flask.render_template('index.html', html=html, title=title)

@app.route('/<topic>/<title>/')
def test_param(topic, title):
    filename = "%s/%s.markdown" % (topic, title)
    fname = os.path.join(ROOT, filename)
    try:
        input_file = io.open(fname, encoding="utf-8")
    except IOError:
        flask.abort(404)
    else:        
        text = input_file.read()
        html = markdown.markdown(text, extensions=['codehilite'])
        title = blogdata.TITLES[title]
        return flask.render_template('page.html', html=html, title=title)

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('error_404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)       
