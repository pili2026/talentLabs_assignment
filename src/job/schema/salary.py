from ninja import Schema
from pydantic import ConfigDict, field_validator


class SalaryRange(Schema):
    model_config = ConfigDict(populate_by_name=True)

    min: int | None = None
    max: int | None = None

    @field_validator("max")
    @classmethod
    def validate_min_max(cls, max_val, info):
        min_val = info.data.get("min")
        if min_val is not None and max_val is not None and min_val > max_val:
            raise ValueError("min cannot be greater than max")
        return max_val
