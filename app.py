from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Home Page
@app.route("/")
def home():
    return redirect("/login")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)