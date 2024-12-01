from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="API documentation for the Blog app",
      contact=openapi.Contact(email="basotyev@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)


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

    # DRF
    path('api/posts/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('api/comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('api/comments/<int:pk>/', views.CommentDetailAPIView.as_view(), name='comment-detail'),
    path('api/categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('api/categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
