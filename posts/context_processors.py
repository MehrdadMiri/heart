from .models import Category

def categories(request):
    """
    Injects all Category objects into every template context
    under the name 'all_categories'.
    """
    return {
        "all_categories": Category.objects.all()
    }