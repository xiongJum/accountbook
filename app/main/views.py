from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
# from .forms import NameForm
from .. import db
from ..models import User

"""蓝本中路由装饰器由蓝本提供， 即使用main.route
在蓝本中 Flask 会为蓝本中全部端点加上一个命名空间（Blueprint 构造函数的第一个参数），它与端点名之间以一个点号分隔，即为 mian.index。url_for()函数支持省略蓝本名的简写形式，即为 .index（但跨蓝本必须带上蓝本名）
"""
# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         # ...
#         return redirect(url_for('.index'))

#     return render_template('index.html',
#                             form=form, name=session.get('name'),
#                             known=session.get('known', False),
#                             current_time=datetime.utcnow()) # datetime.utcnow() 读取世界标准时间

            