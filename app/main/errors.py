from flask import render_template
from . import main

"""在蓝本中编写错误处理程序，需要使用 app_errorhandler 装饰器。
若使用 errorhandler 则只有蓝本中的错误才会触发处理程序
"""
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500