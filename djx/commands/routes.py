import os
import sys
import importlib.util

def show_routes():
    """Display all URL routes in a table"""
    
    # Check if we're in a Django project
    if not os.path.exists('manage.py'):
        print("❌ Not in a Django project directory")
        return
    
    # Setup Django
    sys.path.insert(0, os.getcwd())
    
    # Find settings module
    import glob
    settings_files = glob.glob('*/settings.py')
    if not settings_files:
        print("❌ Could not find settings.py")
        return
    
    settings_module = settings_files[0].replace('/', '.').replace('.py', '')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    try:
        import django
        django.setup()
        from django.urls import get_resolver
        from django.urls.resolvers import URLPattern, URLResolver
    except Exception as e:
        print(f"❌ Error loading Django: {e}")
        return
    
    print("\n📍 Routes\n")
    print(f"{'URL Pattern':<50} {'Name':<30} {'View':<40}")
    print("=" * 120)
    
    def extract_routes(urlpatterns, prefix=''):
        routes = []
        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                # Nested URL patterns
                new_prefix = prefix + str(pattern.pattern)
                routes.extend(extract_routes(pattern.url_patterns, new_prefix))
            elif isinstance(pattern, URLPattern):
                # Actual URL pattern
                url = prefix + str(pattern.pattern)
                name = pattern.name or ''
                
                # Get view name
                if hasattr(pattern.callback, '__name__'):
                    view = pattern.callback.__name__
                elif hasattr(pattern.callback, 'view_class'):
                    view = pattern.callback.view_class.__name__
                else:
                    view = str(pattern.callback)
                
                routes.append((url, name, view))
        return routes
    
    resolver = get_resolver()
    routes = extract_routes(resolver.url_patterns)
    
    # Sort by URL
    routes.sort(key=lambda x: x[0])
    
    for url, name, view in routes:
        print(f"{url:<50} {name:<30} {view:<40}")
    
    print(f"\n✓ Total routes: {len(routes)}\n")
