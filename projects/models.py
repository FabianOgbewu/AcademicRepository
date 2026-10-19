from django.db import models
from django.contrib.auth.models import User

class ProjectSubmission(models.Model):
    # 1. Dropdown choices for Category and Status
    CATEGORY_CHOICES = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('BUS', 'Business'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REVISION', 'Revision Required'),
    ]

    # 2. Database Columns
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    abstract = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    supervisor_feedback = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    # 3. Securely link the project to a specific User (Student)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
