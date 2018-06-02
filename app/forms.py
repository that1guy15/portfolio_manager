import requests
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import DataRequired, ValidationError

def api_get(query):
    """
    Runs API GET query on given url
    query - str

    :return:
    Returns JSON payload
    """
    resp = requests.get(query)
    if resp.status_code != 200:
        raise ApiError('GET API {}'.format(resp.status_code))
    api_data = resp.json()

    return api_data

def crypto_check(form, field):
    crypto_list = api_get('https://min-api.cryptocompare.com/data/all/coinlist')

    if field.data not in crypto_list['Data']:
        raise ValidationError('{} is not a valid Crypto'.format(field.data), 'error')

class NewStock(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(message="Symbol Required"), crypto_check])
    amount = FloatField("Amount Purchased", validators=[DataRequired()])
    price = FloatField("Purchase Price", validators=[DataRequired()])
    date = DateField("Date Purchased", format='%Y-%m-%d')
    submit = SubmitField("Submit")

class AddSymbol(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(message="Symbol Required"), crypto_check])
    addtransaction = BooleanField("Add Transaction")
    submit = SubmitField("Add")