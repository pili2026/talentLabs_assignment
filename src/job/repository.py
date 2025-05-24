from typing import Type
from uuid import UUID

from asgiref.sync import sync_to_async
from django.db.models.manager import Manager

from .model import JobPostDBModel


class JobRepository:
    def __init__(self, model: Type[JobPostDBModel] = JobPostDBModel):
        self.db_model: Type[JobPostDBModel] = model
        self.objects: Manager[JobPostDBModel] = model.objects

    async def create(self, data: dict) -> JobPostDBModel:
        return await self.objects.acreate(**data)

    async def get_by_id(self, job_id: UUID) -> JobPostDBModel | None:
        return await sync_to_async(lambda: self.objects.filter(id=job_id).first())()

    async def get_all(self) -> list[JobPostDBModel]:
        return await sync_to_async(list)(self.objects.all())

    async def update(self, job: JobPostDBModel, data: dict) -> JobPostDBModel:
        for key, value in data.items():
            setattr(job, key, value)
        await job.asave()
        return job

    async def delete(self, job: JobPostDBModel) -> None:
        await job.adelete()
