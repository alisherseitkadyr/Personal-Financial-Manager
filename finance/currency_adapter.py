# currency_adapter.py

import requests


class CurrencyAdapter:
    API_URL = "https://v6.exchangerate-api.com/v6/e387c239a84073b51051f933/latest/KZT"

    @staticmethod
    def get_exchange_rates():
        response = requests.get(CurrencyAdapter.API_URL)

        if response.status_code == 200:
            try:
                data = response.json()
                if 'conversion_rates' in data:
                    return data['conversion_rates']
                else:
                    raise ValueError("Error: 'conversion_rates' key not found in the API response.")
            except ValueError as e:
                raise ValueError(f"Error parsing JSON response: {e}")
        else:
            raise ValueError(f"Error fetching exchange rates. Status code: {response.status_code}")

    @staticmethod
    def convert(amount, from_currency, to_currency, rates):
        if from_currency == "KZT":
            rate = rates[to_currency]
        elif to_currency == "KZT":
            rate = 1 / rates[from_currency]
        else:
            rate = rates[to_currency] / rates[from_currency]

        return amount * rate
