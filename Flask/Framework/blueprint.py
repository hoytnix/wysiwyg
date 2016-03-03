#!/usr/bin/env python

"""
anavah.blueprints
~~~~~~~~~~~~~~~~~

M(V)C.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

from flask import Blueprint, render_template

from .models import (Site, SiteSetting, SiteRoute, SiteTemplate, TemplateElement, \
                     ElementAttribute)
from .utils.fs import abs_fs

blueprints = Blueprint('blueprints', __name__, template_folder=abs_fs['templates/pages'])

@blueprints.route('/')
def site_list():
    sites = Site.query.all()
    return render_template('site_list.html', sites=sites)


@blueprints.route('/<site_url>')
def site_detail(site_url):
    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()
    return render_template('site_detail.html', site=site, **settings)

@blueprints.route('/<site_url>/<path:path>')
def route_detail(site_url, path):
    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()

    route = SiteRoute.query.filter_by(parent=site.id).first()
    template = route.child

    e = template.element_dict

    return render_template('route_detail.html', **settings)

