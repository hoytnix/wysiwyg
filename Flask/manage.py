#!/usr/bin/env python

"""
manage
~~~~~~

CLI.

Having a task-queue and self-healing architecture should depreceate this.

:copyright: (c) 2016 Michael Hoyt. <@pr0xmeh>
:license: Anavah.
"""

import click

from flask import current_app

from Framework.app import create_app
from Framework.extensions import db
from Framework.utils.imports import all_models
from Framework.utils.populate import populate_all


@click.group()
@click.version_option()
def cli():
    """Doc-string.
    """


@cli.command('start')
def run_server():
    app = create_app()
    app.run(host='0.0.0.0', port=13337, debug=True)


@cli.command('resetdb')
@click.option('-f', '--fix', is_flag=True)
def resetdb(fix):
    models = all_models()

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.app_context():
        if fix:
            populate_all()


@cli.command('test')
def test():
    from Framework.utils.fs import abs_fs

    print(abs_fs)


if __name__ == '__main__':
    cli()
