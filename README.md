# djx-cli — Django Express

> Convention over configuration for Django. Inspired by Ruby on Rails.

[![PyPI](https://img.shields.io/pypi/v/djx-cli)](https://pypi.org/project/djx-cli/)
[![Python](https://img.shields.io/pypi/pyversions/djx-cli)](https://pypi.org/project/djx-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**3 commands. Full CRUD app. No boilerplate.**

```bash
pip install djx-cli
djx new myblog && cd myblog
djx scaffold Post title:string content:text published:boolean
python manage.py migrate && python manage.py runserver
# → http://127.0.0.1:8000/posts/ — list, create, edit, delete. Done.
```

---

## Why DJX?

Django is powerful but verbose. Starting a new feature means manually creating models, views, templates, URLs, and wiring them together. DJX does all of that in one command — the same way Rails has done it for 20 years.

| Task | Django | DJX |
|------|--------|-----|
| New project | `django-admin startproject` + manual venv + settings | `djx new myproject` |
| New CRUD feature | model + views + urls + templates (manual) | `djx scaffold Post title:string` |
| See all routes | no built-in command | `djx routes` |
| Remove a feature | delete files manually | `djx destroy scaffold Post` |

---

## Installation

```bash
pip install djx-cli
```

Requires Python 3.8+ and works with Django 4.2+.

---

## Quick Start

```bash
# 1. Create a new project — venv, Django, git, migrations all automatic
djx new myblog
cd myblog
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 2. Scaffold a full CRUD feature
djx scaffold Post title:string content:text published:boolean

# 3. Run migrations and start server
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/posts/` — you have a working list, create, edit, and delete. No code written.

---

## Commands

### `djx new <project>`
Create a new Django project with everything configured.

```bash
djx new myproject
```

Creates: Django project, git repository, README, initial migrations. Asks if you want a virtual environment created automatically.

---

### `djx scaffold <Model> <fields>`
Generate a complete CRUD feature — model, views, templates, and URLs all wired together.

```bash
djx scaffold Post title:string content:text published:boolean
djx scaffold Comment body:text author:string post:references:Post
```

Generates:
- `posts/models.py` — model with all fields
- `posts/views.py` — ListView, DetailView, CreateView, UpdateView, DeleteView
- `posts/templates/posts/` — list, detail, form, confirm_delete templates
- `posts/urls.py` — all routes
- Wired into project `urls.py` automatically
- Added to `INSTALLED_APPS` automatically

---

### `djx model <Model> <fields>`
Generate a model only (no views or templates).

```bash
djx model Article title:string body:text author:string
```

---

### `djx controller <Model>`
Generate views and templates for an existing model.

```bash
djx controller Post
```

---

### `djx destroy <type> <Model>`
Clean removal of a scaffold, model, or controller.

```bash
djx destroy scaffold Post    # removes app, URLs, INSTALLED_APPS entry
djx destroy model Post       # removes model only
djx destroy controller Post  # removes views and templates only
```

---

### `djx routes`
Display all registered URL routes in a clean table.

```bash
djx routes
```

```
📍 Routes
URL Pattern              Name           View
=====================================================
posts/                   post-list      ListView
posts/<int:pk>/          post-detail    DetailView
posts/new/               post-create    CreateView
posts/<int:pk>/edit/     post-update    UpdateView
posts/<int:pk>/delete/   post-delete    DeleteView
✓ Total routes: 28
```

---

### `djx add <package>`
Install a package and add it to `INSTALLED_APPS` automatically.

```bash
djx add django-crispy-forms
djx add djangorestframework
```

---

### `djx config <KEY> <value>`
Set a value in `settings.py` from the terminal.

```bash
djx config DEBUG False
djx config ALLOWED_HOSTS '["*"]'
```

---

### `djx wire <app>`
Manually wire an app's URLs into the project `urls.py`.

```bash
djx wire posts
```

---

## Field Types

| DJX type | Django field |
|----------|-------------|
| `string` | `CharField(max_length=200)` |
| `text` | `TextField()` |
| `integer` | `IntegerField()` |
| `boolean` | `BooleanField()` |
| `date` | `DateField()` |
| `datetime` | `DateTimeField()` |
| `decimal` | `DecimalField()` |
| `email` | `EmailField()` |
| `url` | `URLField()` |
| `references:Model` | `ForeignKey(Model)` |

---

## Project Structure

After `djx new myblog && djx scaffold Post title:string content:text`:

```
myblog/
├── manage.py
├── README.md
├── myblog/
│   ├── settings.py
│   └── urls.py
└── posts/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── migrations/
    └── templates/
        └── posts/
            ├── post_list.html
            ├── post_detail.html
            ├── post_form.html
            └── post_confirm_delete.html
```

---

## Conventions

DJX follows these conventions so you don't have to think about them:

- App name is the **pluralized, lowercased** model name (`Post` → `posts`)
- Templates follow `app/model_action.html` pattern
- URLs follow RESTful patterns (`/posts/`, `/posts/new/`, `/posts/1/edit/`)
- All models get `created_at` and `updated_at` automatically
- Apps are auto-added to `INSTALLED_APPS`
- URLs are auto-wired to the project `urls.py`

---

## Contributing

Contributions are welcome! DJX is early-stage and there's a lot to build.

```bash
git clone https://github.com/RedsonNgwira/djx-cli.git
cd djx-cli
pip install -e .
djx --help
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for contributions:
- `djx console` — Django shell with all models auto-imported
- `djx generate api` — DRF REST API scaffold
- `djx server` — runserver with better defaults
- `djx db migrate` — shortcut for makemigrations + migrate
- Windows compatibility improvements
- More field types

---

## License

MIT — see [LICENSE](LICENSE).

---

Built with ❤️ from Malawi 🇲🇼 by [Redson Ngwira](https://github.com/RedsonNgwira)
