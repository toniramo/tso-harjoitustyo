from flask import render_template, redirect, request
from app import app
import users, courses

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

@app.route("/courses")
def courses_index():
    courses_of_user = courses.get_courses_of_user()
    return render_template("courses/index.html", courses_of_user=courses_of_user)


@app.route("/courses/course<int:id>")
def course(id):
    course = courses.get_course(id)
    participants = courses.get_participants_of_course(id)
    return render_template("courses/course.html", course=course, participants=participants)

@app.route("/courses/search")
def course_search():
    return render_template("courses/search.html")

@app.route("/courses/search/result", methods=["GET"])
def course_search_result():
    search_string = request.args["search_string"]
    teacher = request.args["teacher"]
    include_enrolled = bool(request.args.get("include_enrolled"))
    searched_courses = courses.get_searched_courses(search_string,teacher,include_enrolled)
    return render_template("/courses/result.html", searched_courses=searched_courses)

@app.route("/courses/enroll/course<int:id>", methods=["POST"])
def enroll_course(id):
    if (courses.enroll_course(id)):
        return redirect("/courses/course"+str(id))
    else:
        return render_template("error.html",message="Virhe liityttäessä kurssille. Oletko jo kurssilla?")

@app.route("/courses/new", methods=["GET","POST"])
def new_course():
    if request.method == "GET":
        return render_template("/courses/new.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        id = courses.new_course(name,description)
        if id != None:
            return redirect("/courses/course"+str(id))
        else:
            return render_template("error.html", message="Virhe luotaessa kurssia. Käytäthän uniikkia kurssinimeä?")

