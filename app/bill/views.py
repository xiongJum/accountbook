from flask import render_template, session, redirect, url_for, current_app
from . import bill
from .forms import BillingFrom
from .. import create_app, db
from ..models import User, Bill
from flask_login import login_required


@bill.route('/account/<int:page>', methods=['GET', "POST"])
@bill.route("/account",methods = ["GET", "POST"])
@login_required
def account(page=None): # 账本
    form = BillingFrom()
    if form.validate_on_submit():
        bill = Bill(accounting_time=form.accounting_time.data,
                    payment_method =form.payment_method.data,
                    direction      =form.direction.data,
                    amount         =form.amount.data,
                    category       =form.category.data,
                    label          =form.label.data,
                    ledger         =form.ledger.data,
                    remark         =form.remark.data,
                    users          =session.get('user_id')
        )
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('bill.account'))

    if not page:
        page = 1
    bills = Bill.query.filter_by().order_by(Bill.accounting_time.desc()).paginate(page=page, per_page=15)
    labels = ['记账日期', '支付方式', '发生方向', '金额', '分类', '备注']
    return render_template('bill/account.html', bills=bills.items, 
                    pagination=bills, labels=labels, form=form)

    

            