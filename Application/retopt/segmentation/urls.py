from django.urls import path, include
from . import views

app_name = 'segmentation'
urlpatterns = [
    path('', views.segmentation_view, name="clustering"),
]
