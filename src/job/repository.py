from typing import Type
from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models.manager import Manager

from job.exception import NotFoundError
from job.schema import JobCreate, JobResponse, JobUpdate

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

    async def get_all(self) -> list[JobResponse]:
        job_list: list[JobDBModel] = await sync_to_async(list)(self.objects.all())
        return [job.to_service_model() for job in job_list]

    async def update(self, job_id: UUID, update_job: JobUpdate) -> JobResponse:
        job: JobDBModel = await self._get_or_raise(job_id)

        for field, value in update_job.model_dump().items():
            setattr(job, field, value)

        await job.asave()
        return job.to_service_model()

    async def delete(self, job_id: UUID) -> bool:
        deleted_count, _ = await self.objects.filter(id=job_id).adelete()
        return deleted_count > 0

    async def _get_or_raise(self, job_id: UUID) -> JobDBModel:
        job = await sync_to_async(lambda: self.objects.filter(id=job_id).first())()
        if job is None:
            raise NotFoundError(f"Job with id {job_id} not found")
        return job
