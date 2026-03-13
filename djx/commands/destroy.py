import os
import shutil
import glob
import re

def destroy_resource(resource_type, name):
    """Destroy generated resources"""
    
    if resource_type not in ['scaffold', 'model', 'controller', 'app']:
        print(f"❌ Unknown resource type: {resource_type}")
        print("   Use: scaffold, model, controller, or app")
        return
    
    from ..utils import pluralize, to_class_name
    
    # Determine app name
    app_name = pluralize(name).lower()
    class_name = to_class_name(name)
    
    if not os.path.exists(app_name):
        print(f"❌ App {app_name} not found")
        return
    
    print(f"🗑️  Destroying {resource_type}: {name}")
    
    if resource_type in ['scaffold', 'app']:
        # Remove entire app directory
        if os.path.exists(app_name):
            shutil.rmtree(app_name)
            print(f"✓ Removed {app_name}/ directory")
        
        # Remove from INSTALLED_APPS
        _remove_from_installed_apps(app_name)
        
        # Remove URL include
        _remove_url_include(app_name)
        
        # Remove migrations
        _remove_migrations(app_name)
        
    elif resource_type == 'model':
        # Just remove model from models.py
        model_file = f"{app_name}/models.py"
        if os.path.exists(model_file):
            with open(model_file, 'r') as f:
                content = f.read()
            
            # Remove the model class
            pattern = rf'class {class_name}\(.*?\):.*?(?=\nclass |\Z)'
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            with open(model_file, 'w') as f:
                f.write(content)
            print(f"✓ Removed {class_name} from {model_file}")
        
    elif resource_type == 'controller':
        # Remove views and templates
        if os.path.exists(f"{app_name}/views.py"):
            os.remove(f"{app_name}/views.py")
            print(f"✓ Removed {app_name}/views.py")
        
        if os.path.exists(f"{app_name}/templates"):
            shutil.rmtree(f"{app_name}/templates")
            print(f"✓ Removed {app_name}/templates/")
    
    print(f"\n✅ {resource_type.capitalize()} {name} destroyed")
    print("⚠️  Run: python manage.py makemigrations && python manage.py migrate")

def _remove_from_installed_apps(app_name):
    """Remove app from INSTALLED_APPS in settings.py"""
    for settings_file in glob.glob('*/settings.py'):
        try:
            with open(settings_file, 'r') as f:
                content = f.read()
            
            if f"'{app_name}'" in content:
                # Remove the line with the app
                lines = content.split('\n')
                lines = [line for line in lines if f"'{app_name}'" not in line]
                content = '\n'.join(lines)
                
                with open(settings_file, 'w') as f:
                    f.write(content)
                print(f"✓ Removed from INSTALLED_APPS in {settings_file}")
        except:
            pass

def _remove_url_include(app_name):
    """Remove URL include from project urls.py"""
    for urls_file in glob.glob('*/urls.py'):
        if urls_file.startswith(app_name):
            continue
        
        try:
            with open(urls_file, 'r') as f:
                content = f.read()
            
            if f"'{app_name}.urls'" in content:
                lines = content.split('\n')
                lines = [line for line in lines if f"'{app_name}.urls'" not in line]
                content = '\n'.join(lines)
                
                with open(urls_file, 'w') as f:
                    f.write(content)
                print(f"✓ Removed URL include from {urls_file}")
        except:
            pass

def _remove_migrations(app_name):
    """Remove migration references"""
    print(f"⚠️  Manually remove migrations for {app_name} if needed")
