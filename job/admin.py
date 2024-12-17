from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    MajorGroup, 
    SubMajorGroup, 
    MinorGroup, 
    UnitGroup, 
    JobPost, 
    JobApplication, 
    SavedJob,
    HireRequest,
    Apprenticeship,
    ApprenticeshipCategory
)

@admin.register(MajorGroup)
class MajorGroupAdmin(ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')
    list_filter = ('code',)
    readonly_fields = ('slug',)
    
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'slug', 'description')
        }),
    )

@admin.register(SubMajorGroup)
class SubMajorGroupAdmin(ModelAdmin):
    list_display = ('code', 'title', 'major_group')
    search_fields = ('code', 'title', 'major_group__title')
    list_filter = ('major_group',)
    readonly_fields = ('slug',)
    autocomplete_fields = ['major_group']
    
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'major_group', 'slug', 'description')
        }),
    )

@admin.register(MinorGroup)
class MinorGroupAdmin(ModelAdmin):
    list_display = ('code', 'title', 'sub_major_group')
    search_fields = ('code', 'title', 'sub_major_group__title')
    list_filter = ('sub_major_group__major_group', 'sub_major_group')
    readonly_fields = ('slug',)
    autocomplete_fields = ['sub_major_group']
    
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'sub_major_group', 'slug', 'description')
        }),
    )

@admin.register(UnitGroup)
class UnitGroupAdmin(ModelAdmin):
    list_display = ('code', 'title', 'minor_group')
    search_fields = ('code', 'title', 'minor_group__title')
    list_filter = ('minor_group__sub_major_group__major_group', 'minor_group')
    readonly_fields = ('slug',)
    autocomplete_fields = ['minor_group']
    
    fieldsets = (
        (None, {
            'fields': ('code', 'title', 'minor_group', 'slug', 'description')
        }),
    )

@admin.register(JobPost)
class JobPostAdmin(ModelAdmin):
    list_display = ('title', 'company', 'status', 'employment_type', 
                   'required_skill_level', 'posted_date', 'deadline', 'views_count', 
                   'applications_count')
    list_filter = ('status', 'employment_type', 'required_skill_level', 
                  'required_education', 'company')
    search_fields = ('title', 'company__company_name', 'description')
    readonly_fields = ('slug', 'posted_date', 'views_count', 'applications_count')
    autocomplete_fields = ['company', 'unit_group', 'location']
    date_hierarchy = 'posted_date'
    list_editable = ['status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'company', 'title', 'slug', 'unit_group', 
                'description', 'posted_date', 'status'
            )
        }),
        ('Requirements', {
            'fields': (
                'required_skill_level', 'required_education', 
                'responsibilities', 'requirements'
            )
        }),
        ('Compensation & Location', {
            'fields': (
                'show_salary', 'salary_range_min', 'salary_range_max', 
                'location'
            )
        }),
        ('Job Details', {
            'fields': ('employment_type', 'deadline')
        }),
        ('Statistics', {
            'fields': ('views_count', 'applications_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_date', 'updated_at')
    list_filter = ('status', 'applied_date', 'job__company')
    search_fields = (
        'job__title', 
        'applicant__user__username', 
        'applicant__user__email'
    )
    date_hierarchy = 'applied_date'
    readonly_fields = ('applied_date', 'updated_at')
    autocomplete_fields = ['job', 'applicant']
    list_editable = ['status']
    
    fieldsets = (
        (None, {
            'fields': ('job', 'applicant', 'status', 'cover_letter')
        }),
        ('Dates', {
            'fields': ('applied_date', 'updated_at')
        }),
    )

@admin.register(SavedJob)
class SavedJobAdmin(ModelAdmin):
    list_display = ('job', 'job_seeker', 'saved_date')
    list_filter = ('saved_date', 'job__company')
    search_fields = (
        'job__title', 
        'job_seeker__user__username', 
        'job_seeker__user__email'
    )
    date_hierarchy = 'saved_date'
    readonly_fields = ('saved_date',)
    autocomplete_fields = ['job', 'job_seeker']
    
    fieldsets = (
        (None, {
            'fields': ('job', 'job_seeker', 'saved_date')
        }),
    )

@admin.register(HireRequest)
class HireRequestAdmin(ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'requested_date')
    list_filter = ('status', 'requested_date', 'job__company')
    search_fields = (
        'job__title', 
        'job_seeker__user__username', 
        'job_seeker__user__email'
    )
    date_hierarchy = 'requested_date'
    readonly_fields = ('requested_date',)
    autocomplete_fields = ['job', 'job_seeker']
    
    fieldsets = (
        (None, {
            'fields': ('job', 'job_seeker', 'status', 'requested_date','message','seeker_message')
        }),
    )

admin.site.register(Apprenticeship,ModelAdmin)
admin.site.register(ApprenticeshipCategory,ModelAdmin)