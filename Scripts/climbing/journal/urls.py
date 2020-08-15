from django.urls import path

from . import views

app_name='journal'
urlpatterns = [
    path('', views.index, name='index'),
    path('locations/', views.log_by_location, name='location_overview'),
    path('date/', views.log_by_date, name='log_by_date'),
    path('locations/<int:location_id>', views.log_by_location, name='log_by_location'),
]
