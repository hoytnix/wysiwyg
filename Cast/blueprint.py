#!/usr/bin/env python

"""
blueprints
~~~~~~~~~~

M(V)C.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Blueprint, render_template

from models import bootstrap_template, user, page_titles


blueprints = Blueprint('blueprints', __name__, template_folder='templates')

@blueprints.route('/', defaults={'path': ''})
@blueprints.route('/<path:path>')
def view(path):
    route = path.split('/')

    if route.__len__() == 1:
        page_path = route[0]
        if page_path == '':
            route_str = 'index'
        else:
            route_str = page_path
    else:
        dir_path = '/'.join(route[0:-1])
        if route[-1] == '':
            page_path = 'index'
        else:
            page_path = ''.join(route[1:])
        route_str = '{}/{}'.format(dir_path, page_path)

    c = {
        'title': page_titles[route_str],
        'template': bootstrap_template,
        'user': user,
        'macro_dir': 'pages/{}'.format('/'.join(route))
    }
    return render_template('pages/{}.html'.format(route_str), **c)

