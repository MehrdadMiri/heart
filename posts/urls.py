from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("search/", views.post_search, name="post_search"),
    path("category/<str:slug>/", views.category_posts, name="category_posts"),
    path("<str:slug>/like/", views.like_post, name="like_post"),
    path("<str:slug>/comment/", views.add_comment, name="add_comment"),
    path("<str:slug>/", views.post_detail, name="post_detail"),
]
