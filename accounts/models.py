from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from job.models import SlugMixin

class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    USER_TYPE_CHOICES = [
        ('Employer', 'Employer'),
        ('Job Seeker', 'Job Seeker'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add related_name to fix clash with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to.')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.')
    )


class JobSeeker(models.Model):
    EDUCATION_CHOICES = [
        ('General Literate', 'General Literate'),
        ('Below SLC', 'Below SLC'),
        ('+2', '+2'),
        ('Bachelors', 'Bachelors'),
        ('Master & above', 'Master & above'),
        ('Pre-Diploma', 'Pre-Diploma'),
        ('Diploma', 'Diploma'),
        ('TLSC', 'TLSC'),
        ('No Education', 'No Education'),
    ]

    LEVEL_CHOICES = [
        ('RPL', 'RPL'),
        ('Level 1', 'Level 1'),
        ('Level 2', 'Level 2'),
        ('Level 3', 'Level 3'),
        ('Level 4', 'Level 4'),
        ('Level 5', 'Level 5'),
        ('Level 6', 'Level 6'),
        ('Level 7', 'Level 7'),
        ('Level 8', 'Level 8'),
        ('None', 'None'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/')
    skill_levels = models.ManyToManyField('SkillLevel')
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    preferred_unit_groups = models.ManyToManyField('job.UnitGroup')
    work_experience = models.PositiveIntegerField(default=0)
    certifications = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def __str__(self):
        return f"Job Seeker - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while JobSeeker.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Location(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

class JobSeekerPreferences(models.Model):
    job_seeker = models.OneToOneField(JobSeeker, on_delete=models.CASCADE)
    preferred_locations = models.ManyToManyField(Location, related_name='job_seeker_preferences')
    preferred_salary_range_from = models.IntegerField(default=0)
    preferred_salary_range_to = models.IntegerField(default=0)
    remote_work_preference = models.BooleanField(default=False)

class Industry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'

class Company(SlugMixin, models.Model):
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001+', '1001+ employees'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES)
    registration_number = models.CharField(max_length=50, unique=True)
    website = models.URLField(blank=True)
    description = models.TextField()
    logo = models.FileField(upload_to='company_logos/', null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    company_email = models.EmailField()
    company_registration_certificate = models.FileField(upload_to='company_registration_certificates/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['company_name']

    def __str__(self):
        return self.company_name

class SkillLevel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name