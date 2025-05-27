from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F, Value, CharField, TextField
from django.db.models.functions import Replace, Lower
from django.db import IntegrityError
from django.http import JsonResponse
import markdown

from .models import Post, Category, Comment, PostLike
from .forms import CommentForm


def post_list(request):
    qs = Post.objects.all()
    return _render_page(request, qs, "آخرین پست‌ها")


def post_search(request):
    q = request.GET.get("q", "").strip()
    norm_q = q.replace('آ', 'ا').replace('أ', 'ا').replace('إ', 'ا').lower()
    qs = Post.objects.annotate(
        norm_title=Lower(
            Replace(
                Replace(
                    Replace(F('title'), Value('آ'), Value('ا'), output_field=CharField()),
                    Value('أ'), Value('ا'), output_field=CharField()),
                Value('إ'), Value('ا'), output_field=CharField()
            ),
            output_field=CharField(),
        ),
        norm_body=Lower(
            Replace(
                Replace(
                    Replace(F('body_md'), Value('آ'), Value('ا'), output_field=TextField()),
                    Value('أ'), Value('ا'), output_field=TextField()),
                Value('إ'), Value('ا'), output_field=TextField()
            ),
            output_field=TextField(),
        ),
    ).filter(
        Q(norm_title__icontains=norm_q) | Q(norm_body__icontains=norm_q)
    )
    return _render_page(request, qs, f'نتایج جستجو: "{q}"', extra_ctx={"q": q})


def category_posts(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    qs = cat.posts.all()
    return _render_page(request, qs, cat.name, extra_ctx={"category": cat})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    html_body = markdown.markdown(post.body_md, extensions=["fenced_code"])
    comments = post.comments.filter(approved=True)
    form = CommentForm()
    return render(request, "post_detail.html", {"post": post, "html_body": html_body, "comments": comments, "form": form})


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return redirect(post.get_absolute_url())


def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.session.session_key:
        request.session.save()
    try:
        PostLike.objects.create(post=post, session_key=request.session.session_key)
    except IntegrityError:
        pass
    return JsonResponse({"likes": post.likes.count()})


def _render_page(request, queryset, heading, extra_ctx=None):
    paginator = Paginator(queryset, 9)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    ctx = {"page": page_obj, "heading": heading}
    if extra_ctx:
        ctx.update(extra_ctx)

    template = "partials/post_cards.html" if request.htmx else "listing.html"
    return render(request, template, ctx)
