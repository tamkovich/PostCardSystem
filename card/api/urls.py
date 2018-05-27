from django.urls import path, re_path
from .views import UserCardRudView, UserCardAPIView

app_name = 'home'

urlpatterns = [
    path('', UserCardAPIView.as_view(), name='card-create'),
    re_path(r'^(?P<pk>\d+)/$', UserCardRudView.as_view(), name='card-rud'),
]
