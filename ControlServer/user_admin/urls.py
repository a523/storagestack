from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path('users/', views.Users.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('self/', views.UserSelf.as_view(), name='user_self')
]
