from django.db import models
from django.utils.text import slugify

class SlugMixin:
    def generate_unique_slug(self):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Get the model class dynamically
            model = self.__class__
            while model.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        super().save(*args, **kwargs)

class MajorGroup(SlugMixin, models.Model):
    """ISCO Major Group (1-digit code)"""
    code = models.CharField(max_length=1, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.title}"

class SubMajorGroup(SlugMixin, models.Model):
    """ISCO Sub-Major Group (2-digit code)"""
    major_group = models.ForeignKey(MajorGroup, on_delete=models.CASCADE, related_name='sub_major_groups')
    code = models.CharField(max_length=2, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.title}"

class MinorGroup(SlugMixin, models.Model):
    """ISCO Minor Group (3-digit code)"""
    sub_major_group = models.ForeignKey(SubMajorGroup, on_delete=models.CASCADE, related_name='minor_groups')
    code = models.CharField(max_length=3, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.title}"

class UnitGroup(SlugMixin, models.Model):
    """ISCO Unit Group (4-digit code)"""
    minor_group = models.ForeignKey(MinorGroup, on_delete=models.CASCADE, related_name='unit_groups')
    code = models.CharField(max_length=4, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.title}"

class JobPost(SlugMixin, models.Model):
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

    EMPLOYMENT_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    unit_group = models.ForeignKey(UnitGroup, on_delete=models.CASCADE)
    required_skill_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='None')
    required_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES,default='No Education')
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ManyToManyField('accounts.Location', related_name='job_posts')
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey('accounts.JobSeeker', on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
    
    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.user.username}"
    
class SavedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey('accounts.JobSeeker', on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'job_seeker')

    def __str__(self):
        return f"Saved job {self.job.title} by {self.job_seeker.user.username}"