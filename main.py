from utils import read_key_secret, draw_table
from yobit import Yobit
from crex import Crex
from binance import Binance

#####################
# DRAW CREX BINANCE #
#####################
bn_key, bn_secret = read_key_secret('binance_token.txt')
bn = Binance(bn_key, bn_secret)
draw_table(bn.get_wallet())

#####################
# DRAW CREX WALLET  #
#####################
cr_key, cr_secret = read_key_secret('crex_token.txt')
cr = Crex(cr_key, cr_secret)
draw_table(cr.get_wallet())

#####################
# DRAW YOBIT WALLET #
#####################
yb_key, yb_secret = read_key_secret('yobit_token.txt')
yb = Yobit(yb_key, yb_secret)
draw_table(yb.get_wallet())
