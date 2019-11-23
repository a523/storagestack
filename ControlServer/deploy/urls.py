from django.urls import path
from . import views

app_name = 'deploy'

urlpatterns = [
    path('nodes/', views.Nodes.as_view())
]
