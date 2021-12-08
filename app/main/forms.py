from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email

class BillForm(FlaskForm):
    """PasswordField 类表示属性为 type="password" 的 <input> 元素。BooleanField 类表示复选框。
    Length() 长度校验， Email() 邮箱格式校验， DataRequired() 必填校验。
    """
    datetime = DateField('记账时间')