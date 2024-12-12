import requests
import sys

book_dict = {
    "name": sys.argv[1],
    "category": "Novel",
    "count": int(sys.argv[2])
}

response = requests.post(f"http://0.0.0.0:9773/librarian/book", json=book_dict)

if not response:
    print(response.json())