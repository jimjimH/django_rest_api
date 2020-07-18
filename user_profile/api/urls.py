from django.urls import path

from user_profile.api.views import (
    api_detail_user_view,
    api_update_user_view,
    api_delete_user_view,
    api_create_user_view,
    obtain_auth_token,
)

app_name = 'user_profile'

urlpatterns = [
    # User register
    path('<int:id>/', api_detail_user_view, name='detail'),
    path('<int:id>/update/', api_update_user_view, name='update'),
    path('<int:id>/delete/', api_delete_user_view, name='delete'),
    path('create/', api_create_user_view, name='create'),
    # User login
    path('login/', obtain_auth_token, name='login'),
]

# GET    /user_profile/<id>
# PUT    /user_profile/<id>/update
# DELETE /user_profile/<id>/delete
# POST   /user_profile/create/ 
