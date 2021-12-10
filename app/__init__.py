from flask import Flask, render_template
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

"""扩展对象"""
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manger = LoginManager()
# login_view 属性用于设置登录页面的端点。
# 因为登录路由在蓝本中定义，所以要在前面加上蓝本的名称
# 匿名用户尝试访问受保护的页面时，Flask-Login 将重定向到登录页面。
login_manger.login_view = 'auth.login'


def create_app(config_name):
    """ 工厂函数，接受一个参数（应用使用的配置名）；
    配置类在 config.py 中定义，其中保存的配置，可以直接使用 app.config 配置对象提供的 from_object() 方法直接导入应用，配置对象可以直接可以直接通过名称从 config 字典中选择
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    """初始化扩展，需要调用 init_app()方法"""
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manger.init_app(app)

    """注册主蓝本"""
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    """注册身份验证蓝本"""
    from .auth import auth as auth_blueprint
    # 如果使用了 url_prefix，注册后蓝本中定义的所有路由都会加上指定的前缀
    # 即 /login 注册为 /auth/login, 完整路径变为 http://localhost/auth/login 
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    """注册账本蓝本"""
    from .bill import bill as bill_blueprint
    app.register_blueprint(bill_blueprint, url_prefix='/bill')

    # 添加路由和自定义的错误页面

    return app