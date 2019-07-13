from main import  db,app
from flask import session, request
from util import encode_json, make_response
from models import *
from sqlalchemy.sql.expression import *
@app.route("/api/login",methods=["POST"])
def login():
    """
    登录
    参数:{
        "identifier":"用户标识符",
        "password":"密码"
    }
    """
    if session.get("userid") is not None:
        return make_response(-1, {
            "message": "用户已登录"
        })
    query = db.session.query(User).filter(or_(
        User.email == request.form["identifier"], User.username == request.form["identifier"])).filter(User.password == request.form["password"])
    if not query.count():
        return make_response(-1, {
            "message": "用户名或密码错误"
        })
    session["userid"] = query.one().id
    return make_response(0)
