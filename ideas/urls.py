
from django.urls import path
from.views import *

app_name = 'ideas'
urlpatterns = [
    path('', ideas, name='ideas'),
    path('made_by/<str:pk>', others_ideas, name='others_ideas'),
    path('<str:pk>/edit', edit_idea, name='edit_idea'),
    path('<str:pk>/delete', delete_idea, name='delete_idea'),
]
