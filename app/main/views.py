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
    

    def amount_(direction='PAY', is_total_direction=True, year=None, month=None, day=None):
        search = and_(Bill.direction==direction)

        if year is not None:
            search = and_(search, extract('year', Bill.accounting_time) == today.year)
            if month is not None:
                search = and_(search, extract('month', Bill.accounting_time) == month)
                if day is not None:
                    search = and_(search, extract('day', Bill.accounting_time) == day)

        amount = db.session.query(func.sum(Bill.amount)).filter(search).scalar()
        amount = 0 if amount == None else '%.2f' % amount

        if is_total_direction == True:
            is_total_direction = [amount]
            return amount_('INCOME', is_total_direction, year, month, day)
        elif type(is_total_direction) == list:
            is_total_direction.append(amount)
            return is_total_direction

        return amount

    # 金额
    ## 总金额支出
    total_amount = amount_()

    ## 今年金额支出和收入
    this_year_amount = amount_(year=today.year)
    
    ## 本月金额支出和收入
    this_month_amount = amount_(year=today.year, month=today.month)

    ## 今天金额
    today_amount = amount_(year=today.year, month=today.month, day=today.day)

    ## 去年金额
    last_year_amount = amount_(year=today.year-1)

    ## 上月金额
    last_month_amount = amount_(year=today.year-1, month=today.month-1)

    ## 全部金额的字典
    amount = {
        "total_amount": total_amount,
        "this":{
            "year": this_year_amount,
            "month": this_month_amount,
            "day": today_amount,},
        "last":{
            "year":last_year_amount,
            "month":last_month_amount
        }
            }
    return render_template('index.html', amount=amount)

    

            