from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from .. models import User
from .forms import LoginForm

"""当请求参数为 GET 时，视图函数会直接渲染模板，即显示登录表单。
当为 POST 时，validate_on_submit() 函数会验证表单数据，然后尝试登入用户。
"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            '''调用 Flask-Login 的 login_user() 函数，在用户会话中把用户标记为已登录。
            若 remember_me 的值等于 True 则在用户的浏览器中写入一个长期有效的 cookie， 使用这个 cookie 可以恢复用户会话，cookie 默认记住为一年，可以使用可选的 REMEMBER_COOKIE_DURATION 配置选项更改这个值。
            '''
            login_user(user, form.remember_me.data) 
            next = request.args.get('next')
            if next is None or not next.startswitch('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('无效的用户名或者密码')
    # 为 render_template() 指定的模板文件保存在 auth 目录中。
    # 这个目录必须在 app/ templates 中创建。
    return render_template('auth/login.html', form=form)

from flask_login import logout_user, login_required

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.login'))

