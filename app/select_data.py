from . import db
from .models import Book
from sqlalchemy import func, extract, and_
from datetime import datetime


def _amount(direction=True, is_total_direction=True, year=None, month=None, day=None):

        search = and_(Book.direction==direction)

        if year == None: # 查询 月日
            if month !=None:
                if day == None: # 查询月日
                    search = and_(search, extract('day', Book.timestart) == day, extract('month', Book.timestart) == month)
                else: # 查询月:
                    search = and_(search, extract('month', Book.timestart) == month)
            else:
                if day != None: ## 查询日
                    search = and_(search, extract('day', Book.timestart) == day)

        else: # 查询年月日
            if month == None: ## 查询年日
                if day != None: ### 查询年日
                    search = and_(search, extract('day', Book.timestart) == day, extract('year', Book.timestart) == year)
                else: # 查询年
                    search = and_(search, extract('year', Book.timestart) == year)
            else: # 查询年月
                if day == None: # 查询年月
                    search = and_(search, extract('month', Book.timestart) == month, extract('year', Book.timestart) == year)
                else: ## 查询年月日
                    search = and_(search, extract('day', Book.timestart) == day, extract('month', Book.timestart) == month, extract('year', Book.timestart) == year)

        amount = db.session.query(func.sum(Book.amount)).filter(search).scalar()
        amount = 0 if amount == None else '%.2f' % amount

        if is_total_direction == True:
            is_total_direction = [amount]
            return _amount(False, is_total_direction, year, month, day)
        elif type(is_total_direction) == list:
            is_total_direction.append(amount)
            return is_total_direction

        return amount

"""数据点"""
"""TODO:
    - 还需要增加一些数据"""
def amountDataPoint():
    
    today =  datetime.now()

    total_amount = _amount() # 所有发生额
    total_today_amount = _amount(day=today.day) # 本日的所有发生额
    total_month_amount = _amount(month=today.month) #本月的所有发生额

    this_year_amount = _amount(year=today.year) ## 本年金额支
    this_month_amount = _amount(year=today.year, month=today.month) ## 本月金额
    today_amount = _amount(year=today.year, month=today.month, day=today.day) ## 今天金额
    
    last_year_amount = _amount(year=today.year-1) ## 去年金额
    last_month_amount = _amount(year=today.year-1, month= 12 if today.month-1==0 else today.month-1) ## 上月金额

    ## 同比
    ony_month_amont = _amount(year=today.year-1, month=today.month) # 去年的本月
    ony_today_amont = _amount(today.month-1, day=today.day)# 上月今天

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

    return amount


def generateChart():
            
    amount = lambda month: _amount(is_total_direction=False, year=datetime.now().year, month=month)

    total_this_month_amount = {month: amount(month) for month in range(1,13)} # 当月全部数据

    return total_this_month_amount