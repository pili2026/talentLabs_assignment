import random
from datetime import date, timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from ninja_jwt.tokens import RefreshToken

from job.model import JobDBModel, JobStatusEnum


class Command(BaseCommand):
    help = "Seed the database with initial user and job data"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com")
            self.stdout.write(self.style.SUCCESS("Created admin user"))
        else:
            admin_user = User.objects.get(username="admin")
            self.stdout.write(self.style.WARNING("Admin user already exists"))

        refresh = RefreshToken.for_user(admin_user)
        access_token = str(refresh.access_token)
        self.stdout.write(self.style.NOTICE(f"Access Token:\n{access_token}"))
        self.stdout.write(self.style.NOTICE("Example curl test:"))
        self.stdout.write(
            self.style.NOTICE(f'curl -H "Authorization: Bearer {access_token}" http://localhost:8000/api/job/')
        )

        if JobDBModel.objects.count() == 0:
            job_titles = [
                "Backend Engineer",
                "Frontend Engineer",
                "DevOps Engineer",
                "Data Analyst",
                "Product Manager",
                "QA Engineer",
                "AI Researcher",
                "UX Designer",
                "Fullstack Developer",
                "Technical Writer",
            ]
            descriptions = [
                "Build and maintain RESTful APIs",
                "Develop intuitive frontend interfaces",
                "Manage CI/CD pipelines and deployment",
                "Analyze business data for insights",
                "Design and document software features",
                "Write test plans and ensure quality",
                "Research and implement machine learning models",
                "Improve user experience through design",
                "Build end-to-end web applications",
                "Create and maintain technical documentation",
            ]
            companies = [
                "TechNova Inc",
                "DevWorks",
                "DataBridge Analytics",
                "CloudOps Ltd",
                "Frontend Magic",
                "AI Lab",
                "Designify Studio",
                "CodeCraft",
                "TalentLabs Inc",
                "WriteWell Co",
            ]
            salary_ranges = ["60k-80k", "70k-90k", "80k-100k", "90k-110k", "100k-120k", "120k-150k"]
            locations = ["Taipei", "Kaohsiung", "Tainan", "Hsinchu", "Taichung", "Remote"]
            skill_pool = [
                "Python",
                "Django",
                "React",
                "SQL",
                "Docker",
                "Kubernetes",
                "Excel",
                "Figma",
                "Linux",
                "GraphQL",
            ]

            today = date.today()
            for _ in range(10):
                posting_date = today - timedelta(days=random.randint(1, 30))
                expiration_date = posting_date + timedelta(days=random.randint(10, 60))
                required_skills = random.sample(skill_pool, k=random.randint(1, 3))

                JobDBModel.objects.create(
                    id=uuid4(),
                    title=random.choice(job_titles),
                    description=random.choice(descriptions),
                    location=random.choice(locations),
                    salary_range=random.choice(salary_ranges),
                    posting_date=posting_date,
                    expiration_date=expiration_date,
                    required_skills=required_skills,
                    status=random.choice(list(JobStatusEnum)),
                    company_name=random.choice(companies),
                )

            self.stdout.write(self.style.SUCCESS("Seeded 10 job records"))
        else:
            self.stdout.write(self.style.WARNING("Jobs already exist, skipping."))
