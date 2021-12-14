from .. import db
from ..models import Bill
from sqlalchemy import func, extract, and_

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
        amount = 0 if amount == None else '%.2f' % amount

        if is_total_direction == True:
            is_total_direction = [amount]
            return amount_('INCOME', is_total_direction, year, month, day)
        elif type(is_total_direction) == list:
            is_total_direction.append(amount)
            return is_total_direction

        return amount


def generateChart():
    
    from datetime import datetime
        
    amount = lambda month: amount_(is_total_direction=False, year=datetime.now().year, month=month)

    test = {month: amount(month) for month in range(1,13)}

    return test