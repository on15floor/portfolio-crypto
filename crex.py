import json
import hmac
import hashlib
import requests
import datetime
import base64

from utils import SilentException


# Возвращает цену пары в USD или 0
def get_pair_price(ticker='APC'):
    response = requests.get(f'https://api.crex24.com/v2/public/tickers?instrument={ticker}-BTC')
    if 'invalid value' in response.text:
        return 0
    else:
        pair_price_in_btc = json.loads(response.text)[0]['last']
        response = requests.get('https://api.crex24.com/v2/public/tickers?instrument=BTC-USDT')
        btc_usd = json.loads(response.text)[0]['last']
        return pair_price_in_btc * btc_usd


# Основной класс
class Crex:
    def __init__(self, api_key, api_secret):
        self.baseUrl = "https://api.crex24.com"
        self.API_KEY = api_key
        self.API_SECRET = api_secret

    def call_api(self, url):
        nonce = round(datetime.datetime.now().timestamp() * 1000)

        # Генерируем подпись
        key = base64.b64decode(self.API_SECRET)
        message = str.encode(url + str(nonce), "utf-8")
        h = hmac.new(key=key, msg=message, digestmod=hashlib.sha512)
        sign = base64.b64encode(h.digest()).decode()

        # Get запрос
        response = requests.get(self.baseUrl + url, headers={'User-Agent': 'script',
                                                             'X-CREX24-API-KEY': self.API_KEY,
                                                             'X-CREX24-API-NONCE': str(nonce),
                                                             'X-CREX24-API-SIGN': sign})

        # Возращаем результат
        obj = json.loads(response.text)
        return obj

    def get_wallet(self):
        try:
            wallet = []
            print(f'[i] Получаем кошелек аккаунта Crex24 в паре c USD (может занять некоторое время)')
            coins = self.call_api('/v2/account/balance')
            for coin in coins:
                ticker = coin['currency']
                amount = coin['available']
                price = get_pair_price(ticker)
                balance = amount * price
                wallet.append([ticker, amount, price, balance])
            return wallet
        except SilentException as e:
            print('[e] Ошибка:', e)
