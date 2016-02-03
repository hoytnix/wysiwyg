#!/usr/bin/env python

"""
blueprints
~~~~~~~~~~

M(V)C.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Blueprint, render_template

from .models import Site, SiteSetting, user


blueprints = Blueprint('blueprints', __name__, template_folder='templates/pages')

@blueprints.route('/')
def site_list():
    sites = Site.query.all()
    c = {
        'user': user,
    }
    #print(c['settings'])
    return render_template('site_list.html', sites=sites, **c)


