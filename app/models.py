from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manger

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    @property # 装饰器，对参数进行必要的检查
    def password(self):
        raise AttributeError("不可直接访问密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """与存储在 User 模型中的密码散列值进行比对。如果这个方法返回 True，表明密码是正确的
        """
        return check_password_hash(self.password_hash, password)

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))