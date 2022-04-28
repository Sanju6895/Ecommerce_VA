"""
This file will include all functions which will be accessible anywhere in the project
This also needs to be included inside settings.py under context_processors
"""


from .models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
    }
