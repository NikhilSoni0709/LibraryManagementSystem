import requests


def request_book(book_name, from_time, to_time, headers):
    book_data = {
        "book_name": book_name,
        "ask_from_time": from_time,
        "ask_to_time": to_time
    }
    response = requests.post(f"http://0.0.0.0:9773/user/borrow", json=book_data, headers=headers)

    if not response:
        print(response.json())

    return response

def add_book(name, category, count, headers):
    book_dict = {
        "name": name,
        "category": category,
        "count": count
    }

    response = requests.post(f"http://0.0.0.0:9773/admin/book", json=book_dict, headers=headers)

    if not response:
        print(response.json())

    return response

def add_user(name, email, category, password, headers):
    user_dict = {
        "name": name,
        "category": category,
        "password": password,
        "email": email
    }

    response = requests.post(f"http://0.0.0.0:9773/admin/user", json=user_dict, headers=headers)
    return response


def get_all_books_for_user(headers, user_name=''):
    response = requests.get(f"http://0.0.0.0:9773/admin/book-requests/{user_name}", headers=headers)
    return response

def update_borrow_request(borrow_id, action, headers):
    response = requests.patch(f"http://0.0.0.0:9773/admin/book-requests/", json={"borrow_id": borrow_id, "action": action}, headers=headers)
    return response

def return_book_with_id(book_id, headers):
    response = requests.patch(f"http://0.0.0.0:9773/admin/return", json={"book_id": book_id}, headers=headers)
    return response
