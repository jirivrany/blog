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

app = flask.Flask(__name__)
app.debug = True

ROOT = os.path.join(app.root_path, u'pages')

@app.route('/')
def home():
    name = 'python/pokus.markdown'
    filename = os.path.join(ROOT, name)
    try:
        input_file = io.open(filename, encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text, extensions=['codehilite'])
    except IOError:
        html = "<h1>{}</h1>".format(filename)

    return flask.render_template('index.html', html=html)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username    

@app.route('/<topic>/<filename>/')
def test_param(topic, filename):
    print topic
    print filename
    fname = os.path.join(ROOT, "{}/{}.markdown".format(topic, filename))
    try:
        input_file = io.open(fname, encoding="utf-8")
    except IOError:
        flask.abort(404)
    else:        
        text = input_file.read()
        html = markdown.markdown(text, extensions=['codehilite'])
        return flask.render_template('index.html', html=html)

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('error_404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)       
