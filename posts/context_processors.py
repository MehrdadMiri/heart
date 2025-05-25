from django.db.models import Prefetch, F, Value, CharField
from django.db.models.functions import Replace, Lower
from .models import Category, Post

def categories(request):
    """Inject categories and their posts ordered alphabetically."""
    normalized_posts = Post.objects.annotate(
        norm_title=Lower(
            Replace(
                Replace(
                    Replace(F("title"), Value("آ"), Value("ا"), output_field=CharField()),
                    Value("أ"), Value("ا"), output_field=CharField(),
                ),
                Value("إ"), Value("ا"), output_field=CharField(),
            )
        )
    ).order_by("norm_title")

    qs = Category.objects.prefetch_related(
        Prefetch("posts", queryset=normalized_posts)
    )

    return {
        "all_categories": qs
    }
