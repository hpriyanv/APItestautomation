import requests

#TC_AUTH_001: Valid Authentication (ReqRes)
def test_valid_authentication_reqres(config):
    url = config['reqres_url'] + "/login"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert "token" in response_data and response_data["token"]

#TC_AUTH_002: Invalid Credentials (ReqRes)
def test_invalid_credentials_reqres(config):
        url = config['reqres_url'] + "/login"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "email": "eve.holt@reqres.in",
            "password": "!@!@"  # Invalid password
        }

        response = requests.post(url, json=data, headers=headers)
        assert response.status_code == 400

        response_data = response.json()
        assert "error" in response_data
        assert response_data["error"] == "user not found"

#TC_AUTH_003: Missing Password (ReqRes)
def test_missing_password_reqres(config):
        url = config['reqres_url'] + "/login"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "email": "eve.holt@reqres.in",
            }

        response = requests.post(url, json=data, headers=headers)
        assert response.status_code == 400

        response_data = response.json()
        assert "error" in response_data
        assert response_data["error"] == "Missing password"
