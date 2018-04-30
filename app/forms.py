from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import DataRequired

class NewStock(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(message="Symbol Required")])
    amount = FloatField("Amount Purchased", validators=[DataRequired()])
    price = FloatField("Purchase Price", validators=[DataRequired()])
    date = DateField("Data Purchased", format='%Y-%m-%d')
    submit = SubmitField("Submit")

class AddSymbol(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(message="Symbol Required")])
    addtransaction = BooleanField("Add Transaction")
    submit = SubmitField("Add")