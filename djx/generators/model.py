from ..utils import ensure_app, parse_fields, to_class_name, pluralize
import os
import glob

FIELD_MAP = {
    'string': 'models.CharField(max_length=255)',
    'text': 'models.TextField()',
    'integer': 'models.IntegerField()',
    'boolean': 'models.BooleanField(default=False)',
    'date': 'models.DateField()',
    'datetime': 'models.DateTimeField()',
    'decimal': 'models.DecimalField(max_digits=10, decimal_places=2)',
    'email': 'models.EmailField()',
    'url': 'models.URLField()',
}

def find_model_app(model_name):
    """Find which app contains a model"""
    for app_dir in glob.glob('*/models.py'):
        app = app_dir.split('/')[0]
        with open(app_dir, 'r') as f:
            if f'class {model_name}(' in f.read():
                return app
    return None

def generate(name, fields, app_name):
    """Generate Django model"""
    ensure_app(app_name)
    class_name = to_class_name(name)
    parsed_fields = parse_fields(fields)
    
    model_code = f"""from django.db import models

class {class_name}(models.Model):
"""
    
    for field_name, field_type in parsed_fields:
        if field_type.startswith('references'):
            # Handle references:ModelName or just references (use field name)
            if ':' in field_type:
                ref_model = field_type.split(':', 1)[1]
            else:
                ref_model = field_name
            ref_model = to_class_name(ref_model)
            
            # Find the app that contains this model
            ref_app = find_model_app(ref_model)
            if ref_app:
                model_code += f"    {field_name} = models.ForeignKey('{ref_app}.{ref_model}', on_delete=models.CASCADE)\n"
            else:
                # Fallback: assume it's in the same app or use app.Model format
                model_code += f"    {field_name} = models.ForeignKey('{ref_model}', on_delete=models.CASCADE)  # TODO: Add app label if needed\n"
        else:
            model_code += f"    {field_name} = {FIELD_MAP.get(field_type, 'models.CharField(max_length=255)')}\n"
    
    model_code += """    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.__class__.__name__} {self.pk}"

    class Meta:
        ordering = ['-created_at']
"""
    
    with open(f"{app_name}/models.py", 'w') as f:
        f.write(model_code)
    
    print(f"✓ Model created: {app_name}/models.py")
