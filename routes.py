from flask import render_template, redirect, request
from app import app
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html", message="Kirjautuminen epäonnistui. Tarkista, että käytät oikeaa tunnusta ja salasanaa.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        if users.register(username, password, first_name, last_name):
            return redirect("/")
        else:
            return render_template("error.html",message="Uuden käyttäjän luominen ei onnistunut. Syynä tähän voi olla varattu käyttäjänimi.")