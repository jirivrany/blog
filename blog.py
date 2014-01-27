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

app = flask.Flask(__name__)
app.debug = True

@app.route('/')
def hello():
   raise Exception('Deliberate exception raised')

@app.route('/index/')
def hiorme():
    input_file = codecs.open("pages/python/pokus.markdown", mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text, extensions=['codehilite'])
    return flask.render_template('index.html', html=html)

@app.route('/<topic>/<filename>/')
def test_param(topic, filename):
    try:
        input_file = codecs.open("pages/{}/{}.markdown".format(topic, filename), mode="r", encoding="utf-8")
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
