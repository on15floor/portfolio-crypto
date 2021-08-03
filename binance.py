import json
import hmac
import hashlib
import requests
import urllib
import time

from utils import SilentException
from urllib.parse import urlparse


# Возвращает цену пары в USD или 0
def get_pair_price(ticker='BTC'):
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT')
    if 'Invalid symbol' in response.text:
        return 0
    else:
        pair_price = json.loads(response.text)
        return pair_price['price']


# Обертка API Binance
class Binance:
    def __init__(self, api_key, api_secret):
        self.base_url = 'https://api.binance.com/'
        self.API_KEY = api_key
        self.API_SECRET = bytearray(api_secret, encoding='utf-8')

    def call_api(self, url):
        # Генерируем подпись
        payload = {'timestamp': int(time.time() - 1) * 1000}
        payload_str = urllib.parse.urlencode(payload).encode('utf-8')
        sign = hmac.new(key=self.API_SECRET, msg=payload_str, digestmod=hashlib.sha256).hexdigest()
        payload_str = payload_str.decode("utf-8") + "&signature=" + str(sign)

        # Get запрос
        response = requests.request(method='GET', url=self.base_url + url + '?' + payload_str,
                                    headers={"X-MBX-APIKEY": self.API_KEY,
                                             "Content-Type": "application/x-www-form-urlencoded"})

        # Возращаем результат
        obj = json.loads(response.text)
        return obj

    def get_wallet(self):
        try:
            wallet = []
            print(f'[i] Получаем кошелек аккаунта Binance в паре c USD (может занять некоторое время)')
            coins = self.call_api('api/v3/account')
            for coin in coins['balances']:
                ticker = coin['asset']
                amount = float(coin['free'])
                if amount == 0:
                    continue
                price = float(get_pair_price(ticker))
                balance = amount * price
                wallet.append([ticker, amount, price, balance])
            return wallet
        except SilentException as e:
            print('[e] Ошибка:', e)
