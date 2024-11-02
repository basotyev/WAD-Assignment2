from django.urls import path
from . import views

urlpatterns = [
    # Function-based views
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/new/', views.create_post, name='create_post'),
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup, name='signup'),  # Signup page

    # Class-based views
    path('class/posts/', views.PostListView.as_view(), name='post_list_class'),
    path('class/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_class'),
]
