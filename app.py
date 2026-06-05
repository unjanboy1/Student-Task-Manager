import sqlite3
from flask import Flask, render_template, request, redirect, session

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
            (username, password),
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
            (username, password),
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


# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=?", (session["user_id"],)
    )
    tasks = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html", tasks=tasks, username=session["username"]
    )


# Add Task
@app.route("/add-task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, title) VALUES (?, ?)",
        (session["user_id"], title),
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# Delete Task
@app.route("/delete-task/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# Complete Task
@app.route("/complete-task/<int:task_id>")
def complete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# Edit Task Page
@app.route("/edit-task/<int:task_id>")
def edit_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    return render_template("edit_task.html", task=task)


# Update Task Action
@app.route("/update-task/<int:task_id>", methods=["POST"])
def update_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=? WHERE id=?", (title, task_id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)