from pathlib import Path
from ..utils import to_class_name, pluralize

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
    context_object_name = '{pluralize(model_lower)}'

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
    
    (template_dir / f"{model_lower}_list.html").write_text(f"""<h1>{pluralize(class_name)}</h1>
<a href="{{% url '{model_lower}-create' %}}">New {class_name}</a>
<ul>
{{% for item in {pluralize(model_lower)} %}}
  <li><a href="{{% url '{model_lower}-detail' item.pk %}}">{{{{ item }}}}</a> | <a href="{{% url '{model_lower}-update' item.pk %}}">Edit</a> | <a href="{{% url '{model_lower}-delete' item.pk %}}">Delete</a></li>
{{% endfor %}}
</ul>""")
    
    (template_dir / f"{model_lower}_form.html").write_text(f"""<h1>{{{{ object.pk|yesno:"Edit,New" }}}} {class_name}</h1>
<form method="post">{{% csrf_token %}}{{{{ form.as_p }}}}<button type="submit">Save</button></form>
<a href="{{% url '{model_lower}-list' %}}">Cancel</a>""")
    
    (template_dir / f"{model_lower}_detail.html").write_text(f"""<h1>{class_name}</h1>
<p>{{{{ object }}}}</p>
<a href="{{% url '{model_lower}-update' object.pk %}}">Edit</a> | <a href="{{% url '{model_lower}-delete' object.pk %}}">Delete</a> | <a href="{{% url '{model_lower}-list' %}}">Back</a>""")
    
    (template_dir / f"{model_lower}_confirm_delete.html").write_text(f"""<h1>Delete {class_name}?</h1>
<form method="post">{{% csrf_token %}}<button type="submit">Confirm</button></form>
<a href="{{% url '{model_lower}-list' %}}">Cancel</a>""")
    
    print(f"✓ Views and templates created")
