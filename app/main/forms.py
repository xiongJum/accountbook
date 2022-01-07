import datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, TextAreaField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class WriteForm(FlaskForm):
    # account_book = StringField("账本", validators=[DataRequired])
    today = datetime.date.today()
    timestart = DateField("日期",default=None)
    amount = FloatField("金额", validators=[DataRequired()])
    # direction = BooleanField("方向", validators=[DataRequired()])
    tag = StringField("标签", validators=[DataRequired()])
    remark = TextAreaField("备注")
    submit = SubmitField("记账")
    

