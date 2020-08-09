from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"]=user[1]
            session["username"]=username
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]

def register(username,password,first_name,last_name):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,first_name,last_name) VALUES (:username,:password,:first_name,:last_name)"
        db.session.execute(sql, {"username":username,"password":hash_value,"first_name":first_name,"last_name":last_name})
        db.session.commit()
    except:
        return False
    return login(username,password)

