
import requests

response = requests.post("http://0.0.0.0:9773/login", data={"username": "nikhil", "password": "nikhil123"})

print(response.status_code)
if response:
    access_token = response.json()["access_token"]

    response = requests.get("http://0.0.0.0:9773/health", headers={"Authorization": f"Bearer {access_token}"})

    print(response.status_code)
