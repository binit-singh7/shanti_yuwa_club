"""
Context processors for the main app
These functions are called for every request and add variables to the template context
"""
from django.conf import settings
from django.utils import translation


def translation_context(request):
    """
    Add translation and global context variables to all templates
    """
    context = {
        'site_name': 'Shanti Yuwa Club',
        'site_url': request.build_absolute_uri('/'),
        'current_language': translation.get_language(),
    }
    return context
