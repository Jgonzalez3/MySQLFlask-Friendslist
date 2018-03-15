from flask import Flask, redirect, render_template, request, session
from mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = "sdfsagdd"
mysql = MySQLConnection(app, 'fullfriend')
@app.route("/")
def index():
    query = "SELECT name, age, date_format(created_at, '%M %D'), date_format(created_at, '%Y') FROM friends"
    friends = mysql.query_db(query)
    return render_template("full_friends.html", all_friends=friends)

@app.route("/friends/<friend_id>")
def show(friend_id):
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {"specific_id": friend_id}
    friends = mysql.query_db(query, data)
    return render_template("full_friends.html", one_friend=friends[0])

@app.route("/friends", methods=["POST"])
def create():
    query = "INSERT INTO friends (name, age, created_at) VALUES (:name, :age, NOW())"
    data = {
        "name": request.form['name'],
        "age": request.form['age']
    }
    mysql.query_db(query, data)
    return redirect("/")

app.run(debug=True)