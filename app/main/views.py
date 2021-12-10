from flask import render_template, session, redirect, url_for
from . import main
from .. import create_app, db
from ..models import Bill
from flask_login import login_required
from sqlalchemy import func

"""蓝本中路由装饰器由蓝本提供， 即使用main.route
在蓝本中 Flask 会为蓝本中全部端点加上一个命名空间（Blueprint 构造函数的第一个参数），它与端点名之间以一个点号分隔，即为 mian.index。url_for()函数支持省略蓝本名的简写形式，即为 .index（但跨蓝本必须带上蓝本名）
"""
@main.route('/', methods=['GET', 'POST'])
@login_required
def index(): # 数据汇总
    sum_amount = []
    sum_pay_amount = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='PAY').scalar()
    sum_amount.append('%.2f' % sum_pay_amount)
    sum_income = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='INCOME').scalar()
    sum_amount.append('%.2f' % sum_income)
    return render_template('index.html', amount=sum_amount)

    

            