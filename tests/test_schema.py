import os
import json
import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def test_schema_validation(config):
    # Arrange
    user_id = 8046612
    url = f"{config['gorest_url']}/users/{user_id}"
    headers = {"Authorization": f"Bearer {config['gorest_token']}",  "Content-Type": "application/json"}

    # Act
    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200, f"Unexpected status code: {resp.status_code}"

    # Load schema from relative path
    schema_path = os.path.abspath(os.path.join(os.getcwd(), "schemas/user_schema.json"))
    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Assert
    try:
        validate(instance=resp.json(), schema=schema)
        print("✅ Schema validation passed.")
    except ValidationError as ve:
        print("❌ Schema validation failed:")
        print(ve.message)
        assert False, f"Schema validation failed: {ve.message}"
