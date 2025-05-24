import uuid

from django.db import models

from .enum_type import JobStatusEnum


class JobPostDBModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    salary_range = models.JSONField()
    company_name = models.CharField(max_length=255)
    posting_date = models.DateField(db_index=True)
    expiration_date = models.DateField(db_index=True)
    required_skills = models.JSONField(default=list)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in JobStatusEnum],
        db_index=True,
    )

    def __str__(self):
        return f"{self.title} @ {self.company_name}"

    class Meta:
        db_table = "job_post"
