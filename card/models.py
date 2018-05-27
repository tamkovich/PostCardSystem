from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse


class UserCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default='')
    visited_date = models.DateTimeField()
    transport = models.CharField(max_length=20, default='bus')
    value = models.DecimalField(max_digits=6, decimal_places=2)
    # visited_towns =  models.ManyToManyField("self")
    
    def __str__(self):
        return str(self.city)

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-cards:card-rud", kwargs={"pk": self.pk}, request=request)
