from flask import Blueprint, render_template

from ..models.route import Route
from ..models.site import Site

from ..utils.fs import abs_fs


routes = Blueprint('routes', __name__, template_folder=abs_fs['templates/pages'])


@routes.route('/<site_url>/<path:path>')
def detail_view(site_url, path):
    """Query an element_dict from a Route, and give it to the template engine."""

    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()

    route = Route.query.filter_by(parent=site.id).first()
    template = route.child

    html = template.html

    return render_template('route_detail.html', html=html, **settings)
