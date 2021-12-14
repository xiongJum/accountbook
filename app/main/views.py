from flask import render_template
from . import main
from flask_login import login_required
from datetime import datetime
from .query_data import generateChart, amount_

"""蓝本中路由装饰器由蓝本提供， 即使用main.route
在蓝本中 Flask 会为蓝本中全部端点加上一个命名空间（Blueprint 构造函数的第一个参数），它与端点名之间以一个点号分隔，即为 mian.index。url_for()函数支持省略蓝本名的简写形式，即为 .index（但跨蓝本必须带上蓝本名）
"""

@main.route('/', methods=['GET', 'POST'])
@login_required
def index(): # 数据汇总
    today =  datetime.now()

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

    print(generateChart())
    return render_template('index.html', amount=amount)

    

            