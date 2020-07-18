from django.urls import path, include
from user_profile.views import (
    TestAuthView
    )

urlpatterns = [ 
    path('test_auth/', TestAuthView.as_view(), name='test_auth'),
    
    # Django_REST_framework built-in api-auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]