# djx

Convention over configuration for Django. Rails-like scaffolding and generators.

## Installation

```bash
pip install -e .
```

## Usage

### Scaffold (Model + Views + Templates + URLs)
```bash
djx scaffold Post title:string body:text published:boolean
djx scaffold Comment post:references author:string content:text
```

### Model Only
```bash
djx model User email:email name:string age:integer
```

### Controller (Views + Templates)
```bash
djx controller Post
```

### Migration
```bash
djx migration add_index_to_posts
```

### Config Management
```bash
djx config DEBUG False
djx config ALLOWED_HOSTS '["localhost", "127.0.0.1"]'
```

### Install Packages
```bash
djx add django-crispy-forms
djx add djangorestframework
```

## Field Types

- `string` → CharField
- `text` → TextField
- `integer` → IntegerField
- `boolean` → BooleanField
- `date` → DateField
- `datetime` → DateTimeField
- `decimal` → DecimalField
- `email` → EmailField
- `url` → URLField
- `references:Model` → ForeignKey

## Example Workflow

```bash
# Create project
django-admin startproject myproject
cd myproject

# Generate scaffold
djx scaffold Article title:string content:text published:boolean

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

Visit: `http://localhost:8000/articles/`

## Architecture

**Trade-offs**:
- ✓ Faster development, less boilerplate
- ✓ Consistent structure across projects
- ✗ Less explicit than pure Django
- ✗ Opinionated URL patterns

**Conventions**:
- Auto-creates app if missing (pluralized model name)
- Auto-wires URLs to project
- Auto-adds apps to INSTALLED_APPS
- CRUD views use class-based views
- Templates follow `app/model_action.html` pattern
