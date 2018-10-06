from .site_codecs import Codec

from flask import Blueprint
from flask import abort, redirect, render_template, request, url_for

__all__ = ['bp']


bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html',
            encs=Codec.codecs.keys())
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
            codec = Codec(enc)
        except KeyError:
            abort(400)

        failed = None
        try:
            if action == 'decode':
                text = codec.decode(text)
            else:
                text = codec.encode(text)
        except UnicodeError:
            failed = f'Failed to {action}'

        return render_template('index.html',
            encs=Codec.codecs.keys(),
            text=text,
            selected_enc=enc,
            failed=failed)

@bp.route('/robots.txt')
def robots():
    return redirect(url_for('static', filename='robots.txt'))
