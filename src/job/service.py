from uuid import UUID

from .repository import JobRepository
from .schema import JobCreate, JobResponse, JobUpdate


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def create_job(self, create_job: JobCreate) -> JobResponse:
        created_job: JobResponse = await self.job_repository.create(create_job)
        return created_job

    async def get_job(self, job_id: UUID) -> JobResponse:
        job: JobResponse = await self.job_repository.get_by_id(job_id)
        return job

    async def get_all_job(self) -> list[JobResponse]:
        job_list: list[JobResponse] = await self.job_repository.get_all()
        return [JobResponse.from_orm(job) for job in job_list]

    async def update_job(self, job_id: UUID, update_job: JobUpdate) -> JobResponse:
        updated: JobResponse = await self.job_repository.update(job_id, update_job)
        return updated

    async def delete_job(self, job_id: UUID) -> bool:
        return await self.job_repository.delete(job_id)
