import requests
from utils.logger import log_request_response

# TC_VALID_001: Missing Required Fields
def test_missing_required_fields_gorest(config):
    url = config['gorest_url'] + "/users"
    data = {"name": "John Doe Automation"}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }

    expected_values = {
        "email": "can't be blank",
        "gender": "can't be blank, can be male of female",
        "status": "can't be blank"
    }

    resp = requests.post(url, json=data, headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)
    assert resp.status_code == 422

    response_data = resp.json()
    for error in response_data:
        field = error.get("field")
        message = error.get("message")
        if field in expected_values:
            assert message == expected_values[field], \
                f"Expected '{expected_values[field]}' for '{field}', got '{message}'"

# TC_VALID_002: Invalid Email Format
def test_invalid_email_format_gorest(config):
    url = config['gorest_url'] + "/users"
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "John Doe Automation",
        "email": "invalid_format",
        "gender": "male",
        "status": "active"
    }

    expected_error = {
        "field": "email",
        "message": "is invalid"
    }

    resp = requests.post(url, json=data, headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)
    assert resp.status_code == 422

    response_data = resp.json()
    matched = any(
        err.get("field") == expected_error["field"] and err.get("message") == expected_error["message"]
        for err in response_data
    )
    assert matched, f"Expected validation error for {expected_error} not found."

# TC_VALID_003: Invalid Enum Values
def test_invalid_enum_values_gorest(config):
    url = config['gorest_url'] + "/users"
    data = {
        "name": "John Doe Automation",
        "email": "haripriyanv@gmail.com",
        "gender": "unknown",   # Invalid
        "status": "maybe"      # Invalid
    }
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }

    expected_errors = {
        "gender": "can't be blank, can be male of female",
        "status": "can't be blank"
    }

    resp = requests.post(url, json=data, headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)
    assert resp.status_code == 422

    response_data = resp.json()
    for error in response_data:
        field = error.get("field")
        message = error.get("message")
        if field in expected_errors:
            assert message == expected_errors[field], \
                f"Expected '{expected_errors[field]}' for '{field}', got '{message}'"
