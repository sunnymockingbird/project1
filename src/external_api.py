import os

import requests
from dotenv import load_dotenv

from src.generators import looking_target_key

load_dotenv()
API_KEY = os.getenv("API_KEY", "")


def convert(transaction: dict) -> float:
    """Осуществляет конвертацию суммы в рубли, если она задана в USD или EUR"""

    currency = looking_target_key(transaction)
    amount = looking_target_key(transaction, "amount")
    if currency is None or amount is None:
        raise ValueError("Валюта/Сумма транзакции не найдена")

    if currency != "RUB":
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        payload: dict[str, str] = {}
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            return float(response.json()["result"])
        raise ValueError(f"Ошибка API: {response.status_code}")

    return float(amount)
