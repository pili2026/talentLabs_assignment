from uuid import UUID

from asgiref.sync import async_to_sync
from ninja import Query, Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from .schema.job import JobCreate, JobListQuery, JobResponse, JobUpdate, PaginationResult
from .service import JobService

job_router = Router(auth=JWTAuth(), tags=["Job Management"])


@job_router.get("/skill_list", response=list[str], summary="Get all unique skill")
def list_all_skill(request):
    job_service: JobService = request.job_service
    return async_to_sync(job_service.get_all_skill)()


@job_router.post("/", response=JobResponse, summary="Create a new job")
def create_job(request, create_job_schema: JobCreate):
    job_service: JobService = request.job_service
    return async_to_sync(job_service.create_job)(create_job_schema)


@job_router.get("/", response=PaginationResult, summary="List all job")
def list_job(request, query: JobListQuery = Query(...)):
    job_service: JobService = request.job_service
    return async_to_sync(job_service.get_all_job)(query)


@job_router.get("/{job_id}", response=JobResponse, summary="Get job by ID")
def get_job(request, job_id: UUID):
    job_service: JobService = request.job_service
    return async_to_sync(job_service.get_job)(job_id)


@job_router.put("/{job_id}", response=JobResponse, summary="Update job by ID")
def update_job(request, job_id: UUID, update_job_schema: JobUpdate):
    job_service: JobService = request.job_service
    return async_to_sync(job_service.update_job)(job_id, update_job_schema)


@job_router.delete("/{job_id}", response={204: None}, summary="Delete job by ID")
def delete_job(request, job_id: UUID):
    job_service: JobService = request.job_service
    result = async_to_sync(job_service.delete_job)(job_id)
    if not result:
        raise HttpError(404, f"Job {job_id} not found")
    return 204, None
