from app.config.vast.vast_config import HEADERS
import json
import requests


base_url = "https://console.vast.ai/api/v0/"

def get_machine_by_id(machine_id):
    payload = {
        "machine_id": {"eq": machine_id},
    }


    json_payload = json.dumps(payload)

    api_url = f"https://console.vast.ai/api/v0/bundles/"


    print(api_url)
    response = requests.post(api_url, headers=HEADERS, data=json_payload)


    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    # Attempt to parse JSON
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        return None
