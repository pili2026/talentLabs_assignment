import uuid

from django.db import models

from job.schema.job import JobResponse

from .enum_type import JobStatusEnum


class JobDBModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    salary_range = models.JSONField(default=dict)
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

    def to_service_model(self) -> JobResponse:
        return JobResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            location=self.location,
            salary_range=self.salary_range,
            company_name=self.company_name,
            posting_date=self.posting_date,
            expiration_date=self.expiration_date,
            required_skills=self.required_skills,
            status=JobStatusEnum(self.status),
        )

    class Meta:
        db_table = "job_post"
