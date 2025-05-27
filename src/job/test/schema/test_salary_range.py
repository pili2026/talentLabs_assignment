import pytest
from pydantic import ValidationError

from job.schema.salary import SalaryRange


def test_salary_range_valid_case():
    salary = SalaryRange(min=100000, max=150000)
    assert salary.min == 100000
    assert salary.max == 150000


def test_salary_range_min_greater_than_max_raises():
    with pytest.raises(ValidationError) as exc_info:
        SalaryRange(min=150000, max=100000)

    errors = exc_info.value.errors()
    assert any("min cannot be greater than max" in err["msg"] for err in errors)
