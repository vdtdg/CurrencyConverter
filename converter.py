import time

import requests as requests


class Converter:
    rates = dict()
    last_pull_timestamp = 0
    api_key = "28ffc6e03ae907d649e7f57ae5735493"

    @staticmethod
    def convert(currency, amount, target_currency):
        change_rates = Converter.get_change_rates()
        change_rate = change_rates[target_currency] / change_rates[currency]
        return float(amount) * change_rate

    @staticmethod
    def get_change_rates() -> dict:
        # If the last pull is older than 12 hours ago
        if time.time() - Converter.last_pull_timestamp > 3600 * 12:
            response = requests.get(
                f"http://api.exchangeratesapi.io/v1/latest?access_key={Converter.api_key}&symbols=&format=1")
            Converter.rates = response.json()
        return Converter.rates
