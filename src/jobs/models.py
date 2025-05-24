from django.db import models

from jobs.enum_type import JobStatusEnum


class JobPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary_range = models.JSONField()
    company_name = models.CharField(max_length=255)
    posting_date = models.DateField()
    expiration_date = models.DateField()
    required_skills = models.JSONField(default=list)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in JobStatusEnum],
    )

    def __str__(self):
        return f"{self.title} @ {self.company_name}"
