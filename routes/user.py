from main import db, app, config
from flask import session, request, send_file
from util import encode_json, make_response
from models import *
from sqlalchemy.sql.expression import *
@app.route("/api/login", methods=["POST"])
def login():
    """
    登录
    参数:{
        "identifier":"用户标识符",
        "password":"密码"
    }
    返回:{
        "code":"是否调用成功",
        "message":""
    }
    """
    if session.get("userid") is not None:
        return make_response(-1, {
            "message": "用户已登录"
        })
    query = db.session.query(User).filter(or_(
        User.email == request.form["identifier"], User.username == request.form["identifier"])).filter(User.password == request.form["password"])
    if not query.count():
        return make_response(-1, **{
            "message": "用户名或密码错误"
        })
    session["userid"] = query.one().id
    return make_response(0)


@app.route("/api/register", methods=["POST"])
def register():
    """
    登录
    参数:{
        "username":"用户标识符",
        "password":"密码",
        "email":"邮箱"
    }
    返回:{
        "code":"是否调用成功",
        "message":""
    }
    """
    if session.get("userid") is not None:
        return make_response(-1, {
            "message": "用户已登录"
        })
    query = db.session.query(User).filter(or_(
        User.email == request.form["email"], User.username == request.form["username"]))
    if query.count():
        return make_response(-1, **{
            "message": "用户已存在"
        })
    # session["userid"] = query.one().id
    user = User(username=request.form["username"],
                email=request.form["email"], password=request.form["password"])
    db.session.add(user)
    db.session.commit()
    session.permanment = True
    session["userid"] = user.id
    return make_response(0)


@app.route("/api/get_login_state", methods=["POST"])
def get_login_state():
    """
    查询登录状态
    参数:
    返回:{
        "code":"是否调用成功",
        "is_login":"是否登录",
        "user_id":"用户id",
        "is_admin":"是否为管理员",
        "username":"用户名  "
    }
    """
    if not session.get("userid", None):
        return make_response(0, is_login=False)
    else:
        user = User.by_id(session.get("userid"))
        return make_response(9, is_login=True, user_id=user.id, is_admin=user.is_admin, username=user.username)


@app.route("/api/logout", methods=["POST"])
def logout():
    """
    登出
    参数:
    """
    if session.get("userid") is None:
        return make_response(-1, message="你尚未登录!")
    session.pop("userid")
    return make_response(0)


@app.route("/api/generate_qrcode/<string:rubbish_type>", methods=["GET"])
def generate_qrcode(rubbish_type: str):
    import qrcode
    if not session.get("userid"):
        return 404
    image = qrcode.make("{} {}".format(
        session.get("userid"), rubbish_type)).get_image()
    import tempfile
    file = tempfile.mktemp(suffix=".png")
    image.save(file)

    return send_file(file)


@app.route("/api/get_history", methods=["GET", "POST"])
def get_history():
    """
    获取扔垃圾历史
    {
        "userid":"用户ID",//对于非管理员，只能是自己
        "page":"页数",
    }
    {
        "code":0,
        "message":"xxx",
        "data":[
            {
                "time":"时间",
                "rubbish_bin":"垃圾桶",
                "rubbish_id":"id",
                "rubbish_type":"种类"
            }
        ],
        "total_pages":"总页数"
    }
    """
    ITEMS_PER_PAGE = 10
    if not session.get("userid"):
        return make_response(-1, message="请先登录")
    user = User.by_id(session.get("userid"))
    target = request.form.get("userid", user.id)
    if str(user.id) != str(target):
        return make_response(-1, message="你没有权限这样做")

    result = db.session.query(RubbishLog).filter(
        RubbishLog.user_id == target).order_by(RubbishLog.id.desc())
    import math
    pages = int(math.ceil(result.count()/ITEMS_PER_PAGE))
    page = int(request.form["page"])
    result = result.slice(
        (page-1)*ITEMS_PER_PAGE, (page)*ITEMS_PER_PAGE).all()
    ret_data = []
    for item in result:
        ret_data.append({
            "time": str(item.time), "rubbish_bin": item.rubbish_bin, "rubbish_id": item.id, "rubbish_type": item.rubbish_type
        })
    return make_response(0, data=ret_data, total_pages=pages)
