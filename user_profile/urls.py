from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from user_profile.views import (
    TestAuthView
    )

urlpatterns = [
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.   
    path('test_auth/', TestAuthView.as_view(), name='test_auth'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]