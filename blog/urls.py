from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView,
    BlogUpdateView, BlogDeleteView, like_post,      # ← добавили
    dislike_post, MyPostsView
)

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
# Новые пути для лайков и дизлайков
    path('<int:pk>/like/', like_post, name='like'),
    path('<int:pk>/dislike/', dislike_post, name='dislike'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
]