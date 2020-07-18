from django.urls import path

from user_profile.api.views import (
    api_detail_user_view,
    api_update_user_view,
    api_delete_user_view,
    api_create_user_view,
    obtain_auth_token,
)
from blog.api.views import (
    api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view,
)

app_name = 'blog'

urlpatterns = [
    # blog
    path('<int:id>/', api_detail_blog_view, name='detail'),
    path('<int:id>/update/', api_update_blog_view, name='update'),
    path('<int:id>/delete/', api_delete_blog_view, name='delete'),
    path('create/', api_create_blog_view, name='create'),

    # User register
    path('<int:id>/', api_detail_user_view, name='detail'),
    path('<int:id>/update/', api_update_user_view, name='update'),
    path('<int:id>/delete/', api_delete_user_view, name='delete'),
    path('create/', api_create_user_view, name='create'),

    # User login
    path('login/', obtain_auth_token, name='login'),
]
