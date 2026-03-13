import os
import subprocess
import ast
import glob

def add_setting(key, value):
    """Add/update settings.py"""
    settings_path = _find_settings()
    if not settings_path:
        print("⚠ settings.py not found")
        return
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    try:
        parsed_value = ast.literal_eval(value)
        value_str = repr(parsed_value)
    except:
        value_str = value
    
    if f"{key} =" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith(f"{key} ="):
                lines[i] = f"{key} = {value_str}"
                break
        content = '\n'.join(lines)
    else:
        content += f"\n{key} = {value_str}\n"
    
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print(f"✓ {key} set")

def install_package(package):
    """Install package and add to INSTALLED_APPS"""
    subprocess.run(['pip', 'install', package], check=True)
    
    settings_path = _find_settings()
    if not settings_path:
        print(f"✓ {package} installed")
        return
    
    with open(settings_path, 'r') as f:
        content = f.read()
    
    app_name = package.replace('-', '_')
    
    if 'INSTALLED_APPS' in content and f"'{app_name}'" not in content:
        content = content.replace('INSTALLED_APPS = [', f"INSTALLED_APPS = [\n    '{app_name}',")
        with open(settings_path, 'w') as f:
            f.write(content)
        print(f"✓ {package} installed and added to INSTALLED_APPS")
    else:
        print(f"✓ {package} installed")

def _find_settings():
    """Find settings.py"""
    for pattern in ['settings.py', '*/settings.py', 'config/settings.py']:
        if '*' in pattern:
            matches = glob.glob(pattern)
            if matches:
                return matches[0]
        elif os.path.exists(pattern):
            return pattern
    return None
