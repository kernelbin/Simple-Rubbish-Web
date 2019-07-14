from main import db, app, config, csrf
from flask import session, request
from util import encode_json, make_response
from models import *
from sqlalchemy.sql.expression import *
@csrf.exempt
@app.route("/api/packet/process", methods=["POST", "GET"])
def packet_process():
    """
    处理丢垃圾事件。
    {
    "userid":"用户ID",
    "type":"垃圾种类",
    "uuid":"垃圾桶id"
    }
{
    "code":0,
    "ok":true/false,
    "process_id":2333
}
    """
    user = db.session.query(User).filter(User.id == request.form["userid"])

    if user.count() == 0:
        return make_response(-1, message="未知用户ID")
    if request.form.get("type", "_") not in {"dry", "wet", "recyclable", "harmful"}:
        return make_response(-1, message="未知垃圾种类")
    if request.form.get("uuid", "_") not in config.ALLOW_CLIENTS:
        return make_response(-1, message="未认证客户端")
    user = user.one()
    log = RubbishLog()
    log.rubbish_bin = config.ALLOW_CLIENTS[request.form["uuid"]]
    log.rubbish_type = request.form["type"]
    import datetime
    log.time = datetime.datetime.now()
    log.user_id = user.id

    db.session.add(log)
    db.session.commit()
    retid = log.id
    return make_response(0, process_id=retid)
