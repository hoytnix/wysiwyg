#!/usr/bin/env python

"""
blueprints
~~~~~~~~~~

M(V)C.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Blueprint, render_template

from models import bootstrap_template, user


blueprints = Blueprint('blueprints', __name__, template_folder='templates/pages')

@blueprints.route('/')
def index():
    c = {
        'title': 'Index',
        'template': bootstrap_template,
        'user': user,
    }
    return render_template('index.html', **c)


