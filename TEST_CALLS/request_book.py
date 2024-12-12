import requests
import sys

from datetime import datetime

pattern = "%Y-%m-%d %H:%M:%S"
book_data = {
    "book_id": "1",
    "from_time": "2024-10-10 00:00:00",
    "to_time": "2024-10-10 10:00:00"
}

response = requests.post(f"http://0.0.0.0:9773/{sys.argv[1]}/borrow", json=book_data)

if not response:
    print(response.json())