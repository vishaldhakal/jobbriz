from django.db import models
from django.utils.text import slugify

class SlugMixin:
    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        model = self.__class__
        while model.objects.filter(slug=slug).exclude(id=self.id).exists():
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
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Expired', 'Expired'),
        ('Closed', 'Closed'),
    ]
    
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
        ('All', 'All'),
    ]

    company = models.ForeignKey('accounts.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    unit_group = models.ForeignKey(UnitGroup, on_delete=models.CASCADE)
    required_skill_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='None')
    required_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='No Education')
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    show_salary = models.BooleanField(default=True)
    requirements = models.TextField(blank=True, null=True)
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.ManyToManyField('accounts.Location', related_name='job_posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Published')
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    views_count = models.PositiveIntegerField(default=0, blank=True)
    applications_count = models.PositiveIntegerField(default=0, blank=True)
    
    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('accounts.JobSeeker', on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'applicant')
    
    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only increment on creation
            self.job.applications_count = models.F('applications_count') + 1
            self.job.save()
        super().save(*args, **kwargs)

class HireRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='hire_requests')
    job_seeker = models.ForeignKey('accounts.JobSeeker', on_delete=models.CASCADE, related_name='hire_requests')
    requested_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    message = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('job', 'job_seeker')

class SavedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='saved_by')
    job_seeker = models.ForeignKey('accounts.JobSeeker', on_delete=models.CASCADE, related_name='saved_jobs')
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'job_seeker')

    def __str__(self):
        return f"Saved job {self.job.title} by {self.job_seeker.user.username}"
