from django.urls import path, include
from . import views

app_name = 'segmentation'
urlpatterns = [
    path('segmentation/', views.segmentation_view, name="clustering"),
    path('', views.dashboard_view, name="dashboard"),
    path('generate_dataframe/', views.generate_dataframe, name='generate_dataframe'),
    path('dataframe/', views.generate_recommendation_dataframe, name='generate_dataframe'),
    path('segment_customer/', views.segment_customer, name='SegmentCustomer')
]

