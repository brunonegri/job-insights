import csv
from functools import lru_cache
from typing import Dict, List


@lru_cache
def read(path: str) -> List[Dict]:
    with open(path, encoding="utf8") as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def get_unique_job_types(path: str) -> List[str]:
    jobs_data = read(path)
    job_types = [job["job_type"] for job in jobs_data]
    return list(set(job_types))
    raise NotImplementedError


def filter_by_job_type(jobs: List[Dict], job_type: str) -> List[Dict]:
    return [job for job in jobs if job["job_type"] == job_type]
    raise NotImplementedError
