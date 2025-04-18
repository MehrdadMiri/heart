from django.db import migrations


def create_embed_post(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    # Unique slug for embedded video post
    slug = 'embedded-video-post'
    if not Post.objects.filter(slug=slug).exists():
        Post.objects.create(
            title='Embedded Video Post',
            slug=slug,
            body_md='<div id="12229598786"><script type="text/JavaScript" src="https://www.aparat.com/embed/3yghr?data[rnddiv]=12229598786&data[responsive]=yes"></script></div>',
            category=None,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_make_category_nullable'),
    ]

    operations = [
        migrations.RunPython(create_embed_post),
    ]