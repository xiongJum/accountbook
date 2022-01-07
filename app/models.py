import datetime
from enum import unique
from . import db

class User(db.Model):
    __tablename__ = 'users'
    # 创建必要字段
    """TO-DO 后续增加邮箱和密码字段"""
    id = db.Column(db.Integer, primary_key=True) # id，自增
    username = db.Column(db.String(64), unique=False, index=True) # 用户名
    books = db.relationship('Book', backref='user', lazy='dynamic')
    
    def __repr__(self) -> str:
        return '<User %r>' % self.username

class Book(db.Model):
    """账本模型"""
    ####### 字段说明 #######
    # id[主键]: int, 唯一 自增
    # user_id[用户id]: int 非空
    # timestart[发生日期]: datetime 非空
    # amount[金额]: float, 最大2位小数, 非空
    # direction[方向]: bool, true 为收入，false 非空
    # account_book[账本]: 非空
    # tag[标签]: 非空
    # remark： str 长字符串
    # timecreate[创建时间]: datetime

    """TO-DO 增加坐标"""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestart = db.Column(db.Date, index=True, default=datetime.date.today)
    amount = db.Column(db.Float, unique=False)
    direction = db.Column(db.Boolean, unique=False)
    account_book = db.Column(db.String(64), unique=False)
    tag = db.Column(db.Text, unique=False)
    remark = db.Column(db.Text, unique=True)
    timecreate = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self) -> str:
        return '<Book %r>' % self.id