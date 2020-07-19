from django.urls import path

from blog.api.views import (
    api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view,
    api_lastet_blog_view,
    api_tag_blog_view,
    api_search_blog_view,
)

app_name = 'blog'

urlpatterns = [
    # blog
    path('<int:id>/', api_detail_blog_view, name='detail'),
    path('<int:id>/update/', api_update_blog_view, name='update'),
    path('<int:id>/delete/', api_delete_blog_view, name='delete'),
    path('create/', api_create_blog_view, name='create'),
    path('latest/', api_lastet_blog_view, name='latest'),
    path('tag/<int:tag_id>/', api_tag_blog_view, name='tag'),
    path('list/', api_search_blog_view.as_view(), name='search'),
]
