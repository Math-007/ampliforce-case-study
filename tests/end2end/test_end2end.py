import time
from http import HTTPStatus
from typing import Generator, Any

import httpx
import pytest
from httpx import Client


@pytest.fixture(scope="session")
def http_client() -> Generator[Client, Any, None]:
    with httpx.Client(base_url="http://localhost:8000") as client:
        yield client


@pytest.mark.parametrize(
    "file_path, x, expected_results",
    [
        ("provided_example.txt", 3, [23456789, 12345678, 33333333]),
        ("example_10_000.txt", 1, [10_000]),
        ("example_100_000.txt", 1, [10_0000]),
        ("example_1_000_000.txt", 1, [1_000_000]),
        ("example_1_000_000.txt", 10_000, [i for i in range(1_000_000 - 10_000 + 1, 1_000_000 + 1)]),
    ],
    ids=[
        "provided_example",
        "10k_with_1_limit",
        "100k_with_1_limit",
        "1M_with_1_limit",
        "1M_with_10_000_limit",
    ],
)
def test_create_and_query_file(file_path: str, x: int, expected_results: list[int], http_client: Client) -> None:
    with open(f"test_set/{file_path}", "rb") as file:
        files = {"file": (file_path, file, "text/plain")}  # (filename, file object, MIME type)

        create_file_response = http_client.post("/api/v1/files", files=files)

    assert create_file_response.status_code == HTTPStatus.CREATED
    file_id = create_file_response.json()["id"]

    completed = False
    while not completed:
        file_indexing_status_response = http_client.get(f"/api/v1/files/{file_id}")
        assert file_indexing_status_response.status_code == HTTPStatus.OK
        completed = file_indexing_status_response.json()["status"] == "SUCCESS"
        time.sleep(0.50)

    time.sleep(0.10)
    query_response = http_client.get(f"/api/v1/query/{file_id}", params={"limit": x})
    assert query_response.status_code == HTTPStatus.OK
    assert set(query_response.json()["ids"]) == set(expected_results)
