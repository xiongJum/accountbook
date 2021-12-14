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

        if year == None: # 查询 月日
            if month !=None:
                if day == None: # 查询月日
                    search = and_(search, extract('day', Bill.accounting_time) == day, extract('month', Bill.accounting_time) == month)
                else: # 查询月:
                    search = and_(search, extract('month', Bill.accounting_time) == month)
            else:
                if day != None: ## 查询日
                    search = and_(search, extract('day', Bill.accounting_time) == day)

        else: # 查询年月日
            if month == None: ## 查询年日
                if day != None: ### 查询年日
                    search = and_(search, extract('day', Bill.accounting_time) == day, extract('year', Bill.accounting_time) == year)
                else: # 查询年
                    search = and_(search, extract('year', Bill.accounting_time) == year)
            else: # 查询年月
                if day == None: # 查询年月
                    search = and_(search, extract('month', Bill.accounting_time) == month, extract('year', Bill.accounting_time) == year)
                else: ## 查询年月日
                    search = and_(search, extract('day', Bill.accounting_time) == day, extract('month', Bill.accounting_time) == month, extract('year', Bill.accounting_time) == year)

        amount = db.session.query(func.sum(Bill.amount)).filter(search).scalar()
        print(str(db.session.query(func.sum(Bill.amount)).filter(search)))
        amount = 0 if amount == None else '%.2f' % amount

        if is_total_direction == True:
            is_total_direction = [amount]
            return amount_('INCOME', is_total_direction, year, month, day)
        elif type(is_total_direction) == list:
            is_total_direction.append(amount)
            return is_total_direction

        return amount

    # 金额
    ## 总金额
    total_amount = amount_() # 所有发生额
    total_today_amount = amount_(day=today.day) # 本日的所有发生额
    total_month_amount = amount_(month=today.month) #本月的所有发生额

    this_year_amount = amount_(year=today.year) ## 本年金额支
    this_month_amount = amount_(year=today.year, month=today.month) ## 本月金额
    today_amount = amount_(year=today.year, month=today.month, day=today.day) ## 今天金额
    
    last_year_amount = amount_(year=today.year-1) ## 去年金额
    last_month_amount = amount_(year=today.year-1, month=today.month-1) ## 上月金额

    ## 同比
    ony_month_amont = amount_(year=today.year-1, month=today.month) # 去年的本月
    ony_today_amont = amount_(today.month-1, day=today.day)# 上月今天


    

    ## 全部金额的字典
    amount = {
        "total_amount": total_amount,
        "total_today_amount": total_today_amount,
        "total_month_amount": total_month_amount,
        "this":{
            "year": this_year_amount,
            "month": this_month_amount,
            "day": today_amount,},
        "last":{
            "year":last_year_amount,
            "month":last_month_amount
        },
        "ony":{
            "month": ony_month_amont,
            "day":ony_today_amont
        },
            }
    return render_template('index.html', amount=amount)

    

            