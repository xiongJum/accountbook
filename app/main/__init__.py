from flask import Blueprint

"""创建 Blueprint 类对象创建蓝本
必须指定两个参数，蓝本的名称和蓝本所在的包或者模块（多数情况下，使用 Python 的 __name__ 变量即可）
"""
main = Blueprint('main', __name__)

""" 应用的路由保存在 app/main/views.py 模块中，错误处理程序保存在 app/main/errors.py 模块中。
导入这两个模块，将路由和处理程序与蓝本关联起来。
避免循环导入（以下模块还需要导入 main 蓝本），这些脚本需要在末尾引用
"""
from . import views, errors

