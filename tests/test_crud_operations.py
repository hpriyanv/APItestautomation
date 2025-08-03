import requests
from uuid import uuid4
from utils.logger import log_request_response

# ---------------------------
# TC_CRUD_001: Create Resource - JSONPlaceholder
# ---------------------------
def test_create_resource_jsonplaceholder(config):
    url = config['jsonplaceholder_url'] + "/posts"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Post Title",
        "body": "This is a test post body content for automation testing",
        "userId": 1
    }

    resp = requests.post(url, json=data, headers=headers)
    log_request_response(resp.request, resp)

    assert resp.status_code == 201
    response_data = resp.json()
    for key in data:
        assert response_data[key] == data[key]

# ---------------------------
# TC_CRUD_002: Create User - GoRest (Requires Token)
# ---------------------------
def test_create_user_gorest(config):
    url = config['gorest_url'] + "/users"
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "John Doe Automation",
        "email": f"user+{uuid4().hex[:8]}@example.com",
        "gender": "male",
        "status": "active"
    }

    resp = requests.post(url, json=data, headers=headers)
    log_request_response(resp.request, resp)

    print(resp.status_code, resp.text)
    assert resp.status_code == 201

    response_data = resp.json()
    for key in data:
        assert response_data[key] == data[key]

# ---------------------------
# TC_CRUD_003: Read Single Resource - JSONPlaceholder
# ---------------------------
def test_read_single_resource_jsonplaceholder(config):
    url = config['jsonplaceholder_url'] + "/posts/1"
    headers = {
        "Content-Type": "application/json"
    }

    expected_response = {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": (
            "quia et suscipit\n"
            "suscipit recusandae consequuntur expedita et cum\n"
            "reprehenderit molestiae ut ut quas totam\n"
            "nostrum rerum est autem sunt rem eveniet architecto"
        )
    }

    resp = requests.get(url, headers=headers)
    log_request_response(resp.request, resp)

    assert resp.status_code == 200
    response_data = resp.json()
    for key in expected_response:
        assert response_data[key] == expected_response[key]
