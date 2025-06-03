from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "video_url")
    list_filter = ("category", "created_at")
    search_fields = ("title", "body_md")
    readonly_fields = ("slug",)
    ordering = ("-created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    readonly_fields = ("slug",)
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("name", "body")
    readonly_fields = ("created_at",)
