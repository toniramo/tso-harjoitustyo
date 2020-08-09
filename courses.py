from flask import session
from db import db

def get_courses_of_user():
    sql =  "SELECT courses.name, courses.description, users.username, courses.id FROM courses \
            JOIN participants ON courses.id = participants.course_id \
            JOIN users ON courses.teacher_id = users.id \
            WHERE participants.user_id = :user_id"
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    return result.fetchall()

def get_course(course_id):
    sql =  "SELECT courses.name, courses.description, users.username, courses.id \
            FROM courses JOIN users ON courses.teacher_id = users.id \
            WHERE courses.id = :course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()

def get_participants_of_course(course_id):
    sql = "SELECT users.username, users.id FROM users \
            JOIN participants ON users.id = participants.user_id \
            JOIN courses ON participants.course_id = courses.id \
            WHERE courses.id = :course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def get_searched_courses(search_string,teacher,include_enrolled):
    sql =  "SELECT courses.name, courses.description, users.username, courses.id FROM courses \
            JOIN users ON courses.teacher_id = users.id \
            WHERE (courses.name ILIKE :search_string \
                   OR courses.description ILIKE :search_string) \
            AND users.username ILIKE :teacher" 
    if include_enrolled != 'True':
        sql += " AND courses.id NOT IN (SELECT participants.course_id FROM participants WHERE user_id=:user_id)"
        result = db.session.execute(sql, {"search_string":"%"+search_string+"%","teacher":"%"+teacher+"%", "user_id":str(session["user_id"])})
    else:    
        result = db.session.execute(sql, {"search_string":"%"+search_string+"%","teacher":"%"+teacher+"%"})
    return result.fetchall()

def enroll_course(id):
        try: 
            sql = "SELECT user_id FROM participants WHERE course_id=:id AND user_id=:user_id"
            result = db.session.execute(sql, {"id":id, "user_id":session["user_id"]})
            if result.fetchone() == None:
                sql = "INSERT INTO participants (user_id, course_id) VALUES (:user_id,:id)"
                db.session.execute(sql, {"user_id":session["user_id"], "id":id})
                db.session.commit()
                return True
            else:
                return False
        except:
            return False

def new_course(name,description):
    try:
        sql = "INSERT INTO courses (name,description,teacher_id) \
                VALUES (:name,:description,:user_id) \
                RETURNING id"
        result = db.session.execute(sql, {"name":name, "description":description, "user_id":session["user_id"]})
        db.session.commit()
        id = result.fetchone()[0]
        enroll_course(id)
        return id
    except:
        return None

