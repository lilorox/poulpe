#!/usr/bin/env python

import logging
from pprint import pprint
from poulpe import Poulpe

def main():
    logging.basicConfig(
        level=logging.WARNING
    )

    reference = 'ZEUR'

    p = Poulpe('./kraken.key')

    balance = p.get_balance()
    tickers = p.get_ticker([
        currency + reference
        for currency in balance.keys()
        if currency != reference
    ])

    portfolio = {}
    for currency, amount in balance.items():
        amount = float(amount)
        if(currency != reference and amount > 0):
            last_value = float(tickers[currency + reference]['c'][0])
            portfolio[currency] = [amount, last_value]
    pprint(portfolio)

    history = p.get_trades_history(trade_type='closed position')
    all_trades = []
    for id, trades in history['closed'].items():
        if 'trades' in trades:
            all_trades += trades['trades']
        # print(id, trades['descr']['order'], "cost:", trades['cost'], "price:", trades['descr']['price'])

    all_trades_info = list(p.get_trades_info(all_trades).values())
    all_trades_info.sort(key=lambda trade: float(trade['time']))
    for info in all_trades_info:
        if info['type'] == "buy":
            from_cur= info['pair'][4:]
            to_cur = info['pair'][:4]
        else:
            from_cur= info['pair'][:4]
            to_cur = info['pair'][4:]

        print(info['type'], info['pair'],
              "from:", from_cur,
              "to:", to_cur,
              "vol:", float(info['vol']),
              "price:", float(info['price']),
              "cost:", float(info['cost']),
              "fee:", float(info['fee'])
        )

# 'OQCDNK-CYHD5-EFTVXW': {
    # 'closetm': 1483951526.8565,
    # 'cost': '17.33952',
    # 'descr': {
        # 'leverage': 'none',
        # 'order': 'sell 0.40000000 ZECEUR '
        # '@ market',
        # 'ordertype': 'market',
        # 'pair': 'ZECEUR',
        # 'price': '0',
        # 'price2': '0',
        # 'type': 'sell'
    # },
    # 'expiretm': 0,
    # 'fee': '0.04508',
    # 'misc': '',
    # 'oflags': 'fciq',
    # 'opentm': 1483951526.0499,
    # 'price': '43.34880',
    # 'reason': None,
    # 'refid': None,
    # 'starttm': 0,
    # 'status': 'closed',
    # 'trades': [
        # 'T6E5LO-AEKYH-WTCQPW',
        # 'TWWT2S-BIUBM-PMC2F5'
    # ],
    # 'userref': None,
    # 'vol': '0.40000000',
    # 'vol_exec': '0.40000000'
# }



    # pprint(p.get_time())

    # pprint(p.get_assets(asset="YETH,XXBT"))

    # pprint(p.get_asset_pairs())
    # pprint(p.get_asset_pairs(pair='XZECZUSD')) # OK
    # pprint(p.get_asset_pairs(pair='BLAH')) # Fail
    # pprint(p.get_asset_pairs(pair='XZECZUSD', info='fees')) # OK
    # pprint(p.get_asset_pairs(pair='XZECZUSD', info='blah')) # Fail
    # pprint(p.get_asset_pairs(pair='BLAH', info='blah')) # Double fail

    # pprint(p.get_ticker('XETHZEUR,XXBTZEUT'))
    # pprint(p.get_ticker(['XETHZEUR', 'XXBTZEUR']))

    # pprint(p.get_OHLC('XETHXXBT', interval=2160, since=1481467260))

    # pprint(p.get_depth('XETHXXBT'))

    # pprint(p.get_trades('XETHXXBT'))

    # pprint(p.get_spread('XETHXXBT'))

    # pprint(p.get_balance())
    # pprint(p.get_trade_balance())
    # pprint(p.get_open_orders(trades=True))
    # pprint(p.get_closed_orders(trades=True))
    # pprint(p.get_trades_history())
    # pprint(p.get_trades_history(trade_type='no position'))
    # pprint(p.get_trades_info(['TAE7QR-OEHFZ-6ANLHW', 'T6TOY7-Y6N5Q-422MCQ']))
    # pprint(p.get_ledgers())
    # pprint(p.get_ledgers_info('LQRH7L-QUA2F-PEWJIW,LSITD6-VAIOT-PNMIQZ'))
    # pprint(p.get_trade_volume())


if __name__ == "__main__":
    main()
