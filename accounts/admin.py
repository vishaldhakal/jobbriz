from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import (
    User, JobSeeker, Location, JobSeekerPreferences,
    Industry, Company, SkillLevel
)
from django.utils.text import slugify

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
    list_display = ('user', 'education', 'work_experience', 'get_skills')
    list_filter = ('education', 'skill_levels')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    filter_horizontal = ('skill_levels', 'preferred_unit_groups')
    readonly_fields = ('slug',)
    
    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skill_levels.all()])
    get_skills.short_description = 'Skills'

@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('slug',)

@admin.register(JobSeekerPreferences)
class JobSeekerPreferencesAdmin(ModelAdmin):
    list_display = ('job_seeker', 'preferred_salary_range_from', 'preferred_salary_range_to', 'remote_work_preference')
    list_filter = ('remote_work_preference',)
    search_fields = ('job_seeker__user__username',)
    filter_horizontal = ('preferred_locations',)

@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

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

@admin.register(SkillLevel)
class SkillLevelAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
