from job.repository import JobRepository
from job.service import JobService


class JobServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.job_service = JobService(JobRepository())
        return self.get_response(request)

    async def __acall__(self, request):
        request.job_service = JobService(JobRepository())
        return await self.get_response(request)
