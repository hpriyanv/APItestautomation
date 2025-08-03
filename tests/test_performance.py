import requests
import time
import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------------------
# TC_PERF_001: Response Time Validation - JSONPlaceholder
# -------------------------------
@pytest.mark.parametrize("endpoint, method, expected_time", [
    ("/posts", "GET", 1.0),
    ("/posts/1", "GET", 0.5),
    ("/posts", "POST", 1.0)
])
def test_response_time_validation_jsonplaceholder(config, endpoint, method, expected_time):
    url = config['jsonplaceholder_url'] + endpoint
    payload = {"title": "foo", "body": "bar", "userId": 1}

    start_time = time.time()

    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=payload)
    else:
        pytest.fail(f"Unsupported method {method}")

    duration = time.time() - start_time
    print(f"\n{method} {url} - Time taken: {duration:.3f} sec")

    assert response.status_code in (200, 201)
    assert duration < expected_time, f"{method} {url} took too long: {duration:.3f}s"


# -------------------------------
# TC_PERF_002: Concurrent Request Handling - HTTPBin
# -------------------------------
CONCURRENCY = 10
MAX_TIME_PER_REQUEST = 2.0  # per-thread timeout
EXPECTED_TOTAL_TIME = 1.5   # total time for all concurrent requests

def fetch_url(url):
    start = time.time()
    resp = requests.get(url, timeout=MAX_TIME_PER_REQUEST)
    elapsed = time.time() - start
    return resp.status_code, elapsed

def test_concurrent_request_handling_httpbin(config):
    url = config['httpbin_url'] + "/delay/1"  # stable delayed endpoint
    start_all = time.time()

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(fetch_url, url) for _ in range(CONCURRENCY)]
        results = [f.result() for f in as_completed(futures)]

    total_elapsed = time.time() - start_all
    print(f"\nTotal time for {CONCURRENCY} concurrent requests: {total_elapsed:.2f}s")

    assert total_elapsed < EXPECTED_TOTAL_TIME, "Concurrency failed to reduce total response time"
    for i, (status, elapsed) in enumerate(results):
        print(f"Request {i+1}: Status {status} in {elapsed:.2f}s")
        assert status == 200
        assert elapsed < MAX_TIME_PER_REQUEST


# -------------------------------
# TC_PERF_003: Pagination Performance - JSONPlaceholder
# -------------------------------
PAGES = [1, 2, 5]
LIMIT = 20
MAX_EXPECTED_TIME = 1.0  # seconds

@pytest.mark.parametrize("page", PAGES)
def test_pagination_performance_jsonplaceholder(page, config):
    url = f"{config['jsonplaceholder_url']}/posts?_page={page}&_limit={LIMIT}"

    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start

    print(f"\nGET {url} -> {response.status_code} in {elapsed:.3f}s")

    assert response.status_code == 200, f"Page {page} failed"
    assert elapsed < MAX_EXPECTED_TIME, f"Page {page} took too long: {elapsed:.2f}s"

    data = response.json()
    assert isinstance(data, list), "Data not in expected format"
    assert len(data) <= LIMIT, "More records than expected"

    if 'Link' in response.headers:
        print("Link Header Found:", response.headers['Link'])
        assert 'rel="next"' in response.headers['Link']

#TC_PERF_004: Stress Test- HTTPBin Echo
import json  # REQUIRED for json.dumps()

# -------------------------------
# TC_PERF_004: Stress Test - HTTPBin Echo
# -------------------------------
TOTAL_REQUESTS = 50
DURATION = 30  # seconds
INTERVAL = DURATION / TOTAL_REQUESTS

payload = {"data": "x" * 1024}  # ~1KB
headers = {"Content-Type": "application/json"}


def send_request(url):
    start = time.time()
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=5)
        elapsed = time.time() - start
        return response.status_code, elapsed
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def test_stress_httpbin(config):
    results = []
    url = config['httpbin_url'] + "/post"
    print(f"Starting {TOTAL_REQUESTS} requests over {DURATION} seconds...")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _ in range(TOTAL_REQUESTS):
            futures.append(executor.submit(send_request, url))
            time.sleep(INTERVAL)

        for f in as_completed(futures):
            status, elapsed = f.result()
            results.append((status, elapsed))

    total_time = time.time() - start_time
    success_responses = [r for r in results if r[0] == 200]
    failed_responses = [r for r in results if r[0] != 200 or r[0] is None]
    response_times = [r[1] for r in success_responses if r[1] is not None]

    print(f"\nTotal time taken: {total_time:.2f}s")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Success: {len(success_responses)}")
    print(f"Failures: {len(failed_responses)}")
    print(f"Success rate: {(len(success_responses) / TOTAL_REQUESTS) * 100:.2f}%")
    if response_times:
        print(f"Average response time: {sum(response_times) / len(response_times):.3f}s")

    # ✅ Assertions
    assert len(success_responses) / TOTAL_REQUESTS >= 0.95, "Success rate below 95%"
    assert all(rt < 2 for rt in response_times), "Some response times exceeded threshold"
