from uuid import UUID

from .repository import JobRepository
from .schema import JobCreate, JobResponse, JobUpdate


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def create_job(self, payload: JobCreate) -> JobResponse:
        job = await self.job_repository.create(payload.dict())
        return JobResponse.from_orm(job)

    async def get_job(self, job_id: UUID) -> JobResponse | None:
        job = await self.job_repository.get_by_id(job_id)
        return JobResponse.from_orm(job) if job else None

    async def get_all_job(self) -> list[JobResponse]:
        job_list = await self.job_repository.get_all()
        return [JobResponse.from_orm(job) for job in job_list]

    async def update_job(self, job_id: UUID, payload: JobUpdate) -> JobResponse | None:
        job = await self.job_repository.get_by_id(job_id)
        if not job:
            return None

        updated = await self.job_repository.update(job, payload.dict())
        return JobResponse.from_orm(updated)

    async def delete_job(self, job_id: UUID) -> bool:
        job = await self.job_repository.get_by_id(job_id)
        if not job:
            return False
        await self.job_repository.delete(job)
        return True
