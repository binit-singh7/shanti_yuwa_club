def translation_context(request):
    """
    Add language-related variables to the context.
    Nepali language support has been removed.
    """
    return {
        'current_language': 'en',
        'translations': {},
    }
