import requests
from utils.logger import log_request_response
#TC_ERROR_001: Resource Not Found- JSONPlaceholde
def test_resource_no_found_jsonplaceholder(config):
    url = config['jsonplaceholder_url'] + "/9999"
    data =  {"name": "John Doe Automation"}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=data,headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code ==404
    assert(resp.json()) == {}

#TC_ERROR_002: Method Not Allowed- HTTPBin
def test_method_not_allowed_httpbin(config):
    url = config['httpbin_url'] + "/get"
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    resp = requests.delete(url, headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code ==405

#TC_ERROR_003: Invalid URL Path- JSONPlaceholder
def test_invalid_url_jsonplaceholder(config):
    url = config['jsonplaceholder_url'] + "/invalid"
    data =  {"name": "John Doe Automation"}
    headers = {
        "Authorization": f"Bearer {config['gorest_token']}",
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=data,headers=headers)
    log_request_response(resp.request, resp)
    print(resp.status_code, resp.text)  # Debug output
    assert resp.status_code ==404
    assert resp.json() == {}
