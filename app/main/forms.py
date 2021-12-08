from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms import FloatField
from datetime import datetime

class BillForm(FlaskForm):
    """PasswordField 类表示属性为 type="password" 的 <input> 元素。BooleanField 类表示复选框。
    Length() 长度校验， Email() 邮箱格式校验， DataRequired() 必填校验。
    """
    accounting_time = DateField('记账日期')
    payment_method = SelectField('支付方式',choices=[
                                                ('aliPay', '支付宝'), 
                                                ('WeChat', '微信'), 
                                                ('CMBC', '招商银行'), 
                                                ('Ant Credit Pay', '花呗')
                                                ])
    direction = SelectField('发生方向', choices=[
                                            ('Pay', '支出'), 
                                            ('income', '收入')
                                            ])
    amount = FloatField('金额', default = '0.00')
    category = SelectField('分类',choices=[
                                    ('clothes', '衣服'), 
                                    ('food', '餐饮'), 
                                    ('housing', '住房'), 
                                    ('travel', '出行'),
                                    ('play', '游戏')
                                    ])
    label = StringField('标签')
    ledger = SelectField('分类',choices=[
                                    ('common', '普通'), 
                                    ('trade', '交易'), 
                                    ('Medical treatment', '医疗'), 
                                    ('Hobby', '爱好')
                                    ])     
    remark = TextAreaField('备注')      
    submit = SubmitField('记账')
