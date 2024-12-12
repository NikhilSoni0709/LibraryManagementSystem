import requests
import sys

user_dict = {
    "name": sys.argv[1],
    "category": "User",
    "password": sys.argv[3],
    "email": sys.argv[2]
}

response = requests.post(f"http://0.0.0.0:9773/admin/user", json=user_dict)

if not response:
    print(response.json())
