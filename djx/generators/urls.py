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
    for pattern in ['*/urls.py']:
        matches = glob.glob(pattern)
        # Filter out app urls.py, keep only project urls.py
        for match in matches:
            if not match.startswith(app_name + '/'):
                project_urls = match
                break
        if project_urls:
            break
    
    if not project_urls:
        print(f"⚠ Add to urls.py: path('{app_name}/', include('{app_name}.urls'))")
        return
    
    try:
        with open(project_urls, 'r') as f:
            content = f.read()
        
        include_line = f"    path('{app_name}/', include('{app_name}.urls')),"
        
        if include_line in content or f"'{app_name}.urls'" in content:
            print(f"✓ URLs already wired")
            return
        
        # Add include import if missing
        if 'from django.urls import' in content and 'include' not in content:
            content = content.replace('from django.urls import', 'from django.urls import include,')
        
        # Add path to urlpatterns
        if 'urlpatterns = [' in content:
            content = content.replace('urlpatterns = [', f'urlpatterns = [\n{include_line}')
            with open(project_urls, 'w') as f:
                f.write(content)
            print(f"✓ URLs wired to {project_urls}")
        else:
            print(f"⚠ Add to {project_urls}: path('{app_name}/', include('{app_name}.urls'))")
    except Exception as e:
        print(f"⚠ Add to urls.py: path('{app_name}/', include('{app_name}.urls'))")
