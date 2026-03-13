import os
from datetime import datetime

def generate(name):
    """Generate empty migration"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    apps = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(f"{d}/migrations")]
    app = apps[0] if apps else 'core'
    
    migration_code = f"""from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = []
"""
    
    os.makedirs(f"{app}/migrations", exist_ok=True)
    migration_path = f"{app}/migrations/{timestamp}_{name}.py"
    
    with open(migration_path, 'w') as f:
        f.write(migration_code)
    
    print(f"✓ Migration: {migration_path}")
