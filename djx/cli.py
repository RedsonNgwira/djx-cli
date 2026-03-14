import click
from .generators import scaffold, model, controller, migration
from .config import add_setting, install_package

class DJXGroup(click.Group):
    def resolve_command(self, ctx, args):
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError:
            click.echo(click.style(f"\n❌ Unknown command: '{args[0]}'", fg='red'))
            click.echo(click.style("\n📚 Available commands:", fg='cyan'))
            for cmd, desc in [
                ("new", "Create a new Django project"),
                ("scaffold", "Generate full CRUD feature"),
                ("model", "Generate model only"),
                ("controller", "Generate views and templates"),
                ("destroy", "Remove generated code"),
                ("routes", "Show all URL routes"),
                ("add", "Install and configure a package"),
                ("wire", "Wire app URLs to project"),
            ]:
                click.echo(f"  djx {cmd:<12} — {desc}")
            click.echo(click.style("\n💡 AI tools sometimes suggest commands that don't exist yet.", fg='yellow'))
            click.echo("   https://github.com/RedsonNgwira/djx-cli for the real roadmap.\n")
            raise SystemExit(1)

@click.group(cls=DJXGroup)
def cli():
    """djx - Convention over Configuration for Django"""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--no-venv', is_flag=True, help='Skip virtual environment creation')
@click.option('--no-git', is_flag=True, help='Skip git initialization')
@click.option('--venv/--no-venv', default=True, prompt='Create virtual environment?', 
              help='Create virtual environment (default: yes)')
def new(project_name, no_venv, no_git, venv):
    """Create new Django project with everything configured"""
    from .commands.new import create_project
    # If --no-venv flag is used, it overrides the prompt
    skip_venv = no_venv or not venv
    create_project(project_name, skip_venv, no_git)

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
@click.argument('resource_type')
@click.argument('name')
def destroy(resource_type, name):
    """Destroy scaffold/model/controller (e.g: djx destroy scaffold Post)"""
    from .commands.destroy import destroy_resource
    destroy_resource(resource_type, name)

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

@cli.command()
def routes():
    """Display all URL routes"""
    from .commands.routes import show_routes
    show_routes()

if __name__ == '__main__':
    cli()
