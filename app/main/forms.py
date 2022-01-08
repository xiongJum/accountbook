import datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, TextAreaField, BooleanField, SubmitField, DateField
from wtforms import SelectField
from wtforms.validators import DataRequired

class WriteForm(FlaskForm):
    # account_book = StringField("账本", validators=[DataRequired])
    timestart = DateField("日期",default=None)
    amount = FloatField("金额", validators=[DataRequired()])
    # direction = BooleanField("方向", validators=[DataRequired()])
    tag = StringField("标签", validators=[DataRequired()])
    remark = TextAreaField("备注")
    submit = SubmitField("记账")

class EditItemsForm(FlaskForm):
    """修改账本"""

    account_book = StringField("账本", validators=[DataRequired()])
    timestart = DateField("日期",validators=[DataRequired()])
    amount = FloatField("金额", validators=[DataRequired()])
    direction = SelectField ("方向", coerce=bool)
    tag = StringField("标签", validators=[DataRequired()])
    remark = TextAreaField("备注")
    submit = SubmitField("修改")

    def __init__(self, *args, **kwargs):
        super(EditItemsForm, self).__init__(*args, **kwargs)
        self.direction.choices = [(False, "支出"), (True, "记账")]
        

    

