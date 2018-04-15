from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import DataRequired

class NewStock(FlaskForm):
    symbol = SelectField("Stock Symbol", choices=[('ETH', 'Ethereum'), ('XRP', 'Ripple'), ('BTC', 'Bitcoin'), ('BCH', 'Bitcoin Cash'), ('LTC', 'Litecoin')])
    amount = FloatField("Amount Purchased", validators=[DataRequired()])
    price = FloatField("Purchase Price", validators=[DataRequired()])
    date = DateField("Data Purchased", format='%Y-%m-%d')
    submit = SubmitField("Submit")