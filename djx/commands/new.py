import os
import subprocess
import sys

def create_project(project_name, no_venv, no_git):
    """Create new Django project with full setup"""
    
    print(f"🚀 Creating Django project: {project_name}")
    
    # Create project directory
    if os.path.exists(project_name):
        print(f"❌ Directory {project_name} already exists")
        sys.exit(1)
    
    os.makedirs(project_name)
    os.chdir(project_name)
    
    # Create virtual environment
    if not no_venv:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Determine pip path
        pip_path = 'venv/bin/pip' if os.name != 'nt' else 'venv\\Scripts\\pip.exe'
        python_path = 'venv/bin/python' if os.name != 'nt' else 'venv\\Scripts\\python.exe'
        
        # Install Django
        print("📥 Installing Django...")
        subprocess.run([pip_path, 'install', 'django'], check=True)
    else:
        pip_path = 'pip'
        python_path = sys.executable
    
    # Create Django project
    print("🏗️  Creating Django project structure...")
    subprocess.run(['django-admin', 'startproject', project_name, '.'], check=True)
    
    # Create .gitignore
    gitignore = """*.pyc
__pycache__/
*.egg-info/
dist/
build/
.pytest_cache/
*.db
*.sqlite3
venv/
.env
.vscode/
.idea/
*.log
"""
    with open('.gitignore', 'w') as f:
        f.write(gitignore)
    
    # Create README
    readme = f"""# {project_name}

Django project created with djx.

## Setup

```bash
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Commands

```bash
djx scaffold Post title:string content:text
djx routes
djx destroy scaffold Post
```
"""
    with open('README.md', 'w') as f:
        f.write(readme)
    
    # Run initial migration
    print("🗄️  Running initial migrations...")
    subprocess.run([python_path, 'manage.py', 'migrate'], check=True)
    
    # Initialize git
    if not no_git:
        print("📝 Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    print(f"\n✅ Project {project_name} created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    if not no_venv:
        activate_cmd = 'source venv/bin/activate' if os.name != 'nt' else 'venv\\Scripts\\activate'
        print(f"  {activate_cmd}")
    print(f"  python manage.py runserver")
    print(f"\nScaffold your first model:")
    print(f"  djx scaffold Post title:string content:text")
