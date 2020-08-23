from flask import render_template, redirect, request
from app import app
import users
import courses
import course_contents


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Kirjautuminen epäonnistui. Tarkista, että käytät oikeaa tunnusta ja salasanaa.")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        # TODO check that fields are not empty
        if users.register(username, password, first_name, last_name):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden käyttäjän luominen ei onnistunut. Syynä tähän voi olla varattu käyttäjänimi.")


@app.route("/courses")
def courses_index():
    courses_of_user = courses.get_courses_of_user()
    return render_template("courses/index.html", courses_of_user=courses_of_user)


@app.route("/courses/course<int:id>")
def course(id):
    course = courses.get_course(id)
    participants = courses.get_participants_of_course(id)
    chapters = course_contents.get_course_chapters(id)
    return render_template("courses/course.html",
                           course=course,
                           participants=participants,
                           chapters=chapters)


@app.route("/courses/search")
def course_search():
    return render_template("courses/search.html",
                           include_enrolled=True,
                           order_by="name")


@app.route("/courses/search/result", methods=["GET"])
def course_search_result():
    search_string = request.args["search_string"]
    teacher = request.args["teacher"]
    include_enrolled = bool(request.args.get("include_enrolled"))
    order_by = request.args.get("order_by")
    if order_by == "":
        order_by = "name"
    searched_courses = courses.get_searched_courses(
        search_string,
        teacher,
        include_enrolled, order_by)
    return render_template("/courses/result.html",
                           searched_courses=searched_courses,
                           search_string=search_string,
                           teacher=teacher,
                           include_enrolled=include_enrolled,
                           order_by=order_by)


@app.route("/courses/enroll/course<int:id>", methods=["POST"])
def enroll_course(id):
    if courses.enroll_course(id):
        return redirect("/courses/course"+str(id))
    else:
        return render_template("error.html", message="Virhe liityttäessä kurssille. Oletko jo kurssilla?")


@app.route("/courses/new", methods=["GET", "POST"])
def new_course():
    if request.method == "GET":
        return render_template("/courses/new.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        # TODO check fields are not empty
        id = courses.new_course(name, description)
        if id != None:
            return redirect("/courses/course"+str(id))
        else:
            return render_template("error.html", message="Virhe luotaessa kurssia. Käytäthän uniikkia kurssinimeä?")


@app.route("/courses/course<int:id>/chapters/new", methods=["GET", "POST"])
def new_chapter(id):
    chapter_count = len(course_contents.get_course_chapters(id))
    if request.method == "GET":
        return render_template("/courses/chapters/new.html", course_id=id, chapter_count=chapter_count)
    if request.method == "POST":
        print(request.form)
        ordinal = request.form["ordinal"]
        name = request.form["name"]
        content = request.form["content"]
        chapter_id = course_contents.add_chapter(ordinal, name, content, id)
        if chapter_id != None:
            return redirect("/courses/course"+str(id)+"/chapters/chapter"+str(chapter_id))
        else:
            return render_template("error.html", message="Jokin meni pieleen lisättäessä lukua. :(")


@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>")
def chapter(course_id, chapter_id):
    chapter = course_contents.get_chapter(chapter_id)
    # TODO check if user has enrolled
    return render_template("/courses/chapters/chapter.html", chapter=chapter, chapter_id=chapter_id, course_id=course_id)


@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>/modify", methods=["GET", "POST"])
def modify_chapter(course_id, chapter_id):
    if request.method == "GET":
        chapter = course_contents.get_chapter(chapter_id)
        return render_template("/courses/chapters/modify.html", course_id=course_id, chapter_id=chapter_id, chapter=chapter)
    if request.method == "POST":
        parameters = request.form
        if course_contents.update_chapter(parameters):
            return redirect("/courses/course"+str(course_id)+"/chapters/chapter"+str(chapter_id))
        else:
            return render_template("error.html", message="Jokin meni pieleen muokatessa lukua. :(")
