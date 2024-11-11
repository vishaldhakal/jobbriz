from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from job.models import SlugMixin

class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    USER_TYPE_CHOICES = [
        ('Employer', 'Employer'),
        ('Job Seeker', 'Job Seeker'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,default='Male')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
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

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Certification(models.Model):
    name = models.CharField(max_length=50)
    issuing_organisation = models.CharField(max_length=50)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    COURSE_OR_QUALIFICATION_CHOICES = [
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

    course_or_qualification = models.CharField(max_length=50, choices=COURSE_OR_QUALIFICATION_CHOICES)
    institution = models.CharField(max_length=50)
    year_of_completion = models.DateField(blank=True, null=True)
    course_highlights = models.TextField(blank=True)

    def __str__(self):
        return self.course_or_qualification
    
    class Meta:
        ordering = ['-year_of_completion']
    

class Location(SlugMixin, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

class JobSeeker(models.Model):
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

    AVAILABILITY_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    skill_levels = models.CharField(max_length=200, choices=LEVEL_CHOICES, default="None")
    education = models.ManyToManyField(Education, blank=True)
    preferred_unit_groups = models.ManyToManyField('job.UnitGroup', blank=True)
    work_experience = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, blank=True,related_name='job_seeker_skills')
    preferred_locations = models.ManyToManyField(Location, blank=True)
    preferred_salary_range_from = models.IntegerField(default=0)
    preferred_salary_range_to = models.IntegerField(default=0)
    remote_work_preference = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES,default='Full Time')
    certifications = models.ManyToManyField(Certification, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    
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

class CareerHistory(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.job_title

class Industry(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'

class Company(models.Model):
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
    slug = models.SlugField(max_length=255, unique=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES)
    registration_number = models.CharField(max_length=50, unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = models.FileField(upload_to='company_logos/', null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    company_email = models.EmailField()
    company_registration_certificate = models.FileField(upload_to='company_registration_certificates/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['company_name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            # Check if slug exists and generate a unique one
            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
