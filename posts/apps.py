from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    # def ready(self):
    #     from django.templatetags import registry  # noqa: F401  (ensures filters load)
