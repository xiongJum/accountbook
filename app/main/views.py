import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from . forms import WriteForm
from .. import db
from ..models import Book


@main.route('/', methods=["GET", "POST"])
def index():
    return "<p>Hello, World!</p>"

@main.route('/write/pay', methods=["GET", "POST"])
def pay():
    form = WriteForm()
    if form.validate_on_submit():
        book = Book(user_id=1,
                timestart=form.timestart.data,
                amount=form.amount.data,
                direction=False,
                account_book="common",
                tag=form.tag.data,
                remark=form.remark.data)
        db.session.add(book)
        db.session.commit()
        flash("成功记账")
        return redirect(url_for('.pay'))
    form.timestart.data = datetime.date.today()
    return render_template('write.html', form=form)
