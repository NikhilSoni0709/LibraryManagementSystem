LibrarySystem


Get-started:

    - pip install -r requirements.txt
    - change database url in src/Persistance/database.py (can be made configurable later)
    - python3.11 start_library_service.py {host} {port}


General:

    - admin user will be created by default with username as "admin" and password as "admin@123"
    - JWT authentication has been added with an expiration time of 30 mins via Middleware
    - only admins can add users and books, and approve/deny a borrow request
    - Refer LibrarySystemER for DB Schema
    - Refer test_calls.py and test_functions.py for better understanding


Endpoints:

    - POST: /login
        - data = {"username": "someuser", "password": "somepassword"}
    
    Admin:
        - POST: /admin/user
            - data = { "name": name, "category": category, "password": password, "email": email } 
            - Add new user
        - POST: /admin/book
            - book_dict = { "name": name, "category": category, "count": count }
            - Add new book
        - GET: /admin/book-requests/
            - Get all requested borrow requests
        - GET: /admin/book-requests/{user_name}
            - Get history of borrowings for given user
        - PATCH: /admin/book-requests/
            - data={"borrow_id": someId, "action": "APPROVE/DENY"}
            - Update borrow request in db   

    User:
        - POST: /user/borrow
            - data = { "book_name": book_name, "ask_from_time": datetime, "ask_to_time": datetime }
            - Add a borrow request
        - GET: /user/books
            - Get all available books
        - GET: /user/borrow
            - Get all borrow request for logged-in user


