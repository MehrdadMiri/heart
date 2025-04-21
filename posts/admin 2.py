from django.contrib import admin
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ("title", "category", "created_at", "video_url")
    list_filter         = ("category", "created_at")
    search_fields       = ("title", "body_md")
    prepopulated_fields = {"slug": ("title",)}
    ordering            = ("-created_at",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields       = ("name",)