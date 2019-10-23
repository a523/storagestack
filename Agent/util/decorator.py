import logging
from functools import wraps


def set_func_metadata(func):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        if record.funcName == 'wrapper':
            record.funcName = func.__name__
        if record.module == 'decorator':
            record.module = str(func.__module__).split('.')[-1]
        return record

    logging.setLogRecordFactory(record_factory)


def general_log(logger_name='agent'):
    logger = logging.getLogger(logger_name)

    def decorator(func):
        set_func_metadata(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            args_dict = {}
            if args:
                args_name = func.__code__.co_varnames
                args_dict = dict(zip(args_name, args))
            if kwargs:
                args_dict = args_dict.update(kwargs)
            logger.debug('args: {}'.format(args_dict))
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                raise e

        return wrapper

    return decorator
