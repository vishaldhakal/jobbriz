from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    # ISCO Classification URLs
    path('major-groups/', views.MajorGroupListCreateView.as_view(), name='major-group-list'),
    path('major-groups/<slug:slug>/', views.MajorGroupDetailView.as_view(), name='major-group-detail'),
    path('sub-major-groups/', views.SubMajorGroupListCreateView.as_view(), name='sub-major-group-list'),
    path('sub-major-groups/<slug:slug>/', views.SubMajorGroupDetailView.as_view(), name='sub-major-group-detail'),
    path('minor-groups/', views.MinorGroupListCreateView.as_view(), name='minor-group-list'),
    path('minor-groups/<slug:slug>/', views.MinorGroupDetailView.as_view(), name='minor-group-detail'),
    path('unit-groups/', views.UnitGroupListCreateView.as_view(), name='unit-group-list'),
    path('unit-groups/<slug:slug>/', views.UnitGroupDetailView.as_view(), name='unit-group-detail'),
    
    # Job Posts
    path('jobs/', views.JobPostListCreateView.as_view(), name='job-list'),
    path('jobs/<slug:slug>/', views.JobPostDetailView.as_view(), name='job-detail'),
    path('jobs/<slug:slug>/view/', views.JobPostViewCountView.as_view(), name='job-view'),
    path('jobs/company/<slug:company_slug>/', views.CompanyJobListView.as_view(), name='company-jobs'),
    
    # Job Applications
    path('jobs/<slug:job_slug>/apply/', views.JobApplicationCreateView.as_view(), name='job-apply'),
    path('applications/', views.JobApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/status/', views.UpdateApplicationStatusView.as_view(), name='update-application-status'),
    
    # Saved Jobs
    path('jobs/<slug:job_slug>/save/', views.SavedJobToggleView.as_view(), name='save-job-toggle'),
    path('saved-jobs/', views.SavedJobListView.as_view(), name='saved-job-list'),
] 