from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_category_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(
                to='posts.Category',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='posts',
                verbose_name='دسته‌بندی',
                null=True,
                blank=True,
            ),
        ),
    ]