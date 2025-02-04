import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

user_headers_map = {}

@app.route("/userPage/{user_name}")
def userPage(user_name):
    return render_template('UserPage.html', user_name=user_name)

@app.route('/', methods=['GET', 'POST'])
def rootPage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post("http://0.0.0.0:9773/login", data={"username": username, "password": password})

        print(response.status_code)
        if response:
            access_token = response.json()["access_token"]
            user = response.json()["user"]
            headers={"Authorization": f"Bearer {access_token}"}
            user_headers_map[username] = headers

            if user["category"] == "admin":
                return redirect("/adminPage")
            else:
                response = requests.get(f"http://0.0.0.0:9773/user/books/{username}", headers=user_headers_map[username])
                print(response.json())
                return render_template('UserPage.html', username=username, allBooks=response.json())
        
    return render_template('loginPage.html')



@app.route('/adminPage', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        book_name = request.form['book_name']
        author_name = request.form['author_name']
        category = request.form['category']
        stock = int(request.form['stock'])
        
        book_dict = {
            "name": book_name,
            "author_name": author_name,
            "category": category,
            "count": stock
        }

        response = requests.post(f"http://0.0.0.0:9773/admin/book", json=book_dict, headers=user_headers_map['admin'])
        print(response)

        return redirect('/adminPage')

    response = requests.get(f"http://0.0.0.0:9773/admin/book", headers=user_headers_map['admin'])
    print(response)
    return render_template('AdminPage.html', allBooks=response.json())

@app.route('/delete/<book_name>')
def delete(book_name):
    response = requests.delete(f"http://0.0.0.0:9773/admin/book/{book_name}", headers=user_headers_map['admin'])
    print(response.json())
    return redirect("/adminPage")

if __name__ == "__main__":
    app.run(debug=True, port=8000)