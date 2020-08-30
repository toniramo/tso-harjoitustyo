from flask import render_template, redirect, request, session, abort
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
        if users.register(username, password, first_name, last_name):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden käyttäjän luominen ei onnistunut. Syynä tähän voi olla varattu käyttäjänimi.")

@app.route("/usermanagement/", methods=["GET"])
def usermanagement():
    if "user_id" not in session:
        return redirect("/")
    if session["role"] != "admin":
        return render_template("error.html", message="Sinulla ei ole oikeuksia tälle sivulle.")
    return render_template("usermanagement.html", users=users.get_all_users())
        

@app.route("/usermanagement/user<int:id>", methods=["GET","POST"])
def modifyuser(id):
    if "user_id" not in session:
        return redirect("/")
    if session["role"] != "admin":
        return render_template("error.html", message="Sinulla ei ole oikeuksia tälle sivulle.")
    roles = users.get_roles()
    if request.method == "GET":
        user = users.get_user(id)
        return render_template("modifyuser.html", user=user, roles=roles)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if users.update_user(request.form):
            user = users.get_user(id)
            return render_template("modifyuser.html", user=user, roles=roles, message="Käyttäjätiedot päivitetty onnistuneesti!")
        else:
            return render_template("error.html", message="Käyttäjätietojen päivitys epäonnistui.")

@app.route("/courses")
def courses_index():
    if "user_id" not in session:
        return redirect("/")
    courses_of_user = courses.get_courses_of_user()
    return render_template("courses/index.html", courses_of_user=courses_of_user)


@app.route("/courses/course<int:id>")
def course(id):
    if "user_id" not in session:
        return redirect("/")
    course = courses.get_course(id)
    enrolled = courses.user_enrolled(session["user_id"],id)
    participants = courses.get_participants_of_course(id)
    chapters = course_contents.get_course_chapters(id)
    exercise_results = course_contents.get_course_result_summary(id)
    return render_template("courses/course.html",
                           course=course,
                           enrolled = enrolled,
                           participants=participants,
                           chapters=chapters,
                           exercise_results=exercise_results)

@app.route("/courses/search")
def course_search():
    if "user_id" not in session:
        return redirect("/")
    return render_template("courses/search.html",
                           include_enrolled=True,
                           order_by="name")


@app.route("/courses/search/result", methods=["GET"])
def course_search_result():
    if "user_id" not in session:
        return redirect("/")
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
    if "user_id" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if courses.enroll_course(id):
        return redirect("/courses/course"+str(id))
    else:
        return render_template("error.html", message="Virhe liityttäessä kurssille. Oletko jo kurssilla?")


@app.route("/courses/new", methods=["GET", "POST"])
def new_course():
    if "user_id" not in session:
        return redirect("/")
    if session["role"] not in ["teacher", "admin"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia lisätä kurssia.")
    if request.method == "GET":
        return render_template("/courses/new.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        description = request.form["description"]
        id = courses.new_course(name, description)
        if id != None:
            return redirect("/courses/course"+str(id))
        else:
            return render_template("error.html", message="Virhe luotaessa kurssia. Käytäthän uniikkia kurssinimeä?")


@app.route("/courses/course<int:id>/chapters/new", methods=["GET", "POST"])
def new_chapter(id):
    if "user_id" not in session:
        return redirect("/")
    if session["role"] not in ["teacher", "admin"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä.")
    if session["role"] == "teacher" and not courses.user_enrolled(session["user_id"],id):
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä ennen kuin olet ilmottautunut kurssille.")
    chapter_count = len(course_contents.get_course_chapters(id))
    print("toimii")
    if request.method == "GET":
        return render_template("/courses/chapters/new.html", course_id=id, chapter_count=chapter_count)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
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
    if "user_id" not in session:
        return redirect("/")
    chapter = course_contents.get_chapter(course_id, chapter_id)
    if chapter == None:
        return render_template("error.html", message="Lukua ei löydy kyseessä olevan kurssin alta")
    enrolled = courses.user_enrolled(session["user_id"],course_id)
    if session["role"] == "student" and not enrolled:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tarkastella kurssin sisältöä ennen kuin olet ilmoittautunut kurssille.")
    exercises = course_contents.get_chapter_exercises(chapter_id)
    return render_template("/courses/chapters/chapter.html", chapter=chapter, chapter_id=chapter_id, course_id=course_id, exercises=exercises, enrolled=enrolled)


@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>/modify", methods=["GET", "POST"])
def modify_chapter(course_id, chapter_id):
    if "user_id" not in session:
        return redirect("/")
    if session["role"] not in ["teacher", "admin"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä.")
    if session["role"] == "teacher" and not courses.user_enrolled(session["user_id"],course_id):
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä ennen kuin olet ilmottautunut kurssille.")
    if request.method == "GET":
        chapter = course_contents.get_chapter(course_id, chapter_id)
        if chapter == None:
            return render_template("error.html", message="Lukua ei löydy kyseessä olevan kurssin alta.")
        return render_template("/courses/chapters/modify.html", course_id=course_id, chapter_id=chapter_id, chapter=chapter)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if course_contents.update_chapter(request.form):
            return redirect("/courses/course"+str(course_id)+"/chapters/chapter"+str(chapter_id))
        else:
            return render_template("error.html", message="Jokin meni pieleen muokatessa lukua. :(")

@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>/exercises/new", methods=["GET", "POST"])
def new_exercise(course_id, chapter_id):
    if "user_id" not in session:
        return redirect("/")
    if session["role"] not in ["teacher", "admin"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä.")
    if session["role"] == "teacher" and not courses.user_enrolled(session["user_id"],course_id):
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä ennen kuin olet ilmottautunut kurssille.")
    if course_contents.get_chapter(course_id, chapter_id) == None:
        return render_template("error.html", message="Lukua ei löydy kurssin alta. Teethän tehtävän olemassa olevan kurssin ja luvun alle.")
    exercise_count = len(course_contents.get_chapter_exercises(chapter_id))
    if request.method == "GET":
        return render_template("/courses/exercises/new_initial.html", course_id=course_id, chapter_id=chapter_id, choices=4, exercise_count=exercise_count)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if request.form["button"] == "Päivitä vaihtoehtojen määrä":
            choices = int(request.form["choices"])
            return render_template("/courses/exercises/new_updated.html", course_id=course_id, chapter_id=chapter_id, choices=choices, exercise_count=exercise_count, form=request.form)
        if request.form["button"] == "Luo tehtävä":
            exercise_id = course_contents.add_exercise(request.form)
            if exercise_id != None:
                session["message"] = "Tehtävä luotu onnistuneesti! Voit nyt katsella tehtävää opiskelijan näkökulmasta."
                return redirect("/courses/course"+str(course_id)+"/chapters/chapter"+str(chapter_id)+"/exercises/exercise"+str(exercise_id))
            else:
                return render_template("error.html", message="Jokin meni pieleen luodessa tehtävää. :(")

@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>/exercises/exercise<int:exercise_id>", methods=["GET","POST"])
def exercise(course_id, chapter_id, exercise_id):
    if "user_id" not in session:
        return redirect("/")
    chapter = course_contents.get_chapter(course_id, chapter_id)
    exercise = course_contents.get_exercise(course_id, chapter_id, exercise_id)
    if chapter == None or exercise == None:
        return render_template("error.html", message="Lukua tai tehtävää ei löydy kurssin alta.")
    enrolled = courses.user_enrolled(session["user_id"],course_id)
    if session["role"] == "student" and not enrolled:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tarkastella kurssin sisältöä ennen kuin olet ilmoittautunut kurssille.")
    choices = course_contents.get_exercise_choises(exercise_id)
    answer = course_contents.get_answer_of_current_user(exercise_id)
    if "message" in session:
        message = session["message"]
        del session["message"]
    else:
        message = None
    if request.method == "GET":
        return render_template("/courses/exercises/exercise.html",course_id=course_id, chapter_id=chapter_id, exercise_id=exercise_id, chapter=chapter, exercise=exercise, choices=choices, answer=answer, message=message, enrolled=enrolled)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if session["role"] in ["teacher","admin"]:
            return render_template("/courses/exercises/exercise.html",course_id=course_id, chapter_id=chapter_id, exercise_id=exercise_id, chapter=chapter, exercise=exercise, choices=choices, answer=request.form["choice"], enrolled=enrolled)
        if course_contents.add_answer(exercise_id, choice_id):
            return redirect("/courses/course"+str(course_id)+"/chapters/chapter"+str(chapter_id)+"/exercises/exercise"+str(exercise_id))
        else:
            return render_template("error.html", message="Jokin meni pieleen vastatessa tehtävään. :(")

@app.route("/courses/course<int:course_id>/chapters/chapter<int:chapter_id>/exercises/exercise<int:exercise_id>/modify", methods=["GET","POST"])
def modify_exercise(course_id, chapter_id, exercise_id):
    if session["role"] not in ["teacher", "admin"]:
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä.")
    if session["role"] == "teacher" and not courses.user_enrolled(session["user_id"],course_id):
        return render_template("error.html", message="Sinulla ei ole oikeuksia muokata kurssin sisältöä ennen kuin olet ilmottautunut kurssille.")
    if course_contents.get_chapter(course_id, chapter_id) == None:
        return render_template("error.html", message="Lukua ei löydy kurssin alta. Teethän tehtävän olemassa olevan kurssin ja luvun alle.")
    exercise = course_contents.get_exercise(course_id, chapter_id, exercise_id)
    choices = course_contents.get_exercise_choises(exercise_id)
    if request.method == "GET":
        if exercise != None:
            return render_template("courses/exercises/modify.html", exercise=exercise, choices=choices, course_id=course_id, chapter_id=chapter_id, exercise_id=exercise_id)
        else:
            return render_template("error.html", message="Tehtävää ei löydy kurssin luvun alta.")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        parameters = request.form
        if course_contents.update_exercise_and_choices(parameters, choices):
            session["message"] = "Tehtävän päivitys onnistui!"
            return redirect("/courses/course"+str(course_id)+"/chapters/chapter"+str(chapter_id)+"/exercises/exercise"+str(exercise_id))
        else:
            return render_template("error.html", message="Jokin meni pieleen päivitettäessä tehtävää.")