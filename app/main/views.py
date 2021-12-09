from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import BillForm
from .. import db
from ..models import User, Bill
from flask_login import login_required

"""蓝本中路由装饰器由蓝本提供， 即使用main.route
在蓝本中 Flask 会为蓝本中全部端点加上一个命名空间（Blueprint 构造函数的第一个参数），它与端点名之间以一个点号分隔，即为 mian.index。url_for()函数支持省略蓝本名的简写形式，即为 .index（但跨蓝本必须带上蓝本名）
"""
# @main.route('/', methods=['GET', 'POST'])
# def index(): # 记账
#     form = BillForm()
#     if form.validate_on_submit():
#         # ...
#         return redirect(url_for('.index'))

#     return render_template('index.html',
#                             form=form, name=session.get('name'),
#                             known=session.get('known', False),
#                             current_time=datetime.utcnow()) # datetime.utcnow() 读取世界标准时间

@main.route('/', methods=['GET', 'POST'])
@login_required
def index(): # 记账
    form = BillForm()
    if form.validate_on_submit():
        bill = Bill(accounting_time=form.accounting_time.data,
                    payment_method =form.payment_method.data,
                    direction      =form.direction.data,
                    amount         =form.amount.data,
                    category       =form.category.data,
                    label          =form.label.data,
                    ledger         =form.ledger.data,
                    remark         =form.remark.data,
                    users          =session.get('id')
        )
        print('打印日志',session.get('name'), session.get('id'))
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template('index.html', form=form)

            