import os
import subprocess
import re

def ensure_app(app_name):
    """Create Django app if it doesn't exist"""
    if not os.path.exists(app_name):
        subprocess.run(['python', 'manage.py', 'startapp', app_name], check=True)
        print(f"✓ App created: {app_name}")
        
        try:
            settings_files = ['settings.py', '*/settings.py', 'config/settings.py']
            for pattern in settings_files:
                if '*' in pattern:
                    import glob
                    matches = glob.glob(pattern)
                    if matches:
                        settings_path = matches[0]
                        break
                elif os.path.exists(pattern):
                    settings_path = pattern
                    break
            else:
                return
            
            with open(settings_path, 'r') as f:
                content = f.read()
            
            if f"'{app_name}'" not in content:
                content = content.replace('INSTALLED_APPS = [', f"INSTALLED_APPS = [\n    '{app_name}',")
                with open(settings_path, 'w') as f:
                    f.write(content)
        except:
            pass

def parse_fields(fields):
    """Parse field definitions (name:type)"""
    parsed = []
    for field in fields:
        if ':' in field:
            name, ftype = field.split(':', 1)
            parsed.append((name, ftype))
        else:
            parsed.append((field, 'string'))
    return parsed

def to_class_name(name):
    """Convert to PascalCase"""
    return ''.join(word.capitalize() for word in re.split(r'[_\-]', name))

def pluralize(word):
    """Simple pluralization"""
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    return word + 's'

def singularize(word):
    """Simple singularization"""
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('es'):
        return word[:-2]
    elif word.endswith('s'):
        return word[:-1]
    return word
