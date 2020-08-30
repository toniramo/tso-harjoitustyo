from flask import session
from db import db
from datetime import datetime


def get_course_chapters(course_id):
    sql = "SELECT id, ordinal, name, content  \
           FROM chapters WHERE course_id=:course_id \
           ORDER BY ordinal, name"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()


def get_chapter(course_id, chapter_id):
    sql = "SELECT ordinal, name, content \
           FROM chapters \
           WHERE id=:chapter_id AND course_id=:course_id"
    result = db.session.execute(sql, {"chapter_id":chapter_id, "course_id":course_id})
    return result.fetchone()


def add_chapter(ordinal, name, content, course_id):
    try:
        sql = "INSERT INTO chapters (ordinal, name, content, course_id, creator_id, created_at) \
               VALUES (:ordinal, :name, :content, :course_id, :user_id, :created_at) \
               RETURNING id"
        result = db.session.execute(sql,
            {"ordinal":ordinal,
             "name":name,
             "content":content,
             "course_id":course_id,
             "user_id":str(session["user_id"]),
             "created_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        db.session.commit()
        return result.fetchone()[0]
    except:
        return None


def update_chapter(parameters):
    try:
        sql = "UPDATE chapters \
               SET ordinal=:ordinal, name=:name, content=:content \
               WHERE id=:chapter_id"
        db.session.execute(sql, parameters)
        db.session.commit()
        return True
    except:
        return False


def get_chapter_exercises(chapter_id):
    sql = "SELECT id, ordinal, name, question \
           FROM exercises \
           WHERE chapter_id=:chapter_id \
           ORDER BY ordinal, name"
    result = db.session.execute(sql, {"chapter_id":chapter_id})
    return result.fetchall()


def get_exercise(course_id, chapter_id, exercise_id):
    sql = "SELECT ordinal, name, question \
           FROM exercises \
           WHERE id=:exercise_id AND course_id=:course_id AND chapter_id=:chapter_id"
    result = db.session.execute(sql, 
        {"exercise_id":exercise_id,
         "course_id":course_id,
         "chapter_id":chapter_id})
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
    except:
        return None

def update_exercise_and_choices(parameters, choices): 
    try:
        sql = "UPDATE exercises \
               SET ordinal=:ordinal, name=:name, question=:question \
               WHERE id=:exercise_id"
        db.session.execute(sql, parameters)
        sql = "UPDATE choices  \
               SET description=:description, correct=:correct \
               WHERE id =:choice_id"
        for choice in choices:
            if "correct"+str(choice[0]) in parameters:
                correct = True
            else:
                correct = False
            db.session.execute(sql, 
                {"correct":correct,
                 "description":parameters["choice"+str(choice[0])],
                 "choice_id":choice[0]})
        db.session.commit()
        return True
    except:
        return False

def add_choices(parameters):
    sql = "INSERT INTO choices (correct, description, exercise_id, created_at) \
           VALUES (:correct, :description, :exercise_id, :created_at)"
    for choice in range(1, int(parameters["choices"])+1):
        if parameters["choice"+str(choice)] != "":
            db.session.execute(sql, 
                {"correct":("correct"+str(choice) in parameters),
                 "description":parameters["choice"+str(choice)],
                 "exercise_id":parameters["exercise_id"],
                 "created_at":parameters["created_at"]})

def get_exercise_choises(exercise_id):
    sql = "SELECT id, description, correct \
           FROM choices \
           WHERE exercise_id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    return result.fetchall()

def add_answer(exercise_id, choice_id):
    sql = "INSERT INTO answers (exercise_id, choice_id, user_id, answered_at) \
           VALUES (:exercise_id, :choice_id, :user_id, :answered_at)"
    try:
        db.session.execute(sql,
            {"exercise_id": exercise_id,
             "choice_id": choice_id,
             "user_id": str(session["user_id"]),
             "answered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        db.session.commit()
        return True
    except:
        return False

def get_answer_of_current_user(exercise_id):
    sql = "SELECT choice_id \
           FROM answers \
           WHERE exercise_id=:exercise_id AND user_id=:user_id"
    result = db.session.execute(sql,
                {"exercise_id":exercise_id,
                 "user_id":str(session["user_id"])})
    try:
        return result.fetchone()[0]
    except:
        return None

def get_course_result_summary(course_id):
    sql = "SELECT chapters.name, \
            exercises.name, \
            SUM(CASE WHEN (SELECT correct FROM choices WHERE id = answers.choice_id) THEN 1 ELSE 0 END) as correct_answers,\
            SUM(CASE WHEN (SELECT NOT(correct) FROM choices WHERE id = answers.choice_id) THEN 1 ELSE 0 END) as wrong_answers, \
            SUM(CASE WHEN (SELECT TRUE FROM choices WHERE id = answers.choice_id) THEN 1 ELSE 0 END) as total, \
            exercises.ordinal, \
            chapters.ordinal \
            FROM exercises \
            LEFT JOIN answers ON answers.exercise_id=exercises.id \
            JOIN chapters ON chapters.id = exercises.chapter_id \
            WHERE exercises.course_id =:course_id \
            GROUP BY exercises.id, chapters.id \
            ORDER BY chapters.ordinal, exercises.ordinal"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()