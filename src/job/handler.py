from uuid import UUID

from ninja import Router
from ninja.errors import HttpError

from .repository import JobRepository
from .schema import JobCreate, JobResponse, JobUpdate
from .service import JobService

job_router = Router()
job_service = JobService(JobRepository())


@job_router.post("/", response=JobResponse, summary="Create a new job")
async def create_job(request, payload: JobCreate):
    return await job_service.create_job(payload)


@job_router.get("/", response=list[JobResponse], summary="List all jobs")
async def list_job(request):
    return await job_service.get_all_job()


@job_router.get("/{job_id}", response=JobResponse, summary="Get job by ID")
async def get_job(request, job_id: UUID):
    job = await job_service.get_job(job_id)
    if not job:
        raise HttpError(404, f"Job {job_id} not found")
    return job


@job_router.put("/{job_id}", response=JobResponse, summary="Update job by ID")
async def update_job(request, job_id: UUID, payload: JobUpdate):
    updated = await job_service.update_job(job_id, payload)
    if not updated:
        raise HttpError(404, f"Job {job_id} not found")
    return updated


@job_router.delete("/{job_id}", response={204: None}, summary="Delete job by ID")
async def delete_job(request, job_id: UUID):
    success = await job_service.delete_job(job_id)
    if not success:
        raise HttpError(404, f"Job {job_id} not found")
    return 204, None
