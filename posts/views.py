from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category
import markdown

def post_list(request):
    qs = Post.objects.all()
    return _render_page(request, qs, "مقالات قلب سالم")

def post_search(request):
    q = request.GET.get("q", "").strip()
    qs = Post.objects.filter(
        Q(title__icontains=q) | Q(body_md__icontains=q)
    )
    return _render_page(request, qs, f'نتایج جستجو: "{q}"', extra_ctx={"q": q})

def category_posts(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    qs = cat.posts.all()
    return _render_page(request, qs, cat.name, extra_ctx={"category": cat})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    html_body = markdown.markdown(post.body_md, extensions=["fenced_code"])
    return render(request, "post_detail.html", {"post": post, "html_body": html_body})

def _render_page(request, queryset, heading, extra_ctx=None):
    paginator = Paginator(queryset, 9)
    page_num  = request.GET.get("page", 1)
    page_obj  = paginator.get_page(page_num)

    ctx = {"page": page_obj, "heading": heading}
    if extra_ctx:
        ctx.update(extra_ctx)

    template = "partials/post_cards.html" if request.htmx else "listing.html"
    return render(request, template, ctx)