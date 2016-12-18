import krakenex
import logging

from .exceptions import parse_errors

API_FUNCTIONS = {
    'Time': 'public',
    'Assets': 'public',
    'AssetPairs': 'public',
    'Ticker': 'public',
    'OHLC': 'public',
    'Depth': 'public',
    'Trades': 'public',
    'Spread': 'public',

    'Balance': 'private',
    'TradeBalance': 'private',
    'OpenOrders': 'private',
    'ClosedOrders': 'private',
    'QueryOrders': 'private',
    'TradesHistory': 'private',
    'QueryTrades': 'private',
    'OpenPositions': 'private',
    'Ledgers': 'private',
    'QueryLedgers': 'private',
    'TradeVolume': 'private',
    'AddOrder': 'private',
    'CancelOrder': 'private',
    'DepositMethods': 'private',
    'DepositAddresses': 'private',
    'DepositStatus': 'private',
    'WithdrawInfo': 'private',
    'Withdraw': 'private',
    'WithdrawStatus': 'private',
    'WithdrawCancel': 'private'
}


def parse_args(args):
    params = {}
    for arg, value in args.items():
        if value is not None and arg != "self":
            params[arg] = value
    return params


def list_to_str(arg):
    # Make sure the argument passed
    # is a comma-separated list
    result = ""
    if isinstance(arg, list):
        result = ','.join(arg)
    else:
        result = str(arg)
    return result


class Poulpe:
    def __init__(self, api_key_file):
        self._log = logging.getLogger(__name__)
        self._api_key_file = api_key_file
        self._k = self._init_kraken_api()


    def _init_kraken_api(self):
        k = krakenex.API()
        k.load_key(self._api_key_file)
        return k


    def _query(self, func, *args):
        method = API_FUNCTIONS.get(func, None)
        if method is None:
            # raise exception
            self._log.error('Unknown method {}'.format(func))
            return

        api_methods = {
            'public': self._k.query_public,
            'private': self._k.query_private
        }

        res = api_methods[method](func, *args)
        self._log.debug('Query response: {} (args={})'.format(res, args))

        errors = res.get('error', [])
        if len(errors) > 0:
            for e in errors:
                self._log.error('Error returned by Kraken API: {}'.format(e))
            raise parse_errors(errors, args)
        return res['result']


    ##############
    # Public API #
    ##############

    def get_time(self):
        return self._query('Time')


    def get_assets(self, info=None, aclass=None, asset=None):
        args = parse_args(locals())
        return self._query('Assets', args)


    def get_asset_pairs(self, info=None, pair=None):
        args = parse_args(locals())
        return self._query('AssetPairs', args)


    def get_ticker(self, pairs):
        return self._query('Ticker', { 'pair': list_to_str(pairs) })


    def get_OHLC(self, pair, interval=None, since=None):
        args = parse_args(locals())
        allowed_intervals = [ 1, 5, 15, 30, 60, 240, 1440, 10080, 21600 ]
        if 'interval' in args and args['interval'] not in allowed_intervals:
            args['interval'] = 1

        return self._query('OHLC', args)


    def get_depth(self, pair, count=None):
        args = parse_args(locals())
        return self._query('Depth', args)


    def get_trades(self, pair, since=None):
        args = parse_args(locals())
        return self._query('Trades', args)


    def get_spread(self, pair, since=None):
        args = parse_args(locals())
        return self._query('Spread', args)


    #########################
    # Private User data API #
    #########################

    def get_balance(self):
        return self._query('Balance')


    def get_trade_balance(self, aclass=None, asset=None):
        args = parse_args(locals())
        return self._query('TradeBalance', args)


    def get_open_orders(self, trades=False, userref=None):
        args = parse_args(locals())
        return self._query('OpenOrders', args)


    def get_closed_orders(self, trades=False, userref=None,
                          start=None, end=None, ofs=None,
                          closetime="both"):
        args = parse_args(locals())
        return self._query('ClosedOrders', args)


    def get_orders_info(self, txids, trades=False, userref=None):
        args = parse_args(locals())
        args['txid'] = list_to_str(txids)
        del args['txids']
        return self._query('QueryOrders', args)


    def get_trades_history(self, trade_type="all", trades=False,
                          start=None, end=None, ofs=None):
        # Rename 'trade_type' argument to 'type'
        args = parse_args(locals())
        args['type'] = args['trade_type']
        del args['trade_type']
        return self._query('ClosedOrders', args)


    def get_trades_info(self, txids, trades=False):
        args = parse_args(locals())
        args['txid'] = list_to_str(txids)
        del args['txids']
        return self._query('QueryTrades', args)


    def get_open_postitions(self, txids, docalcs=False):
        args = parse_args(locals())
        args['txid'] = list_to_str(txids)
        del args['txids']
        return self._query('OpenPositions', args)


    def get_ledgers(self, aclass="currency", asset="all", ledger_type="all",
                    start=None, end=None, ofs=None):
        # Rename 'ledger_type' argument to 'type'
        args = parse_args(locals())
        args['type'] = args['ledger_type']
        del args['ledger_type']
        return self._query('Ledgers', args)


    def get_ledgers_info(self, ids):
        args = parse_args(locals())
        args['id'] = list_to_str(ids)
        del args['ids']
        return self._query('QueryLedgers', args)


    def get_trade_volume(self, pairs=None, fee_info=None):
        args = parse_args(locals())
        if pairs is not None:
            args['pair'] = list_to_str(pairs)
            del args['pairs']

        if fee_info is not None:
            args['fee-info'] = fee_info
            del args['fee_info']

        return self._query('TradeVolume', args)

