from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile

'''
from django.http import JsonResponse
from django.core import serializers


def index(request):
    users = User.objects.all().select_related('profile')
    print(list(users.values()))
    # print(users[0].profile.gender)
    # return render(request, 'index.html', locals())

    return JsonResponse({'result': list(users.values())})

    user_json = serializers.serialize('json', users)
    return HttpResponse(user_json, content_type='application/json')
'''

from rest_framework import viewsets
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer