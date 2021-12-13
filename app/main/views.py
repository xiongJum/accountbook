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

@main.route('/', methods=['GET', 'POST'])
@login_required
def index(): # 数据汇总
    today =  datetime.now()
    
    # def thisYearAmont(direction='INCOME', year=today.year):

    #     amount = db.session.query(func.sum(Bill.amount)).filter(and_(
    #         Bill.direction==direction, extract('year', Bill.accounting_time) == year
    #         )).scalar()

    # def thisMonthAmount(direction='INCOME', month=today.month):

    #     amount = db.session.query(func.sum(Bill.amount)).filter(and_(
    #         Bill.direction==direction, extract('year', Bill.accounting_time) == today.year,
    #         extract('month', Bill.accounting_time) == month,
    #         )).scalar()
        
    #     return amount

    def amount(direction='INCOME', year=today.year, month=None, day=None):
        search = and_(Bill.direction==direction, extract('year', Bill.accounting_time) == today.year)
        
        if month is not None:
            search = and_(search, extract('month', Bill.accounting_time) == month)
            if day is not None:
                search = and_(search, extract('day', Bill.accounting_time) == day)

        return db.session.query(func.sum(Bill.amount)).filter(search).scalar()


        # amount = db.session.query(func.sum(Bill.amount)).filter(and_(
        #     Bill.direction==direction, extract('year', Bill.accounting_time) == today.year,
        #     extract('month', Bill.accounting_time) == today.month,
        #     extract('day', Bill.accounting_time) == day
        #     )).scalar()

    # 金额
    ## 总金额支出
    total_pay = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='PAY').scalar()
    # sum_amount.append('%.2f' % sum_pay_amount)
    ## 总金额收入
    total_income = db.session.query(func.sum(Bill.amount)).filter(Bill.direction=='INCOME').scalar()

    ## 今年金额支出和收入
    this_year_pay = amount('PAY')
    this_year_income = amount()
    
    ## 本月金额支出和收入
    this_month_pay = amount('PAY', month=today.month)
    this_month_income = amount(month=today.month)

    ## 今天金额
    today_amount_pay = amount('PAY', month=today.month, day=today.day)
    today_amount_income = amount(month=today.month, day=today.day)

    ## 去年金额
    last_year_pay = amount('PAY', year=today.year-1)
    last_year_income = amount(year=today.year-1)

    ## 上月金额

    ## 全部金额的字典
    amount = {
        "pay":total_pay, 
        "income": total_income, 
        "this":{
            "year":[this_year_pay, this_year_income],
            "month": [this_month_pay, this_month_income]
        }}
    return render_template('index.html', amount=amount)

    

            