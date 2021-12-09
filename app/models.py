from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manger
from datetime import datetime

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
    bills = db.relationship('Bill', backref='user', lazy='dynamic')
    

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

class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    accounting_time = db.Column(db.Date(), nullable=False) # 记账时间，不允许出现空值
    payment_method = db.Column(db.String(64), nullable=False) # 支付方式, 
    direction = db.Column(db.String(64), nullable=False) # 发生方向
    amount = db.Column(db.Float(), nullable=False) # 金额, 浮点数
    category = db.Column(db.String(64), nullable=False) # 分类
    label = db.Column(db.String(64), nullable=True) # 标签，一组字符串
    ledger = db.Column(db.String(64), nullable=False) # 账本
    remark = db.Column(db.Text(), nullable=True) # 备注 长字符串
    users = db.Column(db.Integer, db.ForeignKey('users.id')) # 用户id
    creation_time = db.Column(db.DateTime(), default=datetime.utcnow()) # 创建时间

    def __repr__(self):
        return '<Bill %r>' % self.id

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))