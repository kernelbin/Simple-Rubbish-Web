from main import db


class RubbishLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    rubbish_type = db.Column(db.String(32), nullable=False)
    rubbish_bin = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
