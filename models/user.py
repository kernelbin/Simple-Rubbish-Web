from main import db
# from .base import Base


class User(db.Model):
    __tablename__ = "users"
    # 用户ID
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(20), unique=True)
    # 密码
    password = db.Column(db.String(64), nullable=False)
    # 重置密码所需密钥
    reset_token = db.Column(db.String(256), nullable=False)
    @staticmethod
    def by_id(id):
        return db.session.query(User).filter(User.id == id).one()
    def as_dict(self):
        ret = dict(filter(lambda x: not x[0].startswith(
            "_"), self.__dict__.items()))
        return ret