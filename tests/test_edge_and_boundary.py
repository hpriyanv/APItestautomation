import requests
from utils.logger import log_request_response
from uuid import uuid4

#TC_EDGE_001: Empty Request Body
def test_empty_request_body_gorest(config):
    url = config['gorest_url'] + "/users"
    data =  {}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    expected_values = {
        "email": "can't be blank",
        "gender": "can't be blank, can be male of female",
        "status": "can't be blank"
    }
    resp = requests.post(url, json=data,headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code == 422
    response_data = resp.json()
    for error in response_data:
        field = error.get("field")
        message = error.get("message")
        if field in expected_values:
            assert message == expected_values[field], \
                f"Expected '{expected_values[field]}' for '{field}', got '{message}'"

#TC_EDGE_002: Maximum String Lengths
def test_maximum_string_length_gorest(config):
    url = config['gorest_url'] + "/users"
    data =  {"name": "John Doe Automation John Doe Automation John Doe Automation John Doe Automation",
 "email": f"user+{uuid4().hex[:8]}@example.com",
 "gender": "male",
 "status": "active"}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=data,headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code == 201


#TC_EDGE_003: Unicode and Special Characters
def test_unicode_special_char_gorest(config):
    url = config['gorest_url'] + "/users"
    data =  { "name": "José María González-Pérez £$%^",
 "email": f"user+{uuid4().hex[:8]}@example.com",
 "gender": "male",
 "status": "active"}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=data,headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code == 201