import click
from .generators import scaffold, model, controller, migration
from .config import add_setting, install_package

@click.group()
def cli():
    """djx - Convention over Configuration for Django"""
    pass

@cli.command()
@click.argument('name')
@click.argument('fields', nargs=-1)
@click.option('--app', default=None)
def scaffold(name, fields, app):
    """Generate model, views, templates, URLs (e.g: djx scaffold Post title:string body:text)"""
    from .generators.scaffold import generate
    generate(name, fields, app)

@cli.command()
@click.argument('name')
@click.argument('fields', nargs=-1)
@click.option('--app', default=None)
def model(name, fields, app):
    """Generate model only"""
    from .generators.model import generate
    generate(name, fields, app)

@cli.command()
@click.argument('name')
@click.option('--app', default=None)
def controller(name, app):
    """Generate views and templates"""
    from .generators.controller import generate
    generate(name, app)

@cli.command()
@click.argument('name')
def migration(name):
    """Generate empty migration"""
    from .generators.migration import generate
    generate(name)

@cli.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Set settings.py value (e.g: djx config ALLOWED_HOSTS '["*"]')"""
    add_setting(key, value)

@cli.command()
@click.argument('package')
def add(package):
    """Install package and add to INSTALLED_APPS"""
    install_package(package)

@cli.command()
@click.argument('app_name')
def wire(app_name):
    """Wire app URLs to project urls.py"""
    from .generators.urls import wire_urls
    wire_urls(app_name, app_name)

if __name__ == '__main__':
    cli()
