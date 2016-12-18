class UnknownKrakenErrorException(Exception): pass
class MultipleErrorsException(Exception): pass

class GeneralException(Exception): pass
class ServiceException(Exception): pass
class TradeException(Exception): pass
class OrderException(Exception): pass
class QueryException(Exception): pass


ERROR_TO_EXCEPTION_MAP = {
    'EGeneral': GeneralException,
    'EService': ServiceException,
    'ETrade': TradeException,
    'EOrder': OrderException,
    'EQuery': QueryException,
}


def get_exception_from_error(error):
    err_type, err_msg = error.split(':')

    ExceptionClass = ERROR_TO_EXCEPTION_MAP.get(err_type, UnknownKrakenErrorException)
    return ExceptionClass(err_msg)


def parse_errors(errors, args=None):
    if len(errors) == 1:
        msg = errors[0]

        if args is not None:
            msg += ' (args={})'.format(args)

        return get_exception_from_error(msg)

    msg = ', '.join(errors)
    if args is not None:
        msg += ' (args={})'.format(args)
    return MultipleErrorsException(msg)
