import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    """密码散列测试
    """
    def test_password_setter(self): # 密码不为空
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self): # 不可直接读取密码
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self): # 验证密码的准确性
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self): # 验证密码是随机的
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)