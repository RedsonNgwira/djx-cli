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
                ("db", "Run migrations (djx db) or reset (djx db reset)"),
                ("console", "Django shell with all models auto-imported"),
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

@cli.command()
def console():
    """Open Django shell with all models auto-imported"""
    import subprocess, sys, os, glob

    if not os.path.exists('manage.py'):
        click.echo("❌ No Django project found. Run from project root.")
        sys.exit(1)

    model_imports = []
    for models_file in glob.glob('*/models.py'):
        app = models_file.split('/')[0]
        with open(models_file) as f:
            for line in f:
                if line.startswith('class ') and 'Model' in line:
                    model_name = line.split('(')[0].replace('class ', '').strip()
                    model_imports.append(f"from {app}.models import {model_name}")

    names = ', '.join(l.split()[-1] for l in model_imports)
    startup = '\n'.join(model_imports) + f'\nprint("✓ Models loaded: {names}")'

    click.echo(click.style("🐍 Django Console — all models imported", fg='green'))
    os.environ['PYTHONSTARTUP'] = ''
    subprocess.run([sys.executable, 'manage.py', 'shell', '-c',
        startup + '\nimport code; code.interact(local=locals())'])

@cli.command()
@click.argument('action', default='', required=False)
def db(action):
    """Database shortcuts: djx db (migrate), djx db reset"""
    import subprocess, sys
    if action == 'reset':
        click.echo("🗄️  Resetting database...")
        subprocess.run([sys.executable, 'manage.py', 'flush', '--no-input'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        click.echo(click.style("✅ Database reset!", fg='green'))
    else:
        click.echo("🗄️  Running migrations...")
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        click.echo(click.style("✅ Done!", fg='green'))

if __name__ == '__main__':
    cli()
