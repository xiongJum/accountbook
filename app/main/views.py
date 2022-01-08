import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from . import main
from . forms import WriteForm
from .. import db
from ..models import Book


@main.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@main.route('/write/<directions>', methods=["GET", "POST"])
def write(directions):
    form = WriteForm()
    if form.validate_on_submit():
        direction = False if directions=='pay' else True
        book = Book(user_id=1,
                timestart=form.timestart.data,
                amount=form.amount.data,
                direction=direction,
                account_book="common",
                tag=form.tag.data,
                remark=form.remark.data)
        db.session.add(book)
        db.session.commit()
        flash("成功记账")
        return redirect(url_for('.write', directions=directions))
    form.timestart.data = datetime.date.today()
    return render_template('write.html', form=form, directions=directions)

@main.route('/book', methods=["GET", "POST"])
def book():
    books = Book.query
    page = request.args.get('page', 1, type=int)
    if page == -1: # 计算评论的总量和总也是，得出真正显示的页数
        page = (books.count() - 1) // current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = books.order_by(Book.timestart.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    books = pagination.items
    return render_template('book.html', books=books, pagination=pagination)
