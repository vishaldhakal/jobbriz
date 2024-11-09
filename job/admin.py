from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    MajorGroup, 
    SubMajorGroup, 
    MinorGroup, 
    UnitGroup, 
    JobPost, 
    JobApplication, 
    SavedJob
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
    list_display = ('title', 'company', 'unit_group', 'employment_type', 
                   'required_skill_level', 'is_active', 'posted_date', 'deadline')
    list_filter = ('is_active', 'employment_type', 'required_skill_level', 
                  'required_education', 'company')
    search_fields = ('title', 'company__company_name', 'description')
    readonly_fields = ('slug', 'posted_date')
    autocomplete_fields = ['company', 'unit_group', 'location']
    date_hierarchy = 'posted_date'
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'company', 'title', 'slug', 'unit_group', 
                'description', 'posted_date'
            )
        }),
        ('Requirements', {
            'fields': (
                'required_skill_level', 'required_education', 
                'responsibilities', 'requirements'
            )
        }),
        ('Compensation & Location', {
            'fields': ('salary_range_min', 'salary_range_max', 'location')
        }),
        ('Job Details', {
            'fields': ('employment_type', 'is_active', 'deadline')
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ('job', 'applicant', 'applied_date', 'updated_at')
    list_filter = ('applied_date', 'job__company')
    search_fields = (
        'job__title', 
        'applicant__user__username', 
        'applicant__user__email'
    )
    date_hierarchy = 'applied_date'
    readonly_fields = ('applied_date', 'updated_at')
    autocomplete_fields = ['job', 'applicant']
    
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
