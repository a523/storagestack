from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path('users', views.Users.as_view(), name='users_list'),
    # path('users/<int:id>', views.Users.as_view(), name='add_user')
]
