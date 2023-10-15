import requests
import json
from config import keys


class ConvertionExeption(Exception):
    pass

class Converter:
    @staticmethod
    def converter(quote, base, amount):
        if quote == base:
            raise ConvertionExeption(f"Невозможно перевести одинаковые валюты {quote}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f"Не удалось обработать количество {amount}")
        data = requests.get(f"https://api.currencyapi.com/v3/latest?apikey=cur_live_vhaIEHO3qNQE23tVCJA0NrUuIZEVZ7ryS3bBeJIZ&base_currency={base_ticker}&currencies={quote_ticker}")
        total_data = float(json.loads(data.content)["data"][quote_ticker]["value"]) * float(amount)
        return total_data