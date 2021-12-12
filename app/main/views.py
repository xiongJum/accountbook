from flask import render_template, session, redirect, url_for
from . import main
from .. import create_app, db
from ..models import Bill
from flask_login import login_required
from sqlalchemy import func, extract, and_
from datetime import datetime

"""蓝本中路由装饰器由蓝本提供， 即使用main.route
在蓝本中 Flask 会为蓝本中全部端点加上一个命名空间（Blueprint 构造函数的第一个参数），它与端点名之间以一个点号分隔，即为 mian.index。url_for()函数支持省略蓝本名的简写形式，即为 .index（但跨蓝本必须带上蓝本名）
"""
now_year = datetime.now().year
now_month = datetime.now().month
@main.route('/', methods=['GET', 'POST'])
@login_required
def index(): # 数据汇总
    # 总金额
    ## 支付
    sum_pay_amount = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='PAY').scalar()
    # sum_amount.append('%.2f' % sum_pay_amount)
    ## 收入
    sum_income = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='INCOME').scalar()
    # 当月金额
    ## 支付
    sum_this_month_amount_pay =  db.session.query(func.sum(Bill.amount)).filter(and_(
        Bill.direction=='PAY', extract('year', Bill.accounting_time) == now_year,
        extract('month', Bill.accounting_time) == now_year
        )).scalar()
    ## 收入
    sum_this_month_amount_income = db.session.query(func.sum(Bill.amount)).filter(and_(
        Bill.direction=='INCOME', extract('year', Bill.accounting_time) == now_year,
        extract('month', Bill.accounting_time) == now_year
        )).scalar()
    ## 全部金额的字典
    amount = {"pay":sum_pay_amount, "income": sum_income, 'this_month_pay':sum_this_month_amount_pay, 'this_month_income':sum_this_month_amount_income}
    return render_template('index.html', amount=amount)

    

            