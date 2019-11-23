import logging
from functools import wraps
import subprocess


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
                args_dict.update(kwargs)
            logger.debug('Args: {}'.format(args_dict))
            try:
                ret = func(*args, **kwargs)
                logger.debug('return: {}: {} {}'.format(ret.returncode, ret.stdout, ret.stderr))
                return ret
            except subprocess.CalledProcessError as e:
                logger.exception("{0} Why: {1}".format(e, e.stderr))
                raise e
            except Exception as e:
                logger.exception(e)
                raise e

        return wrapper

    return decorator
