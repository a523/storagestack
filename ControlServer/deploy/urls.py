from django.urls import path
from . import views

app_name = 'deploy'

urlpatterns = [
    path('hello/', views.check_conn)
]
