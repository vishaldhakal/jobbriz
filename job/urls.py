from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    # ISCO Classification URLs
    path('major-groups/', views.MajorGroupListCreateView.as_view(), name='major-group-list'),
    path('major-groups/<slug:slug>/', views.MajorGroupDetailView.as_view(), name='major-group-detail'),
    
    # Job Posts
    path('jobs/', views.JobPostListCreateView.as_view(), name='job-list'),
    path('jobs/<slug:slug>/', views.JobPostDetailView.as_view(), name='job-detail'),
    
    # Job Applications
    path('jobs/<int:job_id>/apply/', views.JobApplicationListCreateView.as_view(), name='job-apply'),
    path('my-applications/', views.JobApplicationListCreateView.as_view(), name='my-applications'),
    
    # Saved Jobs
    path('jobs/<int:job_id>/save/', views.SavedJobListCreateView.as_view(), name='save-job'),
    path('my-saved-jobs/', views.SavedJobListCreateView.as_view(), name='my-saved-jobs'),
] 