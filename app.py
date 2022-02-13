import time

from flask import Flask
from flask import request

from converter import Converter

app = Flask(__name__)


@app.route('/')
def home():
    return 'Use /convert to convert currency'


@app.route('/convert', methods=['POST'])
def convert():
    request_body = request.get_json()
    if request_body == {}:
        return {"warning": "No body was sent."}

    currency = request_body['currency']
    amount = request_body['amount']
    target_currency = request_body['target_currency']
    try:
        target_amount = Converter.convert(currency, amount, target_currency)
    except KeyError:
        return create_error_response("Wrong currency used."), 400

    response = {
        "timestamp": "",
        "currency": currency,
        "amount": amount,
        "target_currency": target_currency,
        "target_amount": target_amount
    }
    return response


def create_request_body(currency, amount, target_currency):
    return {
        "currency": currency,
        "amount": amount,
        "target_currency": target_currency
    }


def create_response_body(currency, amount, target_currency, target_amount):
    return {
        "timestamp": time.time(),
        "currency": currency,
        "amount": amount,
        "target_currency": target_currency,
        "target_amount": target_amount
    }


def create_error_response(error):
    return {
        "timestamp": time.time(),
        "error": error
    }
