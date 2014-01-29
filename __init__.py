# -*- coding: utf8 -*-    
'''
co chci?
minimalistický systém 
markdown pro zápis
syntax highlite pro zdrojáky
permalinky jeden-clanek-jaro-nedela
štítky
vyzkoušet si mongoDB ?
cache - https://github.com/thadeusb/flask-cache/ ?
frozen flask ? statická stránka

'''

import flask
import markdown
import codecs
import os
import io
import json

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
        html = "<h1>%s</h1>" % filename

    return flask.render_template('index.html', html=html)

@app.route('/deploy/', methods=['POST'])
def deploy():
    jsondata = json.loads(flask.request.data)
    url = jsondata['repository']['url']
    print url
    return "ok"

@app.route('/deploy/', methods=['GET'])
def deploy_get():
    flask.abort(404)


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
        return flask.render_template('page.html', html=html)

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('error_404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)       
