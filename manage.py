"""Command line interface.

Having a task-queue and self-healing architecture should depreceate this.
"""

import click

from framework.app import create_app
from framework.extensions import db
from framework.utils.imports import all_models
from framework.utils.populate import populate_all


@click.group()
@click.version_option()
def cli():
    """Entry-point."""


@cli.command('start')
def run_server():
    """Execute the application."""

    app = create_app()
    app.run(host='0.0.0.0', port=13337, debug=True)


@cli.command('resetdb')
@click.option('-f', '--fix', is_flag=True)
def resetdb(fix):
    """Drop the database, and refixture it."""

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
    """Execute a function only reachable within the project namespace."""

    from Framework.utils.fs import abs_fs

    print(abs_fs)


if __name__ == '__main__':
    cli()
