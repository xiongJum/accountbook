import os
from app import create_app, db
from app.models import Book, User
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Book=Book)

@app.cli.command()
def test():
    """运行单元测试"""
    import unittest 
    tests = unittest.TestLoader().discover('tests') # 将文件夹下的全部文件添加到测试套件中
    unittest.TextTestRunner(verbosity=2).run(tests) # 运行测试套件