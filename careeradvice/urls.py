from django.urls import path
from . import views

urlpatterns = [
    path('career-paths/', views.CareerPathListView.as_view(), name='career-paths'),
    path('career-tools/', views.CareerToolListView.as_view(), name='career-tools'),
]