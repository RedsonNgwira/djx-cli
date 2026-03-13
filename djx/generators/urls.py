import os
import glob
from ..utils import to_class_name

def wire_urls(app_name, model_name):
    """Auto-wire URLs"""
    class_name = to_class_name(model_name)
    model_lower = model_name.lower()
    
    # Create app urls.py
    urls_code = f"""from django.urls import path
from . import views

urlpatterns = [
    path('', views.{class_name}ListView.as_view(), name='{model_lower}-list'),
    path('<int:pk>/', views.{class_name}DetailView.as_view(), name='{model_lower}-detail'),
    path('new/', views.{class_name}CreateView.as_view(), name='{model_lower}-create'),
    path('<int:pk>/edit/', views.{class_name}UpdateView.as_view(), name='{model_lower}-update'),
    path('<int:pk>/delete/', views.{class_name}DeleteView.as_view(), name='{model_lower}-delete'),
]
"""
    
    with open(f"{app_name}/urls.py", 'w') as f:
        f.write(urls_code)
    
    # Find project urls.py (exclude app urls.py files)
    project_urls = None
    
    # Look for project_name/urls.py pattern
    for pattern in ['*/urls.py']:
        matches = sorted(glob.glob(pattern))
        for match in matches:
            # Skip if it's an app urls.py (inside app directory)
            if match.startswith(app_name + '/'):
                continue
            # Check if this looks like a project urls.py (has settings.py sibling)
            dir_name = match.split('/')[0]
            if os.path.exists(f"{dir_name}/settings.py"):
                project_urls = match
                break
        if project_urls:
            break
    
    if not project_urls:
        print(f"⚠ Add to urls.py: path('{app_name}/', include('{app_name}.urls'))")
        return
    
    try:
        with open(project_urls, 'r') as f:
            lines = f.readlines()
        
        include_line = f"    path('{app_name}/', include('{app_name}.urls')),\n"
        
        # Check if already wired
        if any(f"'{app_name}.urls'" in line for line in lines):
            print(f"✓ URLs already wired")
            return
        
        # Add include to imports - find and replace the import line
        import_fixed = False
        for i, line in enumerate(lines):
            # Only look at actual import lines (start with 'from')
            if line.startswith('from django.urls import'):
                if 'include' not in line:
                    # Replace entire line with include added
                    lines[i] = 'from django.urls import include, path\n'
                    import_fixed = True
                elif 'include' in line:
                    import_fixed = True  # Already has include
                break
        
        # Add path to urlpatterns
        urlpatterns_found = False
        for i, line in enumerate(lines):
            if 'urlpatterns = [' in line:
                lines.insert(i + 1, include_line)
                urlpatterns_found = True
                break
        
        if urlpatterns_found:
            with open(project_urls, 'w') as f:
                f.writelines(lines)
            if import_fixed:
                print(f"✓ URLs wired to {project_urls}")
            else:
                print(f"⚠ URLs added to {project_urls} (check imports)")
        else:
            print(f"⚠ Could not find urlpatterns in {project_urls}")
        
    except Exception as e:
        print(f"⚠ Error wiring URLs: {e}")
        print(f"   Add manually: path('{app_name}/', include('{app_name}.urls'))")
