from django.urls import path
from . import views

urlpatterns = [
    path("",                     views.post_list,      name="post_list"),
    path("search/",              views.post_search,    name="post_search"),
    # Use str converter to allow Unicode slugs (e.g., Persian characters)
    path("category/<str:slug>/", views.category_posts, name="category_posts"),
    path("<str:slug>/",         views.post_detail,    name="post_detail"),
]