from main import app
from flask import render_template


@app.route("/")
def view_home():
    return render_template("main.html")


@app.route("/login")
def view_login():
    return render_template("login.html")


@app.route("/register")
def view_register():
    return render_template("register.html")


@app.route("/reset_password")
def view_reset_password():
    return render_template("reset_password.html")


@app.route("/history")
def view_history():
    return render_template("history.html")
