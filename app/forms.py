from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import DataRequired

class NewStock(FlaskForm):
    symbol = SelectField("Stock Symbol", choices=[('btcusd', 'Bitcoin'), ('ltcusd', 'Litecoin'), ('ethusd', 'Ethereum'), ('bchusd', 'Bitcoin Cash')])
    amount = FloatField("Amount Purchased", validators=[DataRequired()])
    price = FloatField("Purchase Price", validators=[DataRequired()])
    date = DateField("Data Purchased", format='%Y-%m-%d')
    submit = SubmitField("Submit")