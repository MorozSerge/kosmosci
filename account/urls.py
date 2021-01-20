
from django.urls import path
from.views import *

app_name = 'account'
urlpatterns = [

    path('', profile, name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('logout/', sign_out, name='logout'),
    path('newsUpdate', updateNewsSources, name='newsUpdate'),
    path('ideasUpdate', updateIdeaSources, name='ideasUpdate'),
]
