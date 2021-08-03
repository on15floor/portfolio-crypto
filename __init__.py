import os

from dotenv import load_dotenv

from binance import Binance
from crex import Crex
from utils import draw_table
from yobit import Yobit

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
CREX_API_KEY = os.getenv('CREX_API_KEY')
CREX_API_SECRET = os.getenv('CREX_API_SECRET')
YOBIT_API_KEY = os.getenv('YOBIT_API_KEY')
YOBIT_API_SECRET = os.getenv('YOBIT_API_SECRET')


if __name__ == '__main__':
    bn = Binance(BINANCE_API_KEY, BINANCE_API_SECRET)
    draw_table(bn.get_wallet())

    cr = Crex(CREX_API_KEY, CREX_API_SECRET)
    draw_table(cr.get_wallet())

    yb = Yobit(YOBIT_API_KEY, YOBIT_API_SECRET)
    draw_table(yb.get_wallet())
