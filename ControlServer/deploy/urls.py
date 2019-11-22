from django.urls import path
from . import views

app_name = 'deploy'

urlpatterns = [
    path('node/', views.Nodes.as_view())
]
