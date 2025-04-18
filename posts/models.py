from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("نام دسته‌بندی", max_length=50, unique=True)
    slug = models.SlugField("شناسه یکتا", max_length=50, unique=True, editable=False)

    class Meta:
        ordering = ["name"]
        verbose_name        = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            # تولید خودکار slug از نام فارسی (allow_unicode=True)
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("عنوان", max_length=150)
    slug = models.SlugField(unique=True, editable=False)
    body_md = models.TextField("متن (Markdown)")
    video_url = models.URLField("آدرس ویدیو", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        verbose_name="دسته‌بندی",
        on_delete=models.PROTECT,
        related_name="posts",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پُست"
        verbose_name_plural = "پُست‌ها"

    # auto‑generate slug once
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])

    def __str__(self):
        return self.title



