from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import (
    User, JobSeeker, Location, Industry, Company,
    Language, Certification, Education, CareerHistory,
    Skill
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'is_staff')
    list_filter = ('user_type', 'gender', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('User Details', {'fields': ('user_type', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

@admin.register(JobSeeker)
class JobSeekerAdmin(ModelAdmin):
    list_display = ('user', 'work_experience', 'availability')
    list_filter = ('availability', 'skill_levels')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    filter_horizontal = ('education', 'certifications', 'languages', 'preferred_locations')
    readonly_fields = ('slug',)

@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    readonly_fields = ('slug',)

@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('company_name', 'industry', 'company_size', 'is_verified')
    list_filter = ('company_size', 'is_verified', 'industry')
    search_fields = ('company_name', 'registration_number', 'company_email')
    raw_id_fields = ('user', 'industry')
    readonly_fields = ('slug',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'slug', 'industry', 'company_size')
        }),
        ('Company Details', {
            'fields': ('registration_number', 'website', 'description', 'established_date')
        }),
        ('Contact Information', {
            'fields': ('company_email',)
        }),
        ('Media', {
            'fields': ('logo', 'company_registration_certificate')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
    )

@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Certification)
class CertificationAdmin(ModelAdmin):
    list_display = ('name', 'issuing_organisation', 'issue_date', 'expiry_date')
    search_fields = ('name', 'issuing_organisation')
    list_filter = ('issue_date', 'expiry_date')

@admin.register(Education)
class EducationAdmin(ModelAdmin):
    list_display = ('course_or_qualification', 'institution', 'year_of_completion')
    search_fields = ('institution',)
    list_filter = ('course_or_qualification',)

@admin.register(CareerHistory)
class CareerHistoryAdmin(ModelAdmin):
    list_display = ('job_seeker', 'company_name', 'job_title', 'start_date', 'end_date')
    search_fields = ('company_name', 'job_title')
    list_filter = ('start_date', 'end_date')

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
