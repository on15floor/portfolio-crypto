import json
import hmac
import hashlib
import requests
import urllib
import os

from utils import SilentException
from urllib.parse import urlparse


# Каждый новый запрос к серверу должен содержать увеличенное число nonce в диапазоне 1-2147483646
def get_nonce():
    base_dir = os.path.dirname(os.path.abspath(__name__))
    nonce_file = os.path.join(base_dir, 'yobit_nonce')

    if not os.path.exists(nonce_file):
        with open(nonce_file, "w") as f:
            f.write('1')

    with open(nonce_file, 'r+') as inp:
        nonce = int(inp.read())
        inp.seek(0)
        inp.write(str(nonce + 1))
        inp.truncate()

    return nonce


# Возвращает цену пары в USD или 0
def get_pair_price(ticker='btc'):
    pair = f'{ticker}_usd'
    response = requests.get(f'https://yobit.net/api/3/ticker/{pair}')
    if 'Invalid pair' in response.text:
        return 0
    else:
        pair_price = json.loads(response.text)
        return pair_price[pair]['avg']


# Обертка API Yobit
class Yobit:
    def __init__(self, api_key, api_secret):
        self.baseUrl = "https://yobit.net"
        self.API_KEY = api_key
        self.API_SECRET = api_secret.encode('utf-8')

    def call_api(self, **kwargs):
        # Формируем Post body
        body = {'nonce': get_nonce()}
        if kwargs:
            body.update(kwargs)
        data = urllib.parse.urlencode(body)

        # Генерируем подпись
        key = self.API_SECRET
        h = hmac.new(key=key, digestmod=hashlib.sha512)
        h.update(data.encode('utf-8'))
        sign = h.hexdigest()

        # Get запрос
        response = requests.post(self.baseUrl + '/tapi/', data=data,
                                 headers={'Content-type': 'application/x-www-form-urlencoded',
                                          'Key': self.API_KEY,
                                          'Sign': sign})
        # Возращаем результат
        obj = json.loads(response.text)
        return obj

    def get_info(self):
        try:
            print('[i] Получаем информацию аккаунта Yobit')
            return self.call_api(method='getInfo')
        except SilentException as e:
            print('[e] Ошибка:', e)

    def get_wallet(self):
        try:
            wallet = []
            print(f'[i] Получаем кошелек Yobit в паре c USD (может занять некоторое время)')
            coins = self.call_api(method='getInfo')['return']['funds']
            for coin in coins:
                ticker = coin
                amount = coins.get(coin)
                price = get_pair_price(ticker)
                balance = amount * price
                wallet.append([ticker, amount, price, balance])
            return wallet
        except SilentException as e:
            print('[e] Ошибка:', e)

    def order_buy(self, pair='ltc_btc', rate='0.1', amount=0.01):
        try:
            print('[i] Создаем ордер на покупку')
            print(self.call_api(method="Trade", pair=pair, type="buy", rate=rate, amount=amount))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def order_sell(self, pair='ltc_btc', rate='0.1', amount=0.01):
        try:
            print('[i] Создаем ордер на продажу', '*' * 30)
            print(self.call_api(method="Trade", pair=pair, type="sell", rate=rate, amount=amount))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def orders_get(self, pair='ltc_btc'):
        try:
            print('[i] Получаем список активных ордеров')
            print(self.call_api(method="ActiveOrders", pair=pair))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def order_info(self, order_id='123'):
        try:
            print('[i] Получаем информацию по ордеру')
            print(self.call_api(method="OrderInfo", order_id=order_id))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def order_cancel(self, order_id='123'):
        try:
            print('[i] Отменяем ордер')
            print(self.call_api(method="CancelOrder", order_id=order_id))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def get_trade_history(self, pair='ltc_btc'):
        try:
            print('[i] Получаем историю торгов')
            print(self.call_api(method="TradeHistory", pair=pair))
        except SilentException as e:
            print('[e] Ошибка:', e)

    def get_deposit_address(self, coin_name='BTC'):
        try:
            print('[i] Получаем адрес кошелька')
            print(self.call_api(method="GetDepositAddress", coinName=coin_name))
        except SilentException as e:
            print('[e] Ошибка:', e)
