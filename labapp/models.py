from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    dark_mode = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='labapp_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='labapp_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=[
        ('blood', 'Blood Test'),
        ('urine', 'Urine Test'),
        ('imaging', 'Imaging'),
        ('other', 'Other'),
    ])
    preparation_instructions = models.TextField(blank=True)
    report_format = models.TextField(blank=True, help_text="JSON schema for report format")

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    previous_booking = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.status})"

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='report')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    results = models.JSONField(default=dict, help_text="Test results in JSON format")
    pdf_file = models.FileField(upload_to='reports/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviewed_reports'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Report: {self.user.username} - {self.service.name}"

class TestResult(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='test_results')
    parameter = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    reference_range = models.CharField(max_length=100)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.parameter}: {self.value} {self.unit}"