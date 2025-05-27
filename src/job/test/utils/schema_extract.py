from job.schema.job import JobUpdate


def extract_job_update_fields(job_response) -> dict:
    valid_fields = JobUpdate.model_fields.keys()
    return job_response.model_dump(include=valid_fields, mode="json")
