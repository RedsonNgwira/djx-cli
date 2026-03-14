from .model import generate as gen_model
from .controller import generate as gen_controller
from .urls import wire_urls

def generate(name, fields, app_name):
    """Generate full scaffold"""
    app_name = app_name or name.lower()
    
    gen_model(name, fields, app_name)
    gen_controller(name, app_name)
    wire_urls(app_name, name)
    
    print(f"\n✓ Scaffold complete for {name}")
    print(f"Next: python manage.py makemigrations && python manage.py migrate")
