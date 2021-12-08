from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    """PasswordField 类表示属性为 type="password" 的 <input> 元素。BooleanField 类表示复选框。
    Length() 长度校验， Email() 邮箱格式校验， DataRequired() 必填校验。
    """
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), 
                                            Email()]) # 按照指定顺序进行校验
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住登录状态')
    submit = SubmitField('登录')

