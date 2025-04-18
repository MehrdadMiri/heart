import os

from django.core.management.base import BaseCommand
from django.conf import settings

from posts.models import Category, Post


class Command(BaseCommand):
    help = 'Load sample posts into the database from the samples directory.'

    def handle(self, *args, **options):
        # Map sample subdirectories to Category names
        mapping = {
            'diseases': 'بیماری',
            'meds': 'دارو',
        }
        sample_root = os.path.join(settings.BASE_DIR, 'samples')
        for subdir, cat_name in mapping.items():
            # Ensure category exists
            cat, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category '{cat_name}'"))
            dir_path = os.path.join(sample_root, subdir)
            if not os.path.isdir(dir_path):
                self.stdout.write(self.style.ERROR(f"Directory not found: {dir_path}"))
                continue
            # Process each file in the sample directory
            for filename in sorted(os.listdir(dir_path)):
                file_path = os.path.join(dir_path, filename)
                if not os.path.isfile(file_path):
                    continue
                # Derive post title from filename
                title = filename.replace('_', ' ')
                # Read markdown content
                try:
                    with open(file_path, encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to read {file_path}: {e}"))
                    continue
                # Remove leading title heading if present (first line matches title)
                lines = content.splitlines()
                if lines:
                    first = lines[0].lstrip('# ').strip()
                    if first == title:
                        content = '\n'.join(lines[1:]).lstrip('\n')
                # Create or update the Post
                post, p_created = Post.objects.get_or_create(
                    title=title,
                    defaults={'body_md': content, 'category': cat},
                )
                if p_created:
                    self.stdout.write(self.style.SUCCESS(f"Created post '{title}'"))
                else:
                    updated = False
                    if post.body_md != content:
                        post.body_md = content
                        updated = True
                    if post.category != cat:
                        post.category = cat
                        updated = True
                    if updated:
                        post.save()
                        self.stdout.write(self.style.WARNING(f"Updated post '{title}'"))
        self.stdout.write(self.style.SUCCESS("Sample loading completed."))