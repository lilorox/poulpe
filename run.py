#!/usr/bin/env python

import logging
from pprint import pprint
from poulpe import Poulpe

def main():
    logging.basicConfig(
        level=logging.DEBUG
    )

    p = Poulpe('./kraken.key')
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
