from datetime import date, timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from job.model import JobDBModel, JobStatusEnum


class Command(BaseCommand):
    help = "Seed the database with initial user and job data"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com")
            self.stdout.write(self.style.SUCCESS("✅ Created admin user"))

        if JobDBModel.objects.count() == 0:
            base_date = date.today()
            for i in range(1, 11):
                JobDBModel.objects.create(
                    id=uuid4(),
                    title=f"Seeded Job {i}",
                    description=f"Description for Job {i}",
                    location="Taipei",
                    salary_range="70k-90k",
                    posting_date=base_date - timedelta(days=i),
                    expiration_date=base_date + timedelta(days=30),
                    required_skills=["Python", "Django"],
                    status=JobStatusEnum.ACTIVE,
                    company_name="TalentLabs Inc",
                )
            self.stdout.write(self.style.SUCCESS("✅ Seeded 10 job records"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Jobs already exist, skipping."))
