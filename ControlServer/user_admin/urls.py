from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path('', views.Users.as_view(), name='users_list')
]
