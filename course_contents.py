from flask import session
from db import db
from datetime import datetime


def get_course_chapters(course_id):
    sql = "SELECT id, ordinal, name, content FROM chapters WHERE course_id=:course_id ORDER BY ordinal, name"
    result = db.session.execute(sql, {"course_id": course_id})
    return result.fetchall()


def get_chapter(chapter_id):
    sql = "SELECT ordinal, name, content FROM chapters WHERE id=:chapter_id"
    result = db.session.execute(sql, {"chapter_id": chapter_id})
    return result.fetchone()


def add_chapter(ordinal, name, content, course_id):
    try:
        sql = "INSERT INTO chapters (ordinal, name, content, course_id, creator_id, created_at) \
            VALUES (:ordinal, :name, :content, :course_id, :user_id, :created_at) \
            RETURNING id"
        result = db.session.execute(sql,
                                    {
                                        "ordinal": ordinal,
                                        "name": name,
                                        "content": content,
                                        "course_id": course_id,
                                        "user_id": str(session["user_id"]),
                                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    })
        db.session.commit()
        return result.fetchone()[0]
    except Exception as e:
        print(e)


def update_chapter(parameters):
    try:
        sql = "UPDATE chapters SET ordinal=:ordinal, name=:name, content=:content WHERE id=:chapter_id"
        db.session.execute(sql, parameters)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_chapter_exercises(chapter_id):
    sql = "SELECT id, ordinal, name, question FROM exercises WHERE chapter_id=:chapter_id ORDER BY ordinal, name"
    result = db.session.execute(sql, {"chapter_id": chapter_id})
    return result.fetchall()


def get_exercise(exercise_id):
    sql = "SELECT ordinal, name, question FROM exercises WHERE id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id": exercise_id})
    return result.fetchone()


def add_exercise(parameters):
    parameters = parameters.to_dict()
    parameters["user_id"] = str(session["user_id"])
    parameters["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO exercises (ordinal, name, question, course_id, chapter_id, creator_id, created_at) \
            VALUES (:ordinal, :name, :question, :course_id, :chapter_id, :user_id, :created_at) \
            RETURNING id"
    try:
        result = db.session.execute(sql, parameters)
        if result != None:
            parameters["exercise_id"] = result.fetchone()[0]
            add_choices(parameters)
        db.session.commit()
        return parameters["exercise_id"]
    except Exception as e:
        print(e)
        return None

def add_choices(parameters):
    sql = "INSERT INTO choices (correct, description, exercise_id, created_at) \
            VALUES (:correct, :description, :exercise_id, :created_at)"
    for choice in range(1, int(parameters["choices"])+1):
        if parameters["choice"+str(choice)] != '':
            db.session.execute(sql, {
                "correct": ("correct"+str(choice) in parameters),
                "description": parameters["choice"+str(choice)],
                "exercise_id": parameters["exercise_id"],
                "created_at": parameters["created_at"]
            })

def get_exercise_choises(exercise_id):
    sql = "SELECT id, description, correct FROM choices WHERE exercise_id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id": exercise_id})
    return result.fetchall()

def add_answer(exercise_id, choice_id):
    sql = "INSERT INTO answers (exercise_id, choice_id, user_id, answered_at) \
            VALUES (:exercise_id, :choice_id, :user_id, :answered_at)"
    try:
        db.session.execute(sql,
                           {
                               "exercise_id": exercise_id,
                               "choice_id": choice_id,
                               "user_id": str(session["user_id"]),
                               "answered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                           })
        db.session.commit()
        return True
    except Exception as e:
        return False

def get_answer_of_current_user(exercise_id):
    sql = "SELECT choice_id FROM answers WHERE exercise_id=:exercise_id AND user_id=:user_id"
    result = db.session.execute(sql,
                                {
                                    "exercise_id": exercise_id,
                                    "user_id": str(session["user_id"])
                                })
    try:
        return result.fetchone()[0]
    except:
        return None

def get_course_result_summary(course_id):
    sql = "SELECT (SELECT chapters.name FROM chapters WHERE id = exercises.chapter_id) as chapter, \
            exercises.name, \
            SUM(CASE WHEN (SELECT correct FROM choices WHERE id = answers.choice_id) THEN 1 ELSE 0 END) as correct_answers,\
            SUM(CASE WHEN (SELECT correct FROM choices WHERE id = answers.choice_id) THEN 0 ELSE 1 END) as wrong_answers, \
            COUNT(*) as total \
            FROM exercises \
            LEFT JOIN answers ON answers.exercise_id=exercises.id \
            WHERE exercises.course_id =:course_id \
            GROUP BY exercises.id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()