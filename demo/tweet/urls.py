from django.urls import path

from . import views


app_name = 'tweets'

urlpatterns = [
    path('', views.Tweets.as_view(), name='tweet'),
]