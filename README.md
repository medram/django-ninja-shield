# Django Ninja Shield

A powerful and flexible permissions control package for Django Ninja. This package allows you to easily manage and combine permissions for your Django Ninja API endpoints using a clean and intuitive syntax.

## Features

- 🛡️ Simple permission decorators for Django Ninja endpoints
- ⚡ Combine permissions using logical operations (AND, OR, NOT)
- 🔒 Built on top of Django's permission system
- 🚀 Type-safe with full typing support

## Installation

You can install the package using pip:

```bash
pip install django-ninja-shield
```

Or if you're using Poetry:

```bash
poetry add django-ninja-shield
```

## Basic Usage

Here's a simple example of how to use django-ninja-shield:

```python
from django_ninja_shield import requires_permissions
from ninja import Router

router = Router()

@router.get("/articles")
@requires_permissions("articles.view_article")
def get_articles(request):
    return {"message": "You have permission to view articles"}
```

## Advanced Usage

### Combining Permissions

You can combine multiple permissions using logical operators:

```python
from django_ninja_shield import requires_permissions, P

router = Router()

# Using AND operator
@router.post("/articles")
@requires_permissions(P("articles.add_article") & P("articles.change_article"))
def create_article(request):
    return {"message": "You have permission to create articles"}

# Using OR operator
@router.get("/dashboard")
@requires_permissions(P("admin.view_dashboard") | P("staff.view_dashboard"))
def view_dashboard(request):
    return {"message": "You have permission to view the dashboard"}

# Using NOT operator
@router.get("/public")
@requires_permissions(~P("articles.is_restricted"))
def public_view(request):
    return {"message": "This is a public view"}
```

### Complex Permission Combinations

You can create complex permission rules by combining multiple operations:

```python
from django_ninja_shield import requires_permissions, P, IsAdmin, IsUseruser, IsStaff, IsActive

@router.put("/articles/{article_id}")
@requires_permissions(
    (P("articles.change_article") & P("articles.view_article")) |
    IsAdmin() # or: IsStaff(), IsSuperuser, IsActive
)
def update_article(request, article_id: int):
    return {"message": f"Article {article_id} updated"}
```

## Response Format

When permission is denied, the API returns a 403 Forbidden response with the following format:

```json
{
  "detail": "Permission denied"
}
```

## Requirements

- Python ≥ 3.10
- Django ≥ 4.0.0

## License

This project is licensed under the MIT License.
