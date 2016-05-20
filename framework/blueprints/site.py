from flask import Blueprint, render_template

from ..models.site import Site

from ..utils.fs import abs_fs


sites = Blueprint('sites', __name__, template_folder=abs_fs['templates/pages'])


@sites.route('/')
def list_view():
    """Index Sites."""

    sites = Site.query.all()
    return render_template('site_list.html', sites=sites)


@sites.route('/<site_url>')
def detail_view(site_url):
    """Query a Site, and its properties."""

    site = Site.query.filter_by(id=site_url).first()
    settings = site.settings_as_dict()
    return render_template('site_detail.html', site=site, **settings)
