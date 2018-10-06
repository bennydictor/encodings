import codecs
import encodings
import pkgutil
import urllib.parse

import werkzeug
from flask import Flask, request, abort, render_template, redirect, url_for

encs = {
    'base64': (
        lambda x: codecs.decode(x.encode('utf-8'), 'base64').decode('utf-8'),
        lambda x: codecs.encode(x.encode('utf-8'), 'base64').decode('utf-8')),
    'hex': (
        lambda x: codecs.decode(x.encode('utf-8'), 'hex').decode('utf-8'),
        lambda x: codecs.encode(x.encode('utf-8'), 'hex').decode('utf-8')),
    'url': (
        lambda x: werkzeug.url_decode('q=' + x)['q'],
        lambda x: werkzeug.url_encode({'q': x})[2:]),
    'punycode': (
        lambda x: codecs.decode(x, 'punycode'),
        lambda x: codecs.encode(x, 'punycode').decode('utf-8')),
}

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html',
            encs=list(encs.keys()),
            text='')
    else:
        if 'submit_decode' in request.form and 'submit_encode' not in request.form:
            action = 'decode'
        elif 'submit_encode' in request.form and 'submit_decode' not in request.form:
            action = 'encode'
        else:
            abort(400)

        enc = request.form['enc']
        text = request.form['text']

        try:
            if action == 'decode':
                text = encs[enc][0](text)
            else:
                text = encs[enc][1](text)
            failed=None
        except Exception as e:
            failed = f'Failed to {action}'

        return render_template('index.html',
            encs=list(encs.keys()),
            text=text,
            selected_enc=enc,
            failed=failed)

@app.route('/robots.txt')
def robots():
    return redirect(url_for('static', filename='robots.txt'))

application = app
if __name__ == '__main__':
    app.run()
