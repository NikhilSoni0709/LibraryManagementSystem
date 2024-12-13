
import requests
from test_functions import *

response = requests.post("http://0.0.0.0:9773/login", data={"username": "admin", "password": "admin@123"})

print(response.status_code)
if response:
    access_token = response.json()["access_token"]
    headers={"Authorization": f"Bearer {access_token}"}

    while True:
        option = int(input(f"Choose:\n1 for add_user\n \
                           2: add_book\n \
                           3: request book\n \
                           4: all books for user\n \
                           5: all books\n \
                           6: approve borrow\n \
                           7: deny borrow\n"))

        if option == 1:
            response = add_user("vishal", "vsoni@gmail.com", "user", "vishal123", headers)
            print(response.status_code)
        elif option == 2:
            response = add_book("HarryPotter", "Magic", 10, headers)
            print(response.status_code)
        elif option == 3:
            response = request_book("HarryPotter", "2024-01-01 00:00:00", "2024-01-01 10:00:00", headers)
            print(response.status_code)
        elif option == 4:
            response = get_all_books_for_user(headers, user_name="admin")
            print(response.json())
        elif option == 5:
            response = get_all_books_for_user(headers)
            print(response.json())
        elif option == 6:
            response = update_borrow_request(1,"APPROVE",headers)
        elif option == 7:
            response = update_borrow_request(1,"DENY",headers)
        else:
            break
        


