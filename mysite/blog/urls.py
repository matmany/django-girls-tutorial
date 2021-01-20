from django.urls import include, path
from . import views

from rest_framework_nested import routers
from rest_framework import permissions
from blog.api import PostViewSet, CommentViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_router = routers.DefaultRouter()
api_router.register(r"posts", PostViewSet)

post_router = routers.NestedDefaultRouter(
    api_router, r"posts", lookup="post")

post_router.register(r"comments", CommentViewSet, 
    basename="post-comment")

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path("api/", include(api_router.urls)),
    path("api/", include(post_router.urls)),
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name="post_remove"),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]