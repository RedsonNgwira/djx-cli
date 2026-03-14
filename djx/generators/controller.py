from pathlib import Path
from ..utils import to_class_name

def generate(name, app_name):
    """Generate views and templates"""
    class_name = to_class_name(name)
    model_lower = name.lower()
    
    views_code = f"""from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import {class_name}

class {class_name}ListView(ListView):
    model = {class_name}
    template_name = '{app_name}/{model_lower}_list.html'
    context_object_name = '{model_lower}_list'
    paginate_by = 10

class {class_name}DetailView(DetailView):
    model = {class_name}
    template_name = '{app_name}/{model_lower}_detail.html'

class {class_name}CreateView(CreateView):
    model = {class_name}
    template_name = '{app_name}/{model_lower}_form.html'
    fields = '__all__'
    success_url = reverse_lazy('{model_lower}-list')

class {class_name}UpdateView(UpdateView):
    model = {class_name}
    template_name = '{app_name}/{model_lower}_form.html'
    fields = '__all__'
    success_url = reverse_lazy('{model_lower}-list')

class {class_name}DeleteView(DeleteView):
    model = {class_name}
    template_name = '{app_name}/{model_lower}_confirm_delete.html'
    success_url = reverse_lazy('{model_lower}-list')
"""
    
    with open(f"{app_name}/views.py", 'w') as f:
        f.write(views_code)
    
    template_dir = Path(f"{app_name}/templates/{app_name}")
    template_dir.mkdir(parents=True, exist_ok=True)
    
    # Better list template
    (template_dir / f"{model_lower}_list.html").write_text(f"""<!DOCTYPE html>
<html>
<head>
    <title>{class_name} List</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        a {{ color: #4CAF50; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .btn {{ padding: 5px 10px; margin: 2px; }}
    </style>
</head>
<body>
    <h1>{class_name} List</h1>
    <a href="{{% url '{model_lower}-create' %}}" class="btn">+ New {class_name}</a>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>{class_name}</th>
                <th>Created</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {{% for item in {model_lower}_list %}}
            <tr>
                <td>{{{{ item.pk }}}}</td>
                <td><a href="{{% url '{model_lower}-detail' item.pk %}}">{{{{ item }}}}</a></td>
                <td>{{{{ item.created_at|date:"Y-m-d H:i" }}}}</td>
                <td>
                    <a href="{{% url '{model_lower}-update' item.pk %}}" class="btn">Edit</a>
                    <a href="{{% url '{model_lower}-delete' item.pk %}}" class="btn">Delete</a>
                </td>
            </tr>
            {{% empty %}}
            <tr><td colspan="4">No {class_name} records yet.</td></tr>
            {{% endfor %}}
        </tbody>
    </table>
    
    {{% if is_paginated %}}
    <div>
        {{% if page_obj.has_previous %}}
            <a href="?page={{{{ page_obj.previous_page_number }}}}">Previous</a>
        {{% endif %}}
        Page {{{{ page_obj.number }}}} of {{{{ page_obj.paginator.num_pages }}}}
        {{% if page_obj.has_next %}}
            <a href="?page={{{{ page_obj.next_page_number }}}}">Next</a>
        {{% endif %}}
    </div>
    {{% endif %}}
</body>
</html>""")
    
    # Better form template
    (template_dir / f"{model_lower}_form.html").write_text(f"""<!DOCTYPE html>
<html>
<head>
    <title>{{{{ object.pk|yesno:"Edit,New" }}}} {class_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        form {{ max-width: 600px; }}
        label {{ display: block; margin-top: 10px; font-weight: bold; }}
        input, textarea, select {{ width: 100%; padding: 8px; margin-top: 5px; }}
        button {{ margin-top: 20px; padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }}
        button:hover {{ background: #45a049; }}
        a {{ color: #4CAF50; }}
    </style>
</head>
<body>
    <h1>{{{{ object.pk|yesno:"Edit,New" }}}} {class_name}</h1>
    <form method="post">
        {{% csrf_token %}}
        {{{{ form.as_p }}}}
        <button type="submit">Save</button>
        <a href="{{% url '{model_lower}-list' %}}">Cancel</a>
    </form>
</body>
</html>""")
    
    # Better detail template
    (template_dir / f"{model_lower}_detail.html").write_text(f"""<!DOCTYPE html>
<html>
<head>
    <title>{class_name} Details</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .detail {{ max-width: 600px; }}
        .field {{ margin: 10px 0; }}
        .label {{ font-weight: bold; }}
        a {{ color: #4CAF50; text-decoration: none; margin-right: 10px; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{class_name} Details</h1>
    <div class="detail">
        <div class="field"><span class="label">ID:</span> {{{{ object.pk }}}}</div>
        <div class="field"><span class="label">Created:</span> {{{{ object.created_at }}}}</div>
        <div class="field"><span class="label">Updated:</span> {{{{ object.updated_at }}}}</div>
        <hr>
        {{{{ object }}}}
    </div>
    <div>
        <a href="{{% url '{model_lower}-update' object.pk %}}">Edit</a>
        <a href="{{% url '{model_lower}-delete' object.pk %}}">Delete</a>
        <a href="{{% url '{model_lower}-list' %}}">Back to List</a>
    </div>
</body>
</html>""")
    
    # Better delete confirmation
    (template_dir / f"{model_lower}_confirm_delete.html").write_text(f"""<!DOCTYPE html>
<html>
<head>
    <title>Delete {class_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .warning {{ color: red; font-weight: bold; }}
        button {{ padding: 10px 20px; margin: 10px 5px 0 0; cursor: pointer; }}
        .delete {{ background: #f44336; color: white; border: none; }}
        .delete:hover {{ background: #da190b; }}
        a {{ color: #4CAF50; text-decoration: none; padding: 10px 20px; }}
    </style>
</head>
<body>
    <h1>Delete {class_name}?</h1>
    <p class="warning">Are you sure you want to delete "{{{{ object }}}}"?</p>
    <p>This action cannot be undone.</p>
    <form method="post">
        {{% csrf_token %}}
        <button type="submit" class="delete">Yes, Delete</button>
        <a href="{{% url '{model_lower}-list' %}}">Cancel</a>
    </form>
</body>
</html>""")
    
    print(f"✓ Views and templates created")
