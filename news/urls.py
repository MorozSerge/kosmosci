
from django.urls import path
from.views import *

app_name = 'news'
urlpatterns = [
    path('feed/<str:pk>/', feed, name='feed'),
    path('', source_list, name='sources'),
    path('<str:pk>/news/', news_list, name='news'),
]
