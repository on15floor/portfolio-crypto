from prettytable import PrettyTable


# Считывание токена из файла
def read_key_secret(filename: str):
    with open(filename) as f:
        text = f.read().strip().split('\n')
        key = text[1]
        secret = text[3]
        return key, secret


# Ошибка
class SilentException(Exception):
    pass


# Рисуем табличку из списка [монета, количество, стоимость, баланс]
def draw_table(coins):
    table = PrettyTable(['Coin', 'Amount', 'Cost', 'Balance'])
    table.float_format['Amount'] = '.8'
    table.float_format['Cost'] = '.8'
    table.float_format['Balance'] = '.8'
    total_price = 0
    for coin in coins:
        table.add_row(coin)
        total_price += coin[3]
    print(table)
    print('Total balance: {:.8f} USD'.format(total_price))
