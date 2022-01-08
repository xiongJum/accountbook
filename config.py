import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # 密钥
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com') # 邮件服务器
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    # 是否使用 TLS
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]' # 邮件主题前缀
    FLASKY_MAIL_SENDER = 'Flasky Admin <xiongjum121@163.com>' # 发件人
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') # 管理员
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 跟踪修改 SQLALCHEMY
    FLASKY_COMMENTS_PER_PAGE = 15

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bill-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bill.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}