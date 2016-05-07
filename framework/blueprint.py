"""The (V)iew in M(V)C."""

from flask import Blueprint, render_template

from .models.element import Element
from .models.route import Route
from .models.setting import Setting
from .models.site import Site
from .models.template import Template

from .utils.fs import abs_fs


blueprints = Blueprint('blueprints', __name__, template_folder=abs_fs['templates/pages'])


@blueprints.route('/')
def site_list():
    """Index Sites."""

    sites = Site.query.all()
    return render_template('site_list.html', sites=sites)


@blueprints.route('/<site_url>')
def site_detail(site_url):
    """Query a Site, and its properties."""

    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()
    return render_template('site_detail.html', site=site, **settings)


@blueprints.route('/<site_url>/<path:path>')
def route_detail(site_url, path):
    """Query an element_dict from a Route, and give it to the template engine."""

    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()

    route = Route.query.filter_by(parent=site.id).first()
    template = route.child

    template.element_dict  # Does nothing but call the function for the verbosity.

    return render_template('route_detail.html', **settings)
