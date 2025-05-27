from typing import Type
from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models import Q
from django.db.models.manager import Manager

from job.exception import NotFoundException
from job.schema.job import JobCreate, JobListQuery, JobResponse, JobUpdate, PaginationResult, SortOrder

from .model import JobDBModel


class JobRepository:
    def __init__(self, model: Type[JobDBModel] = JobDBModel):
        self.objects: Manager[JobDBModel] = model.objects

    async def create(self, create_job: JobCreate) -> JobResponse:
        create_job_dict: dict = create_job.model_dump()
        created_job: JobDBModel = await self.objects.acreate(**create_job_dict)

        return created_job.to_service_model()

    async def get_by_id(self, job_id: UUID) -> JobResponse:
        job: JobDBModel = await self._get_or_raise(job_id)
        return job.to_service_model()

    async def get_all(self, query: JobListQuery) -> PaginationResult:
        filters = Q()

        if query.status:
            filters &= Q(status=query.status)
        if query.location:
            filters &= Q(location=query.location)
        if query.company_name:
            filters &= Q(company_name__icontains=query.company_name)
        if query.search:
            filters &= (
                Q(title__icontains=query.search)
                | Q(description__icontains=query.search)
                | Q(company_name__icontains=query.search)
            )
        if query.skills:
            skill_filters = Q()
            for skill in query.skills:
                skill_filters |= Q(required_skills__contains=[skill])
            filters &= skill_filters

        qs = self.objects.filter(filters)

        total = await sync_to_async(qs.count)()

        order_field = query.order_by.value
        if query.sort_order == SortOrder.DESC:
            order_field = f"-{order_field}"
        qs = qs.order_by(order_field)

        offset = (query.page - 1) * query.page_size
        qs = qs[offset : offset + query.page_size]

        job_list = await sync_to_async(list)(qs)

        return PaginationResult(
            total=total,
            page=query.page,
            page_size=query.page_size,
            list=[job.to_service_model() for job in job_list],
        )

    async def update(self, job_id: UUID, update_job: JobUpdate) -> JobResponse:
        job: JobDBModel = await self._get_or_raise(job_id)

        for field, value in update_job.model_dump().items():
            setattr(job, field, value)

        await job.asave()
        return job.to_service_model()

    async def delete(self, job_id: UUID) -> bool:
        deleted_count, _ = await self.objects.filter(id=job_id).adelete()
        return deleted_count > 0

    async def get_all_skill(self) -> list[str]:
        @sync_to_async
        def extract_skills():
            skills = self.objects.values_list("required_skills", flat=True)
            unique_skills = set()

            for skill_list in skills:
                if isinstance(skill_list, list):
                    unique_skills.update(skill_list)

            return sorted(unique_skills)

        return await extract_skills()

    async def _get_or_raise(self, job_id: UUID) -> JobDBModel:
        job = await sync_to_async(lambda: self.objects.filter(id=job_id).first())()
        if job is None:
            raise NotFoundException(f"Job with id {job_id} not found")
        return job
