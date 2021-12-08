from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), 
                                            Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        # Regexp 验证函数，正则表达式后面的参数为 正则表达式的标识，和失败时显示的错误信息
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能包含字母、数字、点或下划线')])
    # EqualTo 验证函数，校验两个字段是否一致，另一个字段要作为参数传入
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    """自定义验证函数
    邮箱或者用户名重复校验"""
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')

class LoginForm(FlaskForm):
    """PasswordField 类表示属性为 type="password" 的 <input> 元素。BooleanField 类表示复选框。
    Length() 长度校验， Email() 邮箱格式校验， DataRequired() 必填校验。
    """
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), 
                                            Email()]) # 按照指定顺序进行校验
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住登录状态')
    submit = SubmitField('登录')

