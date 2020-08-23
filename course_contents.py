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


def get_exercise_choises(exercise_id):
    sql = "SELECT id, description FROM exercises WHERE exercise_id=:exercise_id ORDER BY ordinal, name"
    result = db.session.execute(sql, {"exercise_id": exercise_id})
    return result.fetchall
