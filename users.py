from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username,password):
    sql = "SELECT users.password, users.id, roles.name \
           FROM users LEFT JOIN roles ON roles.id = users.role_id \
           WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"]=user[1]
            session["username"]=username
            session["role"]=user[2]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["role"]

def register(username,password,first_name,last_name):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,first_name,last_name, role_id) \
               VALUES (:username,:password,:first_name,:last_name, \
                      (SELECT id FROM roles WHERE name = 'student'))"
        db.session.execute(sql, 
            {"username":username,"password":hash_value,"first_name":first_name,"last_name":last_name})
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_all_users():
    sql = "SELECT users.username, users.first_name, users.last_name, roles.name, users.id \
           FROM users LEFT JOIN roles ON users.role_id = roles.id \
           ORDER BY users.username"
    result = db.session.execute(sql)
    return result.fetchall()

def get_user(id):
    sql = "SELECT users.username, users.first_name, users.last_name, roles.name, users.id \
           FROM users LEFT JOIN roles on users.role_id = roles.id \
           WHERE users.id =:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_roles():
    sql = "SELECT id, name FROM roles"
    result = db.session.execute(sql)
    return result.fetchall()

def update_user(parameters):
    try:
        sql = "UPDATE users SET first_name=:first_name, last_name=:last_name, role_id=:role_id WHERE id=:user_id"
        db.session.execute(sql, parameters)
        db.session.commit()
        return True
    except:
        return False


